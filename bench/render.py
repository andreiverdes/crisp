#!/usr/bin/env python3
"""Standalone HTML comparison renderer (inline CSS, no network).

python3 bench/render.py shared/results/*.json -o bench/out/crisp-comparison.html
"""
import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stats  # noqa: E402
from stats import ARMS, DIMS  # noqa: E402

ARM_LABEL = {"baseline": "baseline", "crisp": "crisp", "crispify": "crispify"}
SHORT = {"correctness": "cor", "clarity": "cla", "ambiguity": "amb", "scanability": "sca",
         "relevance": "rel", "conversational": "con", "completeness": "cmp"}

CSS = """
body{font:14px/1.5 -apple-system,system-ui,sans-serif;margin:0;padding:24px;background:#f6f7f9;color:#1b1f24}
h1{font-size:22px;margin:0 0 4px} h2{font-size:18px;margin:32px 0 8px;border-bottom:2px solid #d0d5dd;padding-bottom:4px}
h3{font-size:15px;margin:24px 0 6px} .muted{color:#667085;font-size:12px}
table.sum{border-collapse:collapse;background:#fff;margin:8px 0 16px;font-size:13px}
table.sum th,table.sum td{border:1px solid #d0d5dd;padding:4px 10px;text-align:right;white-space:nowrap}
table.sum th{background:#eef0f4} table.sum td:first-child,table.sum th:first-child{text-align:left}
table.sum th.team{text-align:center;border-bottom:none}
.good{color:#067647;font-weight:600}.bad{color:#b42318;font-weight:600}
.fixture{background:#fff;border:1px solid #d0d5dd;border-radius:6px;padding:12px;margin:12px 0}
.prompt{background:#f2f4f7;border-left:3px solid #98a2b3;padding:8px 12px;margin:6px 0 12px;white-space:pre-wrap;font-size:13px}
.cols{display:grid;gap:10px;align-items:start}
.col{border:1px solid #d0d5dd;border-radius:6px;overflow:hidden;background:#fff;min-width:0}
.col>.head{background:#eef0f4;padding:4px 10px;font-weight:600;font-size:12px}
.col.baseline>.head{background:#e4e7ec}.col.crisp>.head{background:#d1e9ff}.col.crispify>.head{background:#d3f8df}
.sample{padding:8px 12px;border-top:1px solid #eaecf0}
.sample:first-of-type{border-top:none}
.body{font-size:13px;overflow-wrap:anywhere}
.body p{margin:4px 0}.body ul{margin:4px 0;padding-left:20px}.body h4,.body h5,.body h6{margin:8px 0 2px}
.body pre{background:#101828;color:#e4e7ec;padding:8px;border-radius:4px;overflow-x:auto;font-size:12px}
.body code{background:#eef0f4;padding:0 3px;border-radius:3px;font-size:12px}.body pre code{background:none;padding:0}
.meta{margin-top:6px;font-size:11px;color:#475467;border-top:1px dashed #d0d5dd;padding-top:4px}
.meta b{color:#1b1f24}.empty{color:#98a2b3;padding:8px 12px}
details{margin-top:4px}
summary{cursor:pointer}
"""


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def inline(text):
    """Escape, then apply code spans and bold. Escaping first keeps every other character inert."""
    t = esc(text)
    t = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t


def md(text):
    """Minimal markdown: headings, bullets, code fences, bold, inline code. Everything else escaped text."""
    out, para, in_list, in_code = [], [], False, False
    code = []

    def flush_para():
        if para:
            out.append("<p>" + "<br>".join(inline(l) for l in para) + "</p>")
            para.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in (text or "").splitlines():
        if line.strip().startswith("```"):
            if in_code:
                out.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
                code, in_code = [], False
            else:
                flush_para(); close_list()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        b = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            flush_para(); close_list()
            lvl = min(len(m.group(1)) + 3, 6)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
        elif b:
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(b.group(1))}</li>")
        elif not line.strip():
            flush_para(); close_list()
        else:
            close_list(); para.append(line)
    if in_code:
        out.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
    flush_para(); close_list()
    return "".join(out)


def pct_cls(v, good_positive=True):
    if v is None:
        return ""
    return "good" if (v > 0) == good_positive and v != 0 else ("bad" if v != 0 else "")


def summary_tables(lanes_by_team):
    """lanes_by_team: [(team, lane)] for the same (generator, judge)."""
    stats_by = [(team, stats.lane_stats(lane)) for team, lane in lanes_by_team]
    cols = [(team, arm) for team, st in stats_by for arm in ARMS if st[arm]["n"]]
    first = next((st[arm] for _, st in stats_by for arm in ARMS if st[arm]["n"]), None)
    h = ["<table class='sum'><tr><th rowspan=2>metric</th><th rowspan=2>baseline</th>"]
    for team in dict.fromkeys(t for t, _ in cols):
        n = sum(1 for t, _ in cols if t == team)
        h.append(f"<th class='team' colspan={n}>{esc(team)}</th>")
    h.append("</tr><tr>" + "".join(f"<th>{arm}</th>" for _, arm in cols) + "</tr>")
    st_of = dict(stats_by)

    def row(label, base, fn, cls=None):
        cells = []
        for team, arm in cols:
            v, txt = fn(st_of[team][arm])
            c = cls(v) if cls else ""
            cells.append(f"<td class='{c}'>{txt}</td>")
        h.append(f"<tr><td>{label}</td><td>{base}</td>{''.join(cells)}</tr>")

    if first is None:
        return "<p class='muted'>no samples</p>"
    row("n samples", first["n"], lambda s: (s["n"], s["n"]))
    row("mean words", stats.fmt(first["base_words"]), lambda s: (s["words"], stats.fmt(s["words"])))
    row("mean tokens_est", stats.fmt(first["base_tokens"]), lambda s: (s["tokens"], stats.fmt(s["tokens"])))
    row("words reduction", "-", lambda s: (s["red_words"], stats.fmt(s["red_words"], 0, "%")), lambda v: pct_cls(v))
    row("tokens reduction", "-", lambda s: (s["red_tokens"], stats.fmt(s["red_tokens"], 0, "%")), lambda v: pct_cls(v))
    row("mean output_tokens (provider)", stats.fmt(first["base_out_tokens"], 0), lambda s: (s["out_tokens"], stats.fmt(s["out_tokens"], 0)))
    for d in DIMS:
        row(d, stats.fmt(_base_dim(stats_by, d), 2), lambda s, d=d: (s["dims_arm"][d], stats.fmt(s["dims_arm"][d], 2)))
    row("<b>overall</b>", stats.fmt(_base_overall(stats_by), 2), lambda s: (s["overall_arm"], stats.fmt(s["overall_arm"], 2)))
    row("facts retained", "-", lambda s: (_p(s["facts"]["retained"]), stats.fmt(_p(s["facts"]["retained"]), 0, "%")))
    row("facts covered", stats.fmt(_p(first["facts"]["base_cov"]), 0, "%"), lambda s: (_p(s["facts"]["arm_cov"]), stats.fmt(_p(s["facts"]["arm_cov"]), 0, "%")))
    row("win / tie / loss", "-", lambda s: (None, "{}/{}/{}".format(*s["wtl"])))
    row("win rate", "-", lambda s: (_winrate(s), stats.fmt(_winrate(s), 0, "%")))
    row("judgments with useful content lost", "-", lambda s: (None, f"{s['useful_lost_arm']} / {s['n_judged']}"))
    h.append("</table>")
    return "".join(h)


def _p(x):
    return None if x is None else x * 100


def _winrate(s):
    w, t, l = s["wtl"]
    n = w + t + l
    return None if not n else 100 * (w + 0.5 * t) / n


def _base_dim(stats_by, d):
    vals = [st[a]["dims_base"][d] for _, st in stats_by for a in ARMS if st[a]["n_judged"]]
    return stats.mean(vals)


def _base_overall(stats_by):
    return stats.mean([_base_dim(stats_by, d) for d in DIMS])


def sample_html(sample, arm, judgments):
    meta = [f"<b>{sample['words']}</b> words", f"<b>{sample['tokens_est']}</b> tok_est"]
    u = sample.get("usage") or {}
    if u.get("output_tokens") is not None:
        r = u.get("reasoning_tokens")
        meta.append(f"out {u['output_tokens']}" + (f" (reasoning {r})" if r is not None else ""))
    if sample.get("latency_ms") is not None:
        meta.append(f"{sample['latency_ms'] / 1000:.1f}s")
    if "source_sample" in sample:
        meta.append(f"from baseline #{sample['source_sample']}")
    extra = ""
    if judgments:
        j = judgments[0]
        sc = j["scores"]["arm"] if arm != "baseline" else j["scores"]["baseline"]
        meta.append("<b>" + f"{stats.overall(sc):.2f}</b> overall")
        extra += "<div>" + " ".join(f"{SHORT[d]} <b>{sc[d]}</b>" for d in DIMS) + "</div>"
        if arm != "baseline":
            lost = ", ".join(j["facts_lost"]) or "none"
            f = j["facts"]["arm"]
            extra += f"<div>facts {len(f['present'])}/{f['total']} · lost vs baseline: <b>{esc(lost)}</b> · preferred: <b>{esc(j['preferred'])}</b> ({esc(j['order'])})</div>"
            if j.get("useful_lost", {}).get("arm"):
                extra += f"<div>arm lacks: {esc(j['useful_lost']['arm'])}</div>"
            if j.get("useful_lost", {}).get("baseline"):
                extra += f"<div>baseline lacks: {esc(j['useful_lost']['baseline'])}</div>"
            if j.get("notes"):
                extra += f"<div>notes: {esc(j['notes'])}</div>"
        else:
            f = j["facts"]["baseline"]
            extra += f"<div>facts {len(f['present'])}/{f['total']}</div>"
    return (f"<div class='sample'><div class='muted'>sample {sample['index']}</div><div class='body'>{md(sample['text'])}</div>"
            f"<div class='meta'>{' · '.join(meta)}{extra}</div></div>")


def baseline_judgments(test, sample_index):
    """Judgments where this baseline sample was a comparator (first one, for scores/facts display)."""
    return [j for j in test.get("judgments", []) if j["baseline_sample"] == sample_index]


def fixture_html(tests_by_team, fixtures):
    teams = list(tests_by_team)
    base_test = tests_by_team[teams[0]]
    columns = [("baseline", None, base_test)]
    for team in teams:
        for arm in ARMS:
            if stats.samples_of(tests_by_team[team], arm):
                columns.append((arm, team, tests_by_team[team]))
    tid = base_test["id"]
    parts = [f"<div class='fixture'><h3>{esc(tid)}</h3>"]
    p = fixtures.get(tid)
    parts.append(f"<div class='prompt'>{esc(p) if p else 'prompt text not in fixtures.json'}</div>")
    parts.append(f"<div class='cols' style='grid-template-columns:repeat({len(columns)},minmax(0,1fr))'>")
    for arm, team, test in columns:
        title = "baseline" if team is None else f"{esc(team)} {arm}"
        parts.append(f"<div class='col {arm}'><div class='head'>{title}</div>")
        samples = stats.samples_of(test, arm)
        if not samples:
            parts.append("<div class='empty'>no samples</div>")
        for s in samples:
            if arm == "baseline":
                js = baseline_judgments(test, s["index"])
            else:
                js = [j for j in stats.judgments_of(test, arm) if j["sample"] == s["index"]]
            parts.append(sample_html(s, arm, js))
        parts.append("</div>")
    parts.append("</div></div>")
    return "".join(parts)


def load_fixture_prompts():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.environ.get("CRISP_SHARED", ""), os.path.join(here, "..", "shared"), os.path.join(here, "..", "..", "shared")):
        f = os.path.join(p, "fixtures.json")
        if p and os.path.exists(f):
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            return {fx["id"]: fx["prompt"] for sc in d["scenarios"] for fx in sc["fixtures"]}
    return {}


def render(results):
    fixtures = load_fixture_prompts()
    teams = [r["team"] for r in results]
    lane_keys = []
    for r in results:
        for lane in r["lanes"]:
            k = (lane["generator"], lane["judge"])
            if k not in lane_keys:
                lane_keys.append(k)
    out = [f"<!doctype html><html><head><meta charset='utf-8'><title>CRISP comparison</title><style>{CSS}</style></head><body>",
           "<h1>CRISP comparison</h1>",
           f"<div class='muted'>teams: {esc(', '.join(teams))} · token counts are tiktoken o200k_base estimates · "
           "judged blind, pairwise vs the shared baseline</div>"]
    out.append("<h2>Prompts</h2><table class='sum'><tr><th>team</th><th>arm</th><th>tokens_est</th><th>text</th></tr>")
    for r in results:
        for arm in ARMS:
            out.append(f"<tr><td>{esc(r['team'])}</td><td>{arm}</td><td>{r['prompts'].get(arm + '_tokens_est')}</td>"
                       f"<td style='text-align:left;white-space:normal;max-width:720px'>{esc(r['prompts'].get(arm))}</td></tr>")
    out.append("</table>")
    for gen, judge in lane_keys:
        members = []
        for r in results:
            lane = next((l for l in r["lanes"] if (l["generator"], l["judge"]) == (gen, judge)), None)
            if lane:
                members.append((r["team"], lane))
        out.append(f"<h2>Generator {esc(gen)} · judge {esc(judge)}</h2>")
        gs = members[0][1].get("generator_settings") or {}
        out.append(f"<div class='muted'>generator settings: {esc(json.dumps(gs))}</div>")
        out.append(summary_tables(members))
        ids = []
        for _, lane in members:
            for t in lane["tests"]:
                if t["id"] not in ids:
                    ids.append(t["id"])
        for tid in ids:
            tests_by_team = {team: next(t for t in lane["tests"] if t["id"] == tid)
                             for team, lane in members if any(t["id"] == tid for t in lane["tests"])}
            out.append(fixture_html(tests_by_team, fixtures))
    out.append("</body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    results = []
    for p in a.results:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        if d.get("schema") != "crisp-bench/v1":
            sys.exit(f"{p}: schema {d.get('schema')!r}, expected crisp-bench/v1")
        results.append(d)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(render(results))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
