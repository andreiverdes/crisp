#!/usr/bin/env python3
"""CRISP benchmark runner. Run from any directory with `python runner.py ...`."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import selectors
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "harness"
BASELINE_PATH = ROOT / "baseline" / "gpt-6-luna.json"
GENERATOR = "openai-codex/gpt-6-luna"
JUDGE = "openai-codex/gpt-6.1-sol"
DIMENSIONS = ("correctness", "clarity", "ambiguity", "scanability", "relevance", "conversational", "completeness")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def normalize_result(result):
    for lane in result.get("lanes", []):
        tests = lane.get("tests", {})
        if isinstance(tests, list):
            lane["tests"] = {test["id"]: {k: v for k, v in test.items() if k != "id"} for test in tests}
        elif not isinstance(tests, dict):
            raise ValueError("result lane tests must be an array or object")
    return result


def result_for_disk(result):
    lanes = [{**lane, "tests": [{"id": fid, **test} for fid, test in lane["tests"].items()]}
             for lane in result["lanes"]]
    return {**result, "lanes": lanes}


def write_result(path, result):
    write_json(path, result_for_disk(result))


def fixtures():
    source = read_json(ROOT / "fixtures.json")
    return [f for scenario in source["scenarios"] for f in scenario["fixtures"]]


def count_tokens(text):
    try:
        import tiktoken
    except ImportError as exc:
        raise RuntimeError("Install requirements.txt first (tiktoken is required for tokens_est)") from exc
    return len(tiktoken.get_encoding("o200k_base").encode(text))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(team=None):
    paths = [ROOT / "fixtures.json", ROOT / "rubric.md"]
    if team:
        paths += [ROOT / "prompts" / team / "crisp.md", ROOT / "prompts" / team / "crispify.md"]
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def team_manifest(team):
    return {"inputs": manifest(team), "baseline_sha256": sha(BASELINE_PATH),
            "generator": GENERATOR, "judge": JUDGE, "generator_reasoning": "low",
            "judge_reasoning": "high", "temperature": None, "samples_per_fixture": 3}


def freeze(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        previous = read_json(path)
        if previous != content:
            raise RuntimeError(f"Frozen inputs/settings drift detected in {path}; use a new output location for a new benchmark")
    else:
        write_json(path, content)




def gateway(request, timeout=300):
    executable = shutil.which("omp")
    if not executable:
        raise RuntimeError("omp executable not found on PATH")
    proc = subprocess.Popen([executable, "auth-gateway", "stdio"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(proc.stdout, selectors.EVENT_READ)
            ready = _readline(selector, timeout)
            try:
                ready_obj = json.loads(ready)
            except Exception as exc:
                raise RuntimeError("auth-gateway returned a non-JSON ready line") from exc
            if not isinstance(ready_obj, dict):
                raise RuntimeError("auth-gateway did not return a ready JSON object")
            proc.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
            proc.stdin.flush()
            line = _readline(selector, timeout)
            try:
                response = json.loads(line)
            except Exception as exc:
                raise RuntimeError("auth-gateway returned a non-JSON response line") from exc
        if response.get("id") != request["id"] or response.get("status") != 200:
            raise RuntimeError(f"auth-gateway request failed (status={response.get('status')!r})")
        body = response.get("body") or {}
        choices = body.get("choices") or []
        if not choices or not isinstance(choices[0].get("message", {}).get("content"), str):
            raise RuntimeError("auth-gateway response has no message content")
        text = choices[0]["message"]["content"]
        if not text.strip() or choices[0].get("finish_reason") != "stop":
            raise RuntimeError(f"Generation was empty or incomplete (finish_reason={choices[0].get('finish_reason')!r})")
        return text, body.get("usage") or {}, choices[0].get("finish_reason")
    finally:
        if proc.poll() is None:
            proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def _readline(selector, timeout):
    if not selector.select(timeout):
        raise TimeoutError(f"auth-gateway timed out after {timeout}s")
    line = selector.get_map().values().__iter__().__next__().fileobj.readline()
    if not line:
        raise RuntimeError("auth-gateway closed stdout before replying")
    return line


def usage_record(usage):
    # Normalize the provider's prompt/completion vocabulary to the shared schema.
    def get(*keys):
        for key in keys:
            if usage.get(key) is not None:
                return usage[key]
        return None
    details = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
    completion_details = usage.get("completion_tokens_details") or {}
    normalized = {"input_tokens": get("input_tokens", "prompt_tokens"),
                  "output_tokens": get("output_tokens", "completion_tokens"),
                  "reasoning_tokens": get("reasoning_tokens") if get("reasoning_tokens") is not None else completion_details.get("reasoning_tokens")}
    cached = details.get("cached_tokens")
    if cached is not None:
        normalized["cached_input_tokens"] = cached
    return normalized


def sample(index, text, usage, latency, source_sample=None):
    result = {"index": index, "text": text, "words": len(text.split()), "tokens_est": count_tokens(text),
              "usage": usage_record(usage), "latency_ms": latency}
    if source_sample is not None:
        result["source_sample"] = source_sample
    return result


def request(model, effort, messages, reqid):
    return {"id": reqid, "path": "/v1/chat/completions", "body": {"model": model, "messages": messages,
            "reasoning_effort": effort, "stream": False}}


def run_one(req, index, source_sample=None):
    started = time.monotonic()
    text, usage, finish = gateway(req)
    return sample(index, text, usage, round((time.monotonic() - started) * 1000), source_sample), {
        "request": req, "response": {"status": 200, "finish_reason": finish, "text": text, "usage": usage}}


def parallel_jobs(jobs, workers, callback):
    errors = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_one, req, idx, src): (fixture_id, arm, idx) for fixture_id, arm, idx, src, req in jobs}
        for future in as_completed(futures):
            fixture_id, arm, idx = futures[future]
            try:
                value, raw = future.result()
                callback(fixture_id, arm, idx, value, raw)
            except Exception as exc:
                errors.append(f"{fixture_id}/{arm}/{idx}: {type(exc).__name__}: {exc}")
    if errors:
        raise RuntimeError("One or more samples failed; successful samples were saved and can be resumed:\n" + "\n".join(errors))


def ensure_fixture_tests(tests):
    for f in fixtures():
        tests.setdefault(f["id"], {"arms": {"baseline": {"samples": []}, "crisp": {"samples": []}, "crispify": {"samples": []}}, "judgments": []})
        for arm in ("baseline", "crisp", "crispify"):
            tests[f["id"]]["arms"].setdefault(arm, {"samples": []})
            tests[f["id"]]["arms"][arm].setdefault("samples", [])


def baseline_stage(workers):
    baseline_path = BASELINE_PATH
    freeze(HARNESS / "baseline.freeze.json", {"inputs": manifest(), "generator": GENERATOR, "reasoning": "low", "temperature": None, "samples_per_fixture": 3})
    if baseline_path.exists():
        doc = read_json(baseline_path)
        if doc.get("schema") != "crisp-bench/baseline-v1" or doc.get("generator") != GENERATOR:
            raise RuntimeError(f"Existing baseline has incompatible metadata: {baseline_path}")
    else:
        doc = {"schema": "crisp-bench/baseline-v1", "generator": GENERATOR,
               "generator_settings": {"reasoning": "low", "temperature": None},
               "generated_at": datetime.now(timezone.utc).isoformat(), "tests": {}}
    jobs = []
    for f in fixtures():
        samples = doc["tests"].setdefault(f["id"], {}).setdefault("samples", [])
        existing = {s["index"] for s in samples}
        for idx in range(3):
            if idx not in existing:
                rid = f"base-{f['id']}-{idx}"
                jobs.append((f["id"], "baseline", idx, None,
                             request(GENERATOR, "low", [{"role": "user", "content": f["prompt"]}], rid)))
    def save(fid, arm, idx, value, raw):
        rows = doc["tests"][fid]["samples"]
        rows[:] = [s for s in rows if s["index"] != idx]
        rows.append(value); rows.sort(key=lambda s: s["index"])
        write_json(HARNESS / "raw" / "baseline" / f"{fid}-{idx}.json", raw)
        write_json(baseline_path, doc)
    parallel_jobs(jobs, workers, save)
    return doc


def team_stage(team, workers):
    prompt_files = {arm: ROOT / "prompts" / team / ("crisp.md" if arm == "crisp" else "crispify.md") for arm in ("crisp", "crispify")}
    prompts = {arm: path.read_text(encoding="utf-8") for arm, path in prompt_files.items()}
    result_path = ROOT / "results" / f"{team}.json"
    baseline = read_json(BASELINE_PATH)
    freeze(HARNESS / f"{team}.freeze.json", team_manifest(team))
    if result_path.exists():
        result = normalize_result(read_json(result_path))
        if result.get("team") != team or not result.get("lanes") or result["lanes"][0].get("generator") != GENERATOR:
            raise RuntimeError(f"Existing result has incompatible metadata: {result_path}")
    else:
        result = {"schema": "crisp-bench/v1", "team": team, "generated_at": datetime.now(timezone.utc).isoformat(),
                  "prompts": {arm: prompts[arm] for arm in prompts},
                  "lanes": [{"generator": GENERATOR, "generator_settings": {"reasoning": "low", "temperature": None},
                             "judge": JUDGE, "tokenizer_est": "tiktoken/o200k_base",
                             "baseline_file": "baseline/gpt-6-luna.json", "tests": {}}]}
    lane = result["lanes"][0]
    ensure_fixture_tests(lane["tests"])
    for arm, text in prompts.items():
        result["prompts"][arm] = text
        result["prompts"][arm + "_tokens_est"] = count_tokens(text)
    jobs = []
    for f in fixtures():
        target = lane["tests"][f["id"]]["arms"]
        base_rows = baseline["tests"][f["id"]]["samples"]
        for idx in range(3):
            for arm in ("crisp", "crispify"):
                if any(s["index"] == idx for s in target[arm]["samples"]):
                    continue
                user = f["prompt"] if arm == "crisp" else "Crispify this:\n\n" + next(s["text"] for s in base_rows if s["index"] == idx)
                messages = [{"role": "system", "content": prompts[arm]}, {"role": "user", "content": user}]
                jobs.append((f["id"], arm, idx, idx if arm == "crispify" else None,
                             request(GENERATOR, "low", messages, f"{team}-{arm}-{f['id']}-{idx}")))
    def save(fid, arm, idx, value, raw):
        rows = lane["tests"][fid]["arms"][arm]["samples"]
        rows[:] = [s for s in rows if s["index"] != idx]
        rows.append(value); rows.sort(key=lambda s: s["index"])
        write_json(HARNESS / "raw" / team / f"{fid}-{arm}-{idx}.json", raw)
        write_result(result_path, result)
    for f in fixtures():
        lane["tests"][f["id"]]["arms"]["baseline"]["samples"] = sorted(
            baseline["tests"][f["id"]]["samples"], key=lambda s: s["index"])
    for f in fixtures():
        for arm in ("crisp", "crispify"):
            lane["tests"][f["id"]]["arms"][arm]["samples"].sort(key=lambda s: s["index"])
    write_result(result_path, result)
    parallel_jobs(jobs, workers, save)


def parse_judge(text):
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S | re.I)
    candidate = match.group(1) if match else text[text.find("{"):text.rfind("}") + 1]
    if not candidate: raise ValueError("no JSON object in judge response")
    data = json.loads(candidate)
    if not all(k in data for k in ("A", "B", "useful_lost", "preferred", "notes")):
        raise ValueError("judge JSON missing required keys")
    for side in ("A", "B"):
        row = data[side]
        for dim in DIMENSIONS:
            score = row.get(dim)
            if type(score) is not int or not 1 <= score <= 5: raise ValueError(f"invalid {side}.{dim} score")
        if not isinstance(row.get("facts_present"), list): raise ValueError(f"invalid {side}.facts_present")
    if data["preferred"] not in ("A", "B", "tie"): raise ValueError("invalid preferred value")
    if not isinstance(data["useful_lost"], dict) or not isinstance(data["notes"], str): raise ValueError("invalid judge annotations")
    return data


def judge_stage(team, seed):
    generation_freeze = HARNESS / f"{team}.freeze.json"
    if not generation_freeze.exists():
        raise RuntimeError("Generate this team's samples before judging")
    freeze(generation_freeze, team_manifest(team))
    freeze(HARNESS / f"{team}.judge.freeze.json", {"inputs": manifest(team), "judge": JUDGE, "reasoning": "high", "seed": seed})
    rubric = (ROOT / "rubric.md").read_text(encoding="utf-8").split("\n---\n", 1)[1].strip()
    result_path = ROOT / "results" / f"{team}.json"
    result = normalize_result(read_json(result_path))
    lane = result["lanes"][0]
    byid = {f["id"]: f for f in fixtures()}
    jobs = []
    for fid, fixture in byid.items():
        test = lane["tests"][fid]
        for arm in ("crisp", "crispify"):
            done = {(j["arm"], j["sample"]) for j in test["judgments"]}
            for idx in range(3):
                if (arm, idx) in done: continue
                baseline = next(s for s in test["arms"]["baseline"]["samples"] if s["index"] == idx)
                answer = next(s for s in test["arms"][arm]["samples"] if s["index"] == idx)
                rng = random.Random(f"{seed}:{team}:{fid}:{arm}:{idx}")
                order = "baseline_first" if rng.randrange(2) == 0 else "arm_first"
                a, b = (baseline["text"], answer["text"]) if order == "baseline_first" else (answer["text"], baseline["text"])
                facts = "\n".join(f"{x['id']}: {x['text']}" for x in fixture["required_facts"])
                content = rubric.replace("{{prompt}}", fixture["prompt"]).replace("{{required_facts_list}}", facts).replace("{{answer_a}}", a).replace("{{answer_b}}", b)
                rid = f"judge-{team}-{fid}-{arm}-{idx}"
                req = request(JUDGE, "high", [{"role": "user", "content": content}], rid)
                jobs.append((fid, arm, idx, order, req, baseline, answer, fixture))
    failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(run_one, item[4], item[2], None): item for item in jobs}
        for future in as_completed(futures):
            fid, arm, idx, order, req, baseline, answer, fixture = futures[future]
            try:
                value, raw = future.result()
                raw_path = HARNESS / "raw" / team / f"{fid}-{arm}-judge-{idx}.json"
                write_json(raw_path, raw)
                parsed = parse_judge(value["text"])
                valid_ids = {f["id"] for f in fixture["required_facts"]}
                if any(not set(parsed[side]["facts_present"]).issubset(valid_ids) for side in ("A", "B")):
                    raise ValueError("judge returned unknown required-fact ID")
                if not isinstance(parsed["useful_lost"].get("A"), str) or not isinstance(parsed["useful_lost"].get("B"), str):
                    raise ValueError("invalid useful_lost values")
                baseline_side, arm_side = ("A", "B") if order == "baseline_first" else ("B", "A")
                arm_score = {dim: parsed[arm_side][dim] for dim in DIMENSIONS}
                baseline_score = {dim: parsed[baseline_side][dim] for dim in DIMENSIONS}
                facts_b = set(parsed[baseline_side]["facts_present"]); facts_a = set(parsed[arm_side]["facts_present"])
                preferred = "tie" if parsed["preferred"] == "tie" else ("baseline" if parsed["preferred"] == baseline_side else "arm")
                judgement = {"arm": arm, "sample": idx, "baseline_sample": idx, "order": order,
                    "judge": JUDGE, "scores": {"baseline": baseline_score, "arm": arm_score},
                    "facts": {"baseline": {"present": sorted(facts_b), "total": len(valid_ids)},
                              "arm": {"present": sorted(facts_a), "total": len(valid_ids)}},
                    "facts_lost": sorted(facts_b - facts_a),
                    "useful_lost": {"baseline": parsed["useful_lost"].get(baseline_side, ""), "arm": parsed["useful_lost"].get(arm_side, "")},
                    "preferred": preferred, "notes": parsed["notes"], "judge_latency_ms": value["latency_ms"], "seed": seed}
                test = lane["tests"][fid]
                test["judgments"] = [j for j in test["judgments"] if not (j["arm"] == arm and j["sample"] == idx)]
                test["judgments"].append(judgement); test["judgments"].sort(key=lambda j: (j["arm"], j["sample"]))
                raw["parsed"] = parsed
                write_json(raw_path, raw)
                write_result(result_path, result)
            except Exception as exc:
                failures.append(f"{fid}/{arm}/{idx}: {type(exc).__name__}: {exc}")
    if failures:
        raise RuntimeError("Judge failures; successful judgments were saved and can be resumed:\n" + "\n".join(failures))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="stage", required=True)
    for name in ("baseline", "team"):
        sub = subs.add_parser(name); sub.add_argument("--workers", type=int, default=4)
        if name == "team": sub.add_argument("team", choices=("openai", "anthropic"))
    sub = subs.add_parser("judge"); sub.add_argument("team", choices=("openai", "anthropic")); sub.add_argument("--seed", type=int, default=211)
    args = parser.parse_args()
    try:
        if args.stage == "baseline": baseline_stage(args.workers)
        elif args.stage == "team": team_stage(args.team, args.workers)
        else: judge_stage(args.team, args.seed)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); raise SystemExit(1)

if __name__ == "__main__": main()
