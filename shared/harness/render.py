#!/usr/bin/env python3
"""Render schema-compatible CRISP result files as an offline comparison report."""
import argparse
import html
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIMS = ("correctness", "clarity", "ambiguity", "scanability", "relevance", "conversational", "completeness")
ARMS = ("crisp", "crispify")


def load_fixtures(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    return {f["id"]: {**f, "scenario": s["title"]} for s in doc["scenarios"] for f in s["fixtures"]}


def esc(value):
    return html.escape(str(value), quote=True)


def mean(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return sum(values) / len(values) if values else None


def fmt(value, digits=1):
    return "unavailable" if value is None else f"{value:.{digits}f}"


def safe_json(data):
    return json.dumps(data, ensure_ascii=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def collect(results, fixtures):
    lanes = defaultdict(list)
    for result in results:
        team = result["team"]
        for lane in result.get("lanes", []):
            key = (lane.get("generator", "unknown"), lane.get("judge", "unknown"))
            tests = lane.get("tests", {})
            if isinstance(tests, list):
                tests = {test["id"]: test for test in tests}
            lanes[key].append((team, {**lane, "tests": tests, "prompts": result.get("prompts", {})}))
    return lanes


def stat_row(team, tests):
    output = {"team": team, "arms": {}}
    for arm in ARMS:
        metrics = defaultdict(list)
        scores = defaultdict(list)
        baseline_scores = defaultdict(list)
        retention = []
        wins = defaultdict(list)
        facts = []
        for test in tests.values():
            baseline = {s["index"]: s for s in test.get("arms", {}).get("baseline", {}).get("samples", [])}
            samples = {s["index"]: s for s in test.get("arms", {}).get(arm, {}).get("samples", [])}
            judgements = {j["sample"]: j for j in test.get("judgments", []) if j.get("arm") == arm}
            for idx, sample in samples.items():
                base = baseline.get(idx, {})
                for key in ("words", "tokens_est"):
                    if isinstance(sample.get(key), (int, float)): metrics[f"arm_{key}"].append(sample[key])
                    if isinstance(base.get(key), (int, float)): metrics[f"base_{key}"].append(base[key])
                arm_usage, base_usage = sample.get("usage") or {}, base.get("usage") or {}
                for key in ("input_tokens", "output_tokens"):
                    av, bv = arm_usage.get(key), base_usage.get(key)
                    if isinstance(av, (int, float)): metrics[f"arm_{key}"].append(av)
                    if isinstance(bv, (int, float)): metrics[f"base_{key}"].append(bv)
                if all(isinstance(x, (int, float)) for x in (arm_usage.get("input_tokens"), arm_usage.get("output_tokens"))):
                    metrics["arm_io_total"].append(arm_usage["input_tokens"] + arm_usage["output_tokens"])
                if all(isinstance(x, (int, float)) for x in (base_usage.get("input_tokens"), base_usage.get("output_tokens"))):
                    metrics["base_io_total"].append(base_usage["input_tokens"] + base_usage["output_tokens"])
                j = judgements.get(idx)
                if j:
                    for dim in DIMS:
                        scores[dim].append(j.get("scores", {}).get("arm", {}).get(dim))
                        baseline_scores[dim].append(j.get("scores", {}).get("baseline", {}).get(dim))
                    fact_record = j.get("facts", {}).get("arm", {})
                    if fact_record.get("total"):
                        facts.append(len(fact_record.get("present", [])) / fact_record["total"])
                    source_facts = set(j.get("facts", {}).get("baseline", {}).get("present", []))
                    if source_facts:
                        retention.append(len(source_facts & set(fact_record.get("present", []))) / len(source_facts))
                    wins[j.get("preferred", "tie")].append(1)
        vals = {k: mean(v) for k, v in metrics.items()}
        def reduction(a, b):
            x, y = vals.get(a), vals.get(b)
            return 100 * (x - y) / x if x not in (None, 0) and y is not None else None
        output["arms"][arm] = {
            "mean_words": vals.get("arm_words"), "word_reduction_pct": reduction("base_words", "arm_words"),
            "mean_tokens_est": vals.get("arm_tokens_est"), "token_reduction_pct": reduction("base_tokens_est", "arm_tokens_est"),
            "mean_provider_input": vals.get("arm_input_tokens"), "provider_input_delta": (vals.get("arm_input_tokens") - vals.get("base_input_tokens")) if vals.get("arm_input_tokens") is not None and vals.get("base_input_tokens") is not None else None,
            "mean_provider_output": vals.get("arm_output_tokens"), "provider_output_delta": (vals.get("arm_output_tokens") - vals.get("base_output_tokens")) if vals.get("arm_output_tokens") is not None and vals.get("base_output_tokens") is not None else None,
            "total_io_delta": (vals.get("arm_io_total") - vals.get("base_io_total")) if vals.get("arm_io_total") is not None and vals.get("base_io_total") is not None else None,
            "mean_base_io": vals.get("base_io_total"), "mean_arm_io": vals.get("arm_io_total"),
            "facts_coverage_pct": 100 * mean(facts) if facts else None,
            "facts_retained_pct": 100 * mean(retention) if retention else None,
            "baseline_scores": {d: mean(baseline_scores[d]) for d in DIMS},
            "scores": {d: mean(scores[d]) for d in DIMS}, "wins": len(wins["arm"]), "losses": len(wins["baseline"]), "ties": len(wins["tie"])}
    return output


def report_data(results, fixtures):
    grouped = collect(results, fixtures)
    lanes_out = []
    for (generator, judge), teams in grouped.items():
        lanes_out.append({"generator": generator, "judge": judge, "teams": [
            {"team": team, "prompts": lane.get("prompts", {}), "summary": stat_row(team, lane.get("tests", {})),
             "tests": lane.get("tests", {})} for team, lane in teams]})
    lanes_out.sort(key=lambda x: (x["generator"] != "openai-codex/gpt-6-luna", x["judge"] != "openai-codex/gpt-6.1-sol", x["generator"], x["judge"]))
    return {"fixtures": fixtures, "lanes": lanes_out}

def fixture_summary_html(lane, fixtures):
    rows = []
    for team in lane["teams"]:
        for fid, fixture in fixtures.items():
            test = team["tests"].get(fid, {})
            base = {s["index"]: s for s in test.get("arms", {}).get("baseline", {}).get("samples", [])}
            for arm in ARMS:
                paired = {key: [] for key in ("words", "tokens_est")}
                for sample in test.get("arms", {}).get(arm, {}).get("samples", []):
                    original = base.get(sample["index"], {})
                    for key in paired:
                        if isinstance(original.get(key), (int, float)) and original[key] != 0 and isinstance(sample.get(key), (int, float)):
                            paired[key].append(100 * (original[key] - sample[key]) / original[key])
                values = []
                for key in ("words", "tokens_est"):
                    series = paired[key]
                    values.append("unavailable" if not series else f"{mean(series):.1f}% ({min(series):.1f}–{max(series):.1f})")
                rows.append(f"<tr><th>{esc(team['team'])} / {esc(arm)}</th><td>{esc(fid)} — {esc(fixture['scenario'])}</td><td>{values[0]}</td><td>{values[1]}</td></tr>")
    return f'<h3>Per-fixture paired reductions (mean and sample range, n ≤ 3)</h3><div class="tablewrap"><table><thead><tr><th>Arm</th><th>Fixture</th><th>Word reduction</th><th>Text-token estimate reduction</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'



def summary_html(lane, fixtures):
    rows, quality_rows, usage_rows = [], [], []
    def table(headers, body):
        heads = "".join(f"<th>{esc(t)}</th>" for t in headers)
        return f'<div class="tablewrap"><table><thead><tr>{heads}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
    for team in lane["teams"]:
        for arm in ARMS:
            m = team["summary"]["arms"][arm]
            label = f"<th>{esc(team['team'])} / {esc(arm)}</th>"
            pipeline = (m["mean_base_io"] + m["mean_arm_io"]) if arm == "crispify" and m["mean_base_io"] is not None and m["mean_arm_io"] is not None else m["mean_arm_io"]
            rows.append(f"<tr>{label}<td>{fmt(m['mean_words'])}</td><td>{fmt(m['word_reduction_pct'])}%</td><td>{fmt(m['mean_tokens_est'])}</td><td>{fmt(m['token_reduction_pct'])}%</td><td>{fmt(m['facts_coverage_pct'])}%</td><td>{fmt(m['facts_retained_pct'])}%</td><td>{m['wins']} / {m['losses']} / {m['ties']}</td></tr>")
            cells = "".join(f"<td>{fmt(m['scores'][d])} ({fmt(m['baseline_scores'][d])})</td>" for d in DIMS)
            quality_rows.append(f"<tr>{label}{cells}</tr>")
            values = [m["mean_base_io"], m["mean_provider_input"], m["provider_input_delta"], m["mean_provider_output"], m["mean_arm_io"], m["total_io_delta"], pipeline]
            usage_rows.append(f"<tr>{label}{''.join(f'<td>{fmt(v)}</td>' for v in values)}</tr>")
    summary = table(("Arm", "Mean words", "Word reduction", "Text token est.", "Estimate reduction", "Required facts covered", "Baseline facts retained", "W / L / tie"), rows)
    quality = table(("Arm", *DIMS), quality_rows)
    usage = table(("Arm", "Baseline total", "Call input", "Input Δ", "Call output", "Call total", "Call Δ vs baseline", "Pipeline total"), usage_rows)
    baseline = [sample for test in lane["teams"][0]["tests"].values() for sample in test.get("arms", {}).get("baseline", {}).get("samples", [])]
    baseline_words = mean([s.get("words") for s in baseline])
    baseline_tokens = mean([s.get("tokens_est") for s in baseline])
    primary = lane["generator"] == "openai-codex/gpt-6-luna"
    disclosure = "Primary head-to-head: both independently frozen protocols use the identical baseline." if len(lane["teams"]) > 1 else "Supplementary single-team lane; not a head-to-head comparison or evidence of a winner."
    prompt_rows = []
    for team in lane["teams"]:
        p = team["prompts"]
        prompt_rows.append(f"<li>{esc(team['team'])}: direct {esc(p.get('crisp_tokens_est', 'unavailable'))}, rewrite {esc(p.get('crispify_tokens_est', 'unavailable'))} estimated instruction tokens.<details><summary>Frozen instructions</summary><h4>Direct</h4><pre class='answer'>{esc(p.get('crisp', 'unavailable'))}</pre><h4>Rewrite</h4><pre class='answer'>{esc(p.get('crispify', 'unavailable'))}</pre></details></li>")
    fixture_nav = "".join(f'<option value="{esc(fid)}">{esc(fixtures[fid]["scenario"])} — {esc(fid)}</option>' for fid in fixtures)
    return f'''<section class="lane"><h2>Generator: {esc(lane['generator'])} <span>· Judge: {esc(lane['judge'])}</span></h2>
    <p>{disclosure} Baseline: {len(baseline)} samples, mean {fmt(baseline_words)} words / {fmt(baseline_tokens)} estimated text tokens. Baseline was not forced to be verbose.</p>
    <p class="note">Positive reduction means shorter, not better. Required-fact coverage measures the whole checklist; retention measures only facts present in each paired baseline. W/L/tie is against baseline, not the other team.</p>
    {summary}
    <details><summary>Quality scores — arm (paired baseline)</summary>{quality}<p class="note">All dimensions are 1–5, higher is better. Assessments are model judgments, not human comprehension measurements.</p></details>
    <details><summary>Provider usage and full pipeline overhead</summary>{usage}<p class="note">Provider output may include reasoning; missing usage stays unavailable. Pipeline total includes baseline generation plus rewrite for crispify, only the direct call for crisp. Judge calls are evaluation overhead, excluded here. Usage is not price: input, output and cache rates differ. Text estimates use o200k_base, not the provider's exact tokenizer.</p></details>
    <details><summary>Per-fixture reduction ranges</summary>{fixture_summary_html(lane, fixtures)}</details>
    <details><summary>Frozen prompts and instruction overhead</summary><ul>{''.join(prompt_rows)}</ul></details>
    <p class="note">{'Primary generator and judge are from the same model family; blind ordering does not remove family or preference bias.' if primary else 'Supplementary results were supplied by the competing team with a different generator and judge. Do not pool them with the primary lane.'}</p>
    <div class="inspect"><h3>Inspect answers</h3><label>Fixture <select class="fixture-select">{fixture_nav}</select></label><label>Sample <select class="sample-select"><option value="0">Sample 1</option><option value="1">Sample 2</option><option value="2">Sample 3</option></select></label><div class="fixture-context"></div><div class="answers"></div></div></section>'''


def page(data, output):
    lane_blocks = "".join(summary_html(lane, data["fixtures"]) for lane in data["lanes"])
    payload = safe_json(data)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CRISP benchmark comparison</title>
<style>
:root{{font:15px/1.5 system-ui,-apple-system,sans-serif;color:#17212b;background:#f4f6f8}}body{{margin:0}}main{{max-width:1600px;margin:auto;padding:clamp(14px,3vw,34px)}}h1{{margin:.2em 0}}h2{{font-size:1.3rem}}h2 span{{font-size:.9em;color:#526171}}.lede,.note{{color:#526171}}.lane{{background:white;border:1px solid #d8e0e7;border-radius:12px;padding:18px;margin:24px 0;box-shadow:0 2px 10px #1020300a}}.tablewrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;min-width:1050px}}th,td{{text-align:left;padding:9px;border-bottom:1px solid #e6ebef;vertical-align:top}}thead{{background:#eef3f7}}tbody th{{white-space:nowrap}}.inspect{{margin-top:24px}}label{{display:inline-flex;gap:8px;align-items:center;margin:4px 18px 12px 0}}select{{padding:7px;border:1px solid #aab7c3;border-radius:6px}}.answers{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:14px}}.card{{border:1px solid #d6dfe7;border-radius:9px;padding:14px;min-width:0}}.card h4{{margin:0 0 8px}}.answer{{white-space:pre-wrap;overflow-wrap:anywhere;max-height:480px;overflow:auto;background:#f8fafb;padding:12px;border-radius:6px}}.meta{{font-size:.9em;color:#526171}}.loss{{color:#982b20}}.scorelist{{display:flex;gap:8px;flex-wrap:wrap}}.scorelist span{{background:#edf2f6;border-radius:4px;padding:2px 6px}}@media(max-width:600px){{main{{padding:12px}}.lane{{padding:12px}}label{{display:flex}}}}
select{{min-width:0;max-width:100%}}@media(max-width:600px){{label{{flex-wrap:wrap}}.fixture-select{{width:100%}}}}
</style></head><body><main><h1>CRISP benchmark comparison</h1><p class="lede">Paired generation samples and blind judge assessments. Small n (three samples per fixture); judge scores reflect one model judge and are not ground truth. No automatic winner is selected: review content and trade-offs, not token counts alone.</p>{lane_blocks}<footer class="note">Generated offline from crisp-bench/v1 results. All samples and judge notes remain inspectable below each lane.</footer></main>
<script type="application/json" id="bench-data">{payload}</script><script>
(() => {{
  const data = JSON.parse(document.getElementById('bench-data').textContent);
  document.querySelectorAll('.lane').forEach((section, laneIndex) => {{
    const lane = data.lanes[laneIndex];
    const fixtureSelect = section.querySelector('.fixture-select');
    const sampleSelect = section.querySelector('.sample-select');
    const target = section.querySelector('.answers');
    const context = section.querySelector('.fixture-context');
    function node(tag, text, cls) {{
      const element = document.createElement(tag);
      if (cls) element.className = cls;
      element.textContent = text;
      return element;
    }}
    function draw() {{
      target.replaceChildren();
      context.replaceChildren();
      const fid = fixtureSelect.value, idx = Number(sampleSelect.value);
      const fixture = data.fixtures[fid];
      const task = node('details', '');
      task.append(node('summary', 'Original task and required facts'));
      task.append(node('pre', fixture.prompt, 'answer'));
      const facts = node('ul', '');
      for (const fact of fixture.required_facts) facts.append(node('li', fact.id + ': ' + fact.text));
      task.append(facts);
      context.append(task);
      let baselineShown = false;
      for (const entry of lane.teams) {{
        const test = entry.tests[fid] || {{}}, arms = test.arms || {{}};
        for (const arm of ['baseline', 'crisp', 'crispify']) {{
          if (arm === 'baseline' && baselineShown) continue;
          const sample = (arms[arm]?.samples || []).find(s => s.index === idx);
          if (!sample) continue;
          if (arm === 'baseline') baselineShown = true;
          const card = node('article', '', 'card');
          card.append(node('h4', arm === 'baseline' ? 'Shared neutral baseline' : entry.team + ' · ' + arm));
          card.append(node('div', sample.words + ' words · ' + (sample.tokens_est ?? 'unavailable') + ' text-token estimate · input ' + (sample.usage?.input_tokens ?? 'unavailable') + ' · output ' + (sample.usage?.output_tokens ?? 'unavailable'), 'meta'));
          card.append(node('pre', sample.text, 'answer'));
          if (arm !== 'baseline') {{
            const judgment = (test.judgments || []).find(j => j.arm === arm && j.sample === idx);
            if (judgment) {{
              const scores = node('div', '', 'scorelist');
              for (const [key, value] of Object.entries(judgment.scores.arm))
                scores.append(node('span', key + ': ' + value + ' (base ' + judgment.scores.baseline[key] + ')'));
              card.append(scores);
              card.append(node('div', 'Preferred: ' + judgment.preferred + ' · Required facts covered: ' + judgment.facts.arm.present.length + '/' + judgment.facts.arm.total, 'meta'));
              card.append(node('div', 'Baseline facts lost: ' + (judgment.facts_lost.join(', ') || 'none'), 'loss'));
              card.append(node('div', 'Useful content absent from baseline: ' + (judgment.useful_lost?.baseline || 'none'), 'meta'));
              card.append(node('div', 'Useful content absent from arm: ' + (judgment.useful_lost?.arm || 'none'), 'meta'));
              card.append(node('p', judgment.notes, 'meta'));
            }} else {{
              card.append(node('p', 'Judgment unavailable.', 'meta'));
            }}
          }}
          target.append(card);
        }}
      }}
    }}
    fixtureSelect.addEventListener('change', draw);
    sampleSelect.addEventListener('change', draw);
    draw();
  }});
}})();
</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", nargs="+", type=Path, help="one or more crisp-bench/v1 team result files")
    parser.add_argument("--fixtures", type=Path, default=ROOT / "fixtures.json")
    parser.add_argument("--output", type=Path, default=Path("crisp-comparison.html"))
    args = parser.parse_args()
    fixture_data = load_fixtures(args.fixtures)
    results = [json.loads(p.read_text(encoding="utf-8")) for p in args.results]
    data = report_data(results, fixture_data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page(data, fixture_data), encoding="utf-8")
    print(f"Wrote {args.output}")

if __name__ == "__main__": main()
