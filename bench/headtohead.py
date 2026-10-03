#!/usr/bin/env python3
"""Direct blind pairings that the lane results don't contain:

  a) Anthropic /crisp vs OpenAI /crisp on the shared gpt-6-luna lane (30 pairs, judge gpt-6.1-sol)
  b) ASD-STE100 rewrite vs crispify on the sonnet lane (5 pairs, judge opus-5-5)

Writes site/headtohead.json. Reuses the shared rubric and the lane judge settings.
"""
import json, os, random, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
import run as R  # noqa: E402
from gateway import GatewayPool  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
# gpt-6.1-sol (the lane judge) hit its usage limit; Opus 5.5 judges the cross-team pairs. Neither team generated with it.
TEAM_JUDGE = os.environ.get("TEAM_JUDGE", "anthropic/claude-opus-5-5")


def pair(pool, judge, template, fx, left, right, seed):
    """left/right = (name, text). Returns {winner, scores:{name:{...}}, facts:{name:[...]}, notes, order}."""
    rng = random.Random(seed)
    first_left = rng.random() < 0.5
    a, b = (left, right) if first_left else (right, left)
    prompt = R.fill_rubric(template, fx["prompt"], fx["required_facts"], a[1], b[1])
    fact_ids = [f["id"] for f in fx["required_facts"]]
    last = None
    for _ in range(2):
        r = pool.chat(judge, [{"role": "user", "content": prompt}], reasoning_effort="high")
        try:
            d = R.parse_judge_json(r["text"], fact_ids)
            break
        except ValueError as e:
            last = e
    else:
        raise last
    name = {"A": a[0], "B": b[0]}
    pref = str(d["preferred"]).strip().upper()
    winner = "tie" if pref == "TIE" else name[pref]
    return {
        "winner": winner,
        "order": [a[0], b[0]],
        "scores": {name[s]: {k: d[s][k] for k in R.DIMS} for s in ("A", "B")},
        "facts": {name[s]: d[s]["facts_present"] for s in ("A", "B")},
        "useful_lost": {name[s]: d.get("useful_lost", {}).get(s, "") for s in ("A", "B")},
        "notes": d.get("notes", ""),
    }


def main():
    fixtures = {f["id"]: f for f in R.load_fixtures()}
    template = R.rubric_template()
    pool = GatewayPool(6)
    out = {}

    # a) team vs team, shared lane
    ant = R.load_json(os.path.join(R.SHARED, "results", "anthropic.json"))["lanes"][0]
    oai = R.load_json(os.path.join(R.SHARED, "results", "openai.json"))["lanes"][0]
    A = {t["id"]: t["arms"]["crisp"]["samples"] for t in ant["tests"]}
    O = {t["id"]: t["arms"]["crisp"]["samples"] for t in oai["tests"]}
    jobs = []
    for tid in A:
        for i in range(min(len(A[tid]), len(O[tid]))):
            jobs.append((tid, i))
    def do_team(job):
        tid, i = job
        res = pair(pool, TEAM_JUDGE, template, fixtures[tid],
                   ("anthropic", A[tid][i]["text"]), ("openai", O[tid][i]["text"]), f"h2h:{tid}:{i}")
        res.update({"id": tid, "sample": i})
        print("team", tid, i, res["winner"], flush=True)
        return res
    with ThreadPoolExecutor(6) as ex:
        out["team"] = list(ex.map(do_team, jobs))

    # b) STE vs crispify, sonnet lane
    ste = R.load_json(os.path.join(SITE, "data.json"))["ste"]
    def do_ste(r):
        res = pair(pool, "anthropic/claude-opus-5-5", template, fixtures[r["id"]],
                   ("ste", r["steText"]), ("crisp", r["crispText"]), f"ste:{r['id']}")
        res.update({"id": r["id"]})
        print("ste", r["id"], res["winner"], flush=True)
        return res
    with ThreadPoolExecutor(5) as ex:
        out["ste"] = list(ex.map(do_ste, ste))

    out["judges"] = {"team": TEAM_JUDGE, "ste": "anthropic/claude-opus-5-5"}
    with open(os.path.join(SITE, "headtohead.json"), "w") as f:
        json.dump(out, f, indent=1)
    from collections import Counter
    print("team:", Counter(r["winner"] for r in out["team"]))
    print("ste:", Counter(r["winner"] for r in out["ste"]))


if __name__ == "__main__":
    main()
