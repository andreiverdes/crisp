"""Aggregation over crisp-bench/v1 lanes. Shared by `run.py summary` and `render.py`."""

DIMS = ["correctness", "clarity", "ambiguity", "scanability", "relevance", "conversational", "completeness"]
ARMS = ["crisp", "crispify"]


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pct_reduction(base, arm):
    if not base or arm is None:
        return None
    return (1 - arm / base) * 100


def samples_of(test, arm):
    return (test.get("arms", {}).get(arm) or {}).get("samples") or []


def judgments_of(test, arm):
    return [j for j in test.get("judgments", []) if j["arm"] == arm]


def dim_mean(judgments, side, dim):
    return mean([j["scores"][side][dim] for j in judgments])


def overall(scores):
    return mean([scores[d] for d in DIMS])


def facts_stats(judgments):
    """-> dict(retained, arm_cov, base_cov) as fractions or None."""
    base_present = sum(len(j["facts"]["baseline"]["present"]) for j in judgments)
    arm_present = sum(len(j["facts"]["arm"]["present"]) for j in judgments)
    total = sum(j["facts"]["baseline"]["total"] for j in judgments)
    lost = sum(len(j["facts_lost"]) for j in judgments)
    return {
        "retained": (1 - lost / base_present) if base_present else None,
        "arm_cov": arm_present / total if total else None,
        "base_cov": base_present / total if total else None,
        "lost": lost,
    }


def wtl(judgments):
    """win/tie/loss for the arm."""
    w = sum(1 for j in judgments if j["preferred"] == "arm")
    t = sum(1 for j in judgments if j["preferred"] == "tie")
    l = sum(1 for j in judgments if j["preferred"] == "baseline")
    return w, t, l


def arm_stats(tests, arm):
    """Pool every sample of `arm` across `tests`; compare with the baseline samples of the same tests."""
    used = [t for t in tests if samples_of(t, arm)]
    a = [s for t in used for s in samples_of(t, arm)]
    b = [s for t in used for s in samples_of(t, "baseline")]
    js = [j for t in used for j in judgments_of(t, arm)]
    out = {
        "n": len(a),
        "n_judged": len(js),
        "words": mean([s["words"] for s in a]),
        "tokens": mean([s["tokens_est"] for s in a]),
        "out_tokens": mean([(s.get("usage") or {}).get("output_tokens") for s in a]),
        "in_tokens": mean([(s.get("usage") or {}).get("input_tokens") for s in a]),
        "base_words": mean([s["words"] for s in b]),
        "base_tokens": mean([s["tokens_est"] for s in b]),
        "base_out_tokens": mean([(s.get("usage") or {}).get("output_tokens") for s in b]),
        "base_in_tokens": mean([(s.get("usage") or {}).get("input_tokens") for s in b]),
        "dims_arm": {d: dim_mean(js, "arm", d) for d in DIMS},
        "dims_base": {d: dim_mean(js, "baseline", d) for d in DIMS},
        "facts": facts_stats(js),
        "wtl": wtl(js),
        "useful_lost_arm": sum(1 for j in js if (j.get("useful_lost") or {}).get("arm")),
        "useful_lost_base": sum(1 for j in js if (j.get("useful_lost") or {}).get("baseline")),
    }
    out["red_words"] = pct_reduction(out["base_words"], out["words"])
    out["red_tokens"] = pct_reduction(out["base_tokens"], out["tokens"])
    out["overall_arm"] = mean(list(out["dims_arm"].values())) if js else None
    out["overall_base"] = mean(list(out["dims_base"].values())) if js else None
    return out


def lane_stats(lane):
    return {arm: arm_stats(lane["tests"], arm) for arm in ARMS}


def fmt(x, nd=1, suffix=""):
    return "-" if x is None else f"{x:.{nd}f}{suffix}"
