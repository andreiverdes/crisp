#!/usr/bin/env python3
"""Build site/data.json from the result files. Rerun after new results; then `python3 site/build.py`."""
import json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHARED = os.path.join(ROOT, "shared") if os.path.isdir(os.path.join(ROOT, "shared")) else os.path.join(os.path.dirname(ROOT), "shared")
sys.path.insert(0, os.path.join(ROOT, "bench"))
from count import words, tokens_est  # noqa: E402

DIMS = ["correctness", "clarity", "ambiguity", "scanability", "relevance", "conversational", "completeness"]


def load(p):
    with open(p) as f:
        return json.load(f)


def lane(p):
    return load(p)["lanes"][0]


def arm_stats(l, arm):
    W = T = L = 0; fp = ft = bfp = 0; bw = bt = aw = at = 0; n = 0
    dims = Counter(); bdims = Counter(); nj = 0; per = []; lost = Counter()
    for t in l["tests"]:
        bs = t["arms"]["baseline"]["samples"]; as_ = t["arms"][arm]["samples"]
        tb = sum(s["words"] for s in bs); ta = sum(s["words"] for s in as_)
        tbt = sum(s["tokens_est"] for s in bs); tat = sum(s["tokens_est"] for s in as_)
        bw += tb; bt += tbt; aw += ta; at += tat; n += len(bs)
        js = [j for j in t["judgments"] if j["arm"] == arm]
        c = Counter(j["preferred"] for j in js)
        d = {k: 0 for k in DIMS}; bd = {k: 0 for k in DIMS}
        for j in js:
            nj += 1; W += j["preferred"] == "arm"; T += j["preferred"] == "tie"; L += j["preferred"] == "baseline"
            fp += len(j["facts"]["arm"]["present"]); ft += j["facts"]["arm"]["total"]; bfp += len(j["facts"]["baseline"]["present"])
            for k in DIMS:
                dims[k] += j["scores"]["arm"][k]; bdims[k] += j["scores"]["baseline"][k]; d[k] += j["scores"]["arm"][k]; bd[k] += j["scores"]["baseline"][k]
            for f in j["facts_lost"]: lost[f"{t['id']}:{f}"] += 1
        per.append({"id": t["id"], "baseWords": round(tb / len(bs)), "armWords": round(ta / len(as_)), "baseTok": round(tbt / len(bs)), "armTok": round(tat / len(as_)),
                    "w": c["arm"], "t": c["tie"], "l": c["baseline"],
                    "overall": round(sum(d.values()) / (7 * max(1, len(js))), 2), "baseOverall": round(sum(bd.values()) / (7 * max(1, len(js))), 2),
                    "factsLost": sorted({f for j in js for f in j["facts_lost"]}),
                    "samples": [{"index": s["index"], "text": s["text"], "words": s["words"], "tokens": s["tokens_est"],
                                 "judge": next(({"preferred": j["preferred"], "notes": j["notes"], "scores": j["scores"]["arm"], "baseScores": j["scores"]["baseline"],
                                                 "factsLost": j["facts_lost"], "usefulLost": j["useful_lost"]} for j in js if j["sample"] == s["index"]), None)}
                                for s in as_]})
    return {"wins": W, "ties": T, "losses": L, "factsKept": round(100 * fp / ft, 1), "baseFacts": round(100 * bfp / ft, 1),
            "baseWords": round(bw / n), "armWords": round(aw / n), "baseTok": round(bt / n), "armTok": round(at / n),
            "wordsPct": round(100 * (1 - aw / bw), 1), "tokPct": round(100 * (1 - at / bt), 1),
            "dims": {k: {"base": round(bdims[k] / nj, 2), "arm": round(dims[k] / nj, 2)} for k in DIMS},
            "perFixture": per, "mostLost": lost.most_common(5)}


def baseline_samples(l):
    return {t["id"]: [{"index": s["index"], "text": s["text"], "words": s["words"], "tokens": s["tokens_est"]} for s in t["arms"]["baseline"]["samples"]] for t in l["tests"]}


def main():
    lanes = []
    for label, p in [("Claude Sonnet 5.5 · judge Opus 5.5 · v1 prompt (shipped)", os.path.join(ROOT, "bench/out/v1/results.json")),
                     ("Claude Sonnet 5.5 · judge Opus 5.5 · v2 prompt", os.path.join(SHARED, "results/anthropic-sonnet.json")),
                     ("GPT-6 Luna · judge GPT-6.1 Sol · shared lane, Anthropic prompt", os.path.join(SHARED, "results/anthropic.json")),
                     ("GPT-6 Luna · judge GPT-6.1 Sol · shared lane, OpenAI prompt", os.path.join(SHARED, "results/openai.json"))]:
        l = lane(p)
        lanes.append({"label": label, "generator": l["generator"], "judge": l["judge"], "crisp": arm_stats(l, "crisp"), "crispify": arm_stats(l, "crispify"), "baselineSamples": baseline_samples(l)})
    fx = load(os.path.join(SHARED, "fixtures.json"))
    fixtures = {f["id"]: {"title": s["title"], "prompt": f["prompt"], "facts": f["required_facts"]} for s in fx["scenarios"] for f in s["fixtures"]}
    old = load(os.path.join(HERE, "data.json")) if os.path.exists(os.path.join(HERE, "data.json")) else {}
    ste = old.get("ste")  # probe output persisted from the first build; see session log
    if not ste:
        sys.exit("site/data.json has no 'ste' block; run the STE probe first")
    h2h = load(os.path.join(HERE, "headtohead.json")) if os.path.exists(os.path.join(HERE, "headtohead.json")) else None
    a = load(os.path.join(SHARED, "results/anthropic.json")); o = load(os.path.join(SHARED, "results/openai.json"))
    data = {"generatedAt": "2026-10-04", "lanes": lanes, "fixtures": fixtures, "ste": ste, "headtohead": h2h,
            "prompts": {"crisp": a["prompts"]["crisp"], "crispTokens": a["prompts"]["crisp_tokens_est"],
                        "openaiCrisp": o["prompts"]["crisp"], "openaiCrispTokens": o["prompts"]["crisp_tokens_est"],
                        "shipped": open(os.path.join(ROOT, "skills/crisp/prompts/crisp.md")).read().strip()}}
    with open(os.path.join(HERE, "data.json"), "w") as f:
        json.dump(data, f, indent=1)
    print("data.json:", os.path.getsize(os.path.join(HERE, "data.json")) // 1024, "KB; h2h:", bool(h2h))


if __name__ == "__main__":
    main()
