#!/usr/bin/env python3
"""CRISP benchmark runner. See bench/README.md.

Subcommands: baseline | arms | judge | assemble | summary

Paths beginning with `shared/` resolve to the shared contract dir (default ../shared
relative to the repo root; override with CRISP_SHARED).
"""
import argparse
import json
import os
import random
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from count import TOKENIZER, tokens_est, words  # noqa: E402
from gateway import GatewayPool  # noqa: E402
import stats  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.environ.get("CRISP_SHARED") or (
    os.path.join(REPO, "shared") if os.path.isdir(os.path.join(REPO, "shared")) else os.path.join(os.path.dirname(REPO), "shared")
)
BASELINE_SCHEMA = "crisp-bench/baseline-v1"
RESULTS_SCHEMA = "crisp-bench/v1"
ARMS_SCHEMA = "crisp-bench/arms-v1"
JUDGED_SCHEMA = "crisp-bench/judged-v1"
DIMS = stats.DIMS


# ---------------------------------------------------------------- helpers
def resolve(path):
    """`shared/...` -> SHARED dir; everything else relative to cwd."""
    if path == "shared" or path.startswith("shared/"):
        if not os.path.exists(path):
            return os.path.join(SHARED, path[len("shared/"):])
    return path


def shared_rel(path):
    """Path as stored in result files: relative to shared/ when inside it."""
    p = os.path.abspath(resolve(path))
    root = os.path.abspath(SHARED) + os.sep
    return p[len(root):] if p.startswith(root) else path


def load_json(path):
    with open(resolve(path), encoding="utf-8") as f:
        return json.load(f)


def load_json_if_exists(path):
    p = resolve(path)
    return load_json(path) if os.path.exists(p) else None


def save_json(path, obj):
    p = resolve(path)
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, p)


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_fixtures(limit=False):
    data = load_json("shared/fixtures.json")
    out = []
    for sc in data["scenarios"]:
        for fx in sc["fixtures"]:
            out.append({"id": fx["id"], "scenario": sc["id"], "prompt": fx["prompt"], "required_facts": fx["required_facts"]})
    return out[:1] if limit else out


def read_prompt(prompts_dir, name):
    with open(os.path.join(resolve(prompts_dir), name), encoding="utf-8") as f:
        return f.read().strip()


def make_sample(index, resp, source_sample=None):
    s = {
        "index": index,
        "text": resp["text"],
        "words": words(resp["text"]),
        "tokens_est": tokens_est(resp["text"]),
        "usage": resp["usage"],
        "latency_ms": resp["latency_ms"],
    }
    if source_sample is not None:
        s["source_sample"] = source_sample
    return s


def run_tasks(tasks, on_done, workers, label):
    """tasks: list of (key, zero-arg callable). on_done(key, result) runs under a lock.
    Returns list of (key, error) for failures."""
    lock = threading.Lock()
    failures = []
    total, done = len(tasks), 0
    if not tasks:
        print(f"{label}: nothing to do")
        return failures
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fn): key for key, fn in tasks}
        try:
            for fut in as_completed(futs):
                key = futs[fut]
                try:
                    res = fut.result()
                except Exception as e:  # noqa: BLE001 - report and continue; resume retries it
                    failures.append((key, str(e)))
                    print(f"{label}: FAILED {key}: {e}", file=sys.stderr)
                    continue
                with lock:
                    on_done(key, res)
                    done += 1
                    print(f"{label}: {done}/{total} {key}", flush=True)
        except KeyboardInterrupt:
            for f in futs:
                f.cancel()
            raise
    return failures


def finish(failures):
    if failures:
        print(f"{len(failures)} task(s) failed; rerun the same command to retry them.", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------- baseline
def cmd_baseline(a):
    fixtures = load_fixtures(a.limit)
    n = 1 if a.limit else a.n
    settings = {"reasoning": a.reasoning, "temperature": None}
    out = load_json_if_exists(a.out) or {
        "schema": BASELINE_SCHEMA,
        "generator": a.generator,
        "generator_settings": settings,
        "generated_at": now(),
        "tests": {},
    }
    if out["generator"] != a.generator or out["generator_settings"].get("reasoning") != a.reasoning:
        sys.exit(f"{a.out} was made with {out['generator']} / {out['generator_settings']}; refusing to mix")

    todo = []
    for fx in fixtures:
        have = {s["index"] for s in out["tests"].get(fx["id"], {}).get("samples", [])}
        for i in range(n):
            if i not in have:
                todo.append(((fx["id"], i), fx["prompt"]))

    with GatewayPool(a.concurrency) as pool:
        def mk(prompt):
            return lambda: pool.chat(a.generator, [{"role": "user", "content": prompt}], a.reasoning)

        def on_done(key, resp):
            tid, i = key
            samples = out["tests"].setdefault(tid, {"samples": []})["samples"]
            samples.append(make_sample(i, resp))
            samples.sort(key=lambda s: s["index"])
            save_json(a.out, out)

        failures = run_tasks([(k, mk(p)) for k, p in todo], on_done, a.concurrency, "baseline")
    print(f"wrote {a.out}")
    finish(failures)


# ---------------------------------------------------------------- arms
def cmd_arms(a):
    base = load_json(a.baseline)
    if base.get("schema") != BASELINE_SCHEMA:
        sys.exit(f"{a.baseline}: not a {BASELINE_SCHEMA} file")
    reasoning = a.reasoning if a.reasoning is not None else base["generator_settings"].get("reasoning")
    prompts = {name: read_prompt(a.prompts, f"{name}.md") for name in ("crisp", "crispify")}
    fixtures = [f for f in load_fixtures() if f["id"] in base["tests"]]
    if a.limit:
        fixtures = fixtures[:1]
    out = load_json_if_exists(a.out) or {
        "schema": ARMS_SCHEMA,
        "team": a.team,
        "generator": a.generator,
        "generator_settings": {"reasoning": reasoning, "temperature": None},
        "baseline_file": a.baseline,
        "prompts": prompts,
        "generated_at": now(),
        "tests": {},
    }
    if out["prompts"] != prompts or out["generator"] != a.generator:
        sys.exit(f"{a.out} was made with different prompts or generator; delete it to start over")

    todo = []
    for fx in fixtures:
        bsamples = base["tests"][fx["id"]]["samples"]
        t = out["tests"].setdefault(fx["id"], {"crisp": {"samples": []}, "crispify": {"samples": []}})
        have_c = {s["index"] for s in t["crisp"]["samples"]}
        have_x = {s["index"] for s in t["crispify"]["samples"]}
        for bs in bsamples:
            i = bs["index"]
            if i not in have_c:
                todo.append(((fx["id"], "crisp", i), [
                    {"role": "system", "content": prompts["crisp"]},
                    {"role": "user", "content": fx["prompt"]},
                ], None))
            if i not in have_x:
                todo.append(((fx["id"], "crispify", i), [
                    {"role": "system", "content": prompts["crispify"]},
                    {"role": "user", "content": "Crispify this:\n\n" + bs["text"]},
                ], i))

    with GatewayPool(a.concurrency) as pool:
        def mk(msgs):
            return lambda: pool.chat(a.generator, msgs, reasoning)

        sources = {k: src for k, _, src in todo}

        def on_done(key, resp):
            tid, arm, i = key
            samples = out["tests"][tid][arm]["samples"]
            samples.append(make_sample(i, resp, sources[key]))
            samples.sort(key=lambda s: s["index"])
            save_json(a.out, out)

        failures = run_tasks([(k, mk(m)) for k, m, _ in todo], on_done, a.concurrency, "arms")
    print(f"wrote {a.out}")
    finish(failures)


# ---------------------------------------------------------------- judge
def rubric_template():
    with open(os.path.join(SHARED, "rubric.md"), encoding="utf-8") as f:
        text = f.read()
    return text.split("\n---\n", 1)[1].strip("\n")


def fill_rubric(template, prompt, facts, answer_a, answer_b):
    facts_list = "\n".join(f"{f['id']}: {f['text']}" for f in facts)
    values = {"prompt": prompt, "required_facts_list": facts_list, "answer_a": answer_a, "answer_b": answer_b}
    # drop the authoring comment after the facts placeholder, then substitute in one pass
    template = re.sub(r"(\{\{required_facts_list\}\})[ \t]*<!--.*?-->", r"\1", template)
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)] if m.group(1) in values else m.group(0), template)


def parse_judge_json(text, fact_ids):
    """-> validated dict or raises ValueError."""
    candidates = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        candidates.append(text[start:end + 1])
    last = None
    for c in candidates:
        try:
            d = json.loads(c)
            validate_judge(d, fact_ids)
            return d
        except (ValueError, KeyError, TypeError) as e:
            last = e
    raise ValueError(f"no valid judge JSON ({last})")


def validate_judge(d, fact_ids):
    for side in ("A", "B"):
        for dim in DIMS:
            v = d[side][dim]
            if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 5:
                raise ValueError(f"{side}.{dim}={v!r}")
        fp = d[side]["facts_present"]
        if not isinstance(fp, list):
            raise ValueError("facts_present not a list")
        unknown = [f for f in fp if f not in fact_ids]
        if unknown:
            raise ValueError(f"unknown fact ids {unknown}")
    if str(d["preferred"]).strip().lower() not in ("a", "b", "tie"):
        raise ValueError(f"preferred={d['preferred']!r}")


def build_judgment(arm, idx, base_idx, order, judge, fact_ids, d):
    side_base, side_arm = ("A", "B") if order == "baseline_first" else ("B", "A")
    pref = str(d["preferred"]).strip().lower()
    preferred = "tie" if pref == "tie" else ("baseline" if pref.upper() == side_base else "arm")
    present = {side: [f for f in fact_ids if f in d[side]["facts_present"]] for side in ("A", "B")}
    pb, pa = present[side_base], present[side_arm]
    ul = d.get("useful_lost") or {}
    return {
        "arm": arm,
        "sample": idx,
        "baseline_sample": base_idx,
        "order": order,
        "judge": judge,
        "scores": {
            "baseline": {k: d[side_base][k] for k in DIMS},
            "arm": {k: d[side_arm][k] for k in DIMS},
        },
        "facts": {
            "baseline": {"present": pb, "total": len(fact_ids)},
            "arm": {"present": pa, "total": len(fact_ids)},
        },
        "facts_lost": [f for f in pb if f not in pa],
        "useful_lost": {"baseline": str(ul.get(side_base) or ""), "arm": str(ul.get(side_arm) or "")},
        "preferred": preferred,
        "notes": str(d.get("notes") or ""),
    }


def cmd_judge(a):
    arms = load_json(a.arms)
    base = load_json(a.baseline)
    fixtures = {f["id"]: f for f in load_fixtures()}
    template = rubric_template()
    tids = [t for t in fixtures if t in arms["tests"] and t in base["tests"]]
    if a.limit:
        tids = tids[:1]
    out = load_json_if_exists(a.out) or {
        "schema": JUDGED_SCHEMA,
        "team": arms.get("team"),
        "generator": arms["generator"],
        "generator_settings": arms["generator_settings"],
        "judge": a.judge,
        "judge_settings": {"reasoning": a.reasoning},
        "arms_file": a.arms,
        "baseline_file": a.baseline,
        "generated_at": now(),
        "tests": {},
    }
    if out["judge"] != a.judge:
        sys.exit(f"{a.out} was made with judge {out['judge']}; delete it to start over")

    todo = []
    for tid in tids:
        fx = fixtures[tid]
        bsamples = {s["index"]: s for s in base["tests"][tid]["samples"]}
        done = {(j["arm"], j["sample"]) for j in out["tests"].get(tid, {}).get("judgments", [])}
        for arm in stats.ARMS:
            for s in arms["tests"][tid][arm]["samples"]:
                if (arm, s["index"]) in done:
                    continue
                b_idx = s["index"] if arm == "crisp" else s["source_sample"]
                if b_idx not in bsamples:
                    print(f"judge: {tid}/{arm}/{s['index']}: baseline sample {b_idx} missing, skipped", file=sys.stderr)
                    continue
                todo.append(((tid, arm, s["index"]), fx, bsamples[b_idx], s, b_idx))

    with GatewayPool(a.concurrency) as pool:
        def mk(key, fx, bs, s):
            tid, arm, idx = key
            fact_ids = [f["id"] for f in fx["required_facts"]]
            order = "baseline_first" if random.Random(f"{tid}:{arm}:{idx}").random() < 0.5 else "arm_first"
            first, second = (bs["text"], s["text"]) if order == "baseline_first" else (s["text"], bs["text"])
            msg = [{"role": "user", "content": fill_rubric(template, fx["prompt"], fx["required_facts"], first, second)}]

            def job():
                err = None
                for _ in range(2):  # one retry on unparseable reply
                    resp = pool.chat(a.judge, msg, a.reasoning)
                    try:
                        d = parse_judge_json(resp["text"], fact_ids)
                        return build_judgment(arm, idx, bs["index"], order, a.judge, fact_ids, d)
                    except ValueError as e:
                        err = e
                raise RuntimeError(f"unparseable judge reply: {err}")

            return job

        def on_done(key, judgment):
            js = out["tests"].setdefault(key[0], {"judgments": []})["judgments"]
            js.append(judgment)
            js.sort(key=lambda j: (j["arm"], j["sample"]))
            save_json(a.out, out)

        failures = run_tasks([(t[0], mk(t[0], t[1], t[2], t[3])) for t in todo], on_done, a.concurrency, "judge")
    print(f"wrote {a.out}")
    finish(failures)


# ---------------------------------------------------------------- assemble
def cmd_assemble(a):
    prompts = {name: read_prompt(a.prompts, f"{name}.md") for name in ("crisp", "crispify")}
    result = {
        "schema": RESULTS_SCHEMA,
        "team": a.team,
        "generated_at": now(),
        "prompts": {
            "crisp": prompts["crisp"],
            "crisp_tokens_est": tokens_est(prompts["crisp"]),
            "crispify": prompts["crispify"],
            "crispify_tokens_est": tokens_est(prompts["crispify"]),
        },
        "lanes": [],
    }
    seen = set()
    order = [f["id"] for f in load_fixtures()]
    for lane_path in a.lane:
        judged = load_json(lane_path)
        if judged.get("schema") != JUDGED_SCHEMA:
            sys.exit(f"{lane_path}: not a {JUDGED_SCHEMA} file")
        arms = load_json(judged["arms_file"])
        base = load_json(judged["baseline_file"])
        if arms["prompts"] != prompts:
            sys.exit(f"{judged['arms_file']} was generated with prompts that differ from {a.prompts}")
        key = (judged["generator"], judged["judge"])
        if key in seen:
            sys.exit(f"duplicate lane {key}")
        seen.add(key)
        tests = []
        for tid in order:
            if tid not in arms["tests"] or tid not in base["tests"]:
                continue
            tests.append({
                "id": tid,
                "arms": {
                    "baseline": {"samples": base["tests"][tid]["samples"]},
                    "crisp": {"samples": arms["tests"][tid]["crisp"]["samples"]},
                    "crispify": {"samples": arms["tests"][tid]["crispify"]["samples"]},
                },
                "judgments": judged["tests"].get(tid, {}).get("judgments", []),
            })
        result["lanes"].append({
            "generator": judged["generator"],
            "generator_settings": judged["generator_settings"],
            "judge": judged["judge"],
            "judge_settings": judged.get("judge_settings"),
            "tokenizer_est": TOKENIZER,
            "baseline_file": shared_rel(judged["baseline_file"]),
            "tests": tests,
        })
    save_json(a.out, result)
    print(f"wrote {a.out} ({len(result['lanes'])} lane(s))")


# ---------------------------------------------------------------- summary
def print_table(rows):
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    for k, r in enumerate(rows):
        print("  " + "  ".join(str(c).ljust(w) if i == 0 else str(c).rjust(w) for i, (c, w) in enumerate(zip(r, widths))))
        if k == 0:
            print("  " + "  ".join("-" * w for w in widths))


def cmd_summary(a):
    res = load_json(a.results)
    p = res["prompts"]
    print(f"team={res['team']}  schema={res['schema']}  generated={res['generated_at']}")
    print(f"prompt overhead (tokens_est): crisp={p['crisp_tokens_est']}  crispify={p['crispify_tokens_est']}")
    for lane in res["lanes"]:
        print(f"\n=== generator {lane['generator']} | judge {lane['judge']} | {lane['tokenizer_est']} (estimate) ===")
        st = stats.lane_stats(lane)
        base_row = next((s for s in st.values() if s["n"]), None)
        rows = [["arm", "n", "words", "tok_est", "Δwords%", "Δtok%", "out_tok", "in_tok Δ", "facts kept%", "facts cov%", "W/T/L", "useful lost"]]
        if base_row:
            rows.append(["baseline", base_row["n"], stats.fmt(base_row["base_words"]), stats.fmt(base_row["base_tokens"]), "-", "-",
                         stats.fmt(base_row["base_out_tokens"], 0), "-", "-",
                         stats.fmt(_pct(st, "base_cov"), 0), "-", "-"])
        for arm in stats.ARMS:
            s = st[arm]
            if not s["n"]:
                continue
            f = s["facts"]
            d_in = None if s["in_tokens"] is None or s["base_in_tokens"] is None else s["in_tokens"] - s["base_in_tokens"]
            w, t, l = s["wtl"]
            rows.append([arm, s["n"], stats.fmt(s["words"]), stats.fmt(s["tokens"]), stats.fmt(s["red_words"], 0), stats.fmt(s["red_tokens"], 0),
                         stats.fmt(s["out_tokens"], 0), stats.fmt(d_in, 0, "") if d_in is None else f"{d_in:+.0f}",
                         stats.fmt(None if f["retained"] is None else f["retained"] * 100, 0),
                         stats.fmt(None if f["arm_cov"] is None else f["arm_cov"] * 100, 0),
                         f"{w}/{t}/{l}", s["useful_lost_arm"]])
        print_table(rows)
        print("\n  rubric means (base vs arm, paired):")
        active = [arm for arm in stats.ARMS if st[arm]["n_judged"]]
        if active:
            hdr = ["dim"]
            for arm in active:
                hdr += [f"base|{arm}", arm]
            rows = [hdr]
            for d in stats.DIMS + ["overall"]:
                r = [d]
                for arm in active:
                    s = st[arm]
                    if d == "overall":
                        r += [stats.fmt(s["overall_base"], 2), stats.fmt(s["overall_arm"], 2)]
                    else:
                        r += [stats.fmt(s["dims_base"][d], 2), stats.fmt(s["dims_arm"][d], 2)]
                rows.append(r)
            print_table(rows)
        else:
            print("  (no judgments)")

        print("\n  per fixture (mean over samples; base→arm):")
        rows = [["fixture", "arm", "words", "tok_est", "overall", "facts_lost", "W/T/L"]]
        for t in lane["tests"]:
            for arm in stats.ARMS:
                sm = stats.samples_of(t, arm)
                if not sm:
                    continue
                bs = stats.samples_of(t, "baseline")
                js = stats.judgments_of(t, arm)
                ob = stats.mean([stats.overall(j["scores"]["baseline"]) for j in js])
                oa = stats.mean([stats.overall(j["scores"]["arm"]) for j in js])
                lost = ",".join(sorted({f for j in js for f in j["facts_lost"]})) or "-"
                w, ti, l = stats.wtl(js)
                rows.append([t["id"], arm,
                             f"{stats.fmt(stats.mean([s['words'] for s in bs]), 0)}→{stats.fmt(stats.mean([s['words'] for s in sm]), 0)}",
                             f"{stats.fmt(stats.mean([s['tokens_est'] for s in bs]), 0)}→{stats.fmt(stats.mean([s['tokens_est'] for s in sm]), 0)}",
                             f"{stats.fmt(ob, 2)}→{stats.fmt(oa, 2)}", lost, f"{w}/{ti}/{l}"])
        print_table(rows)


def _pct(st, key):
    for s in st.values():
        v = s["facts"].get(key)
        if v is not None:
            return v * 100
    return None


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--concurrency", type=int, default=4)
        p.add_argument("--limit", action="store_true", help="smoke test: first fixture only (n=1 for baseline)")

    p = sub.add_parser("baseline")
    p.add_argument("--generator", required=True)
    p.add_argument("--n", type=int, default=3)
    p.add_argument("--reasoning", default=None)
    p.add_argument("--out", required=True)
    common(p)
    p.set_defaults(fn=cmd_baseline)

    p = sub.add_parser("arms")
    p.add_argument("--team", required=True)
    p.add_argument("--generator", required=True)
    p.add_argument("--reasoning", default=None, help="default: the baseline file's setting")
    p.add_argument("--baseline", required=True)
    p.add_argument("--prompts", required=True)
    p.add_argument("--out", required=True)
    common(p)
    p.set_defaults(fn=cmd_arms)

    p = sub.add_parser("judge")
    p.add_argument("--arms", required=True)
    p.add_argument("--baseline", required=True)
    p.add_argument("--judge", required=True)
    p.add_argument("--reasoning", default="high")
    p.add_argument("--out", required=True)
    common(p)
    p.set_defaults(fn=cmd_judge)

    p = sub.add_parser("assemble")
    p.add_argument("--team", required=True)
    p.add_argument("--prompts", required=True)
    p.add_argument("--lane", action="append", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_assemble)

    p = sub.add_parser("summary")
    p.add_argument("results")
    p.set_defaults(fn=cmd_summary)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
