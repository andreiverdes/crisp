# CRISP benchmark harness

The harness reads the live `../fixtures.json`, `../rubric.md`, and frozen team prompts from `../prompts/<team>/` each time it runs. It does not contain fixture or prompt copies. Run from any directory; Python 3.10+ and `omp` on `PATH` are required. The runner launches one `omp auth-gateway stdio` process per sample and uses only its JSON-line interface. It never reads gateway credentials or captures stderr.

## Install and run

```sh
cd shared/harness
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

# Shared neutral baseline: 10 fixtures × 3 samples, once.
python runner.py baseline --workers 4

# For each team, direct and rewrite arms (30 each), then 60 blind paired judgments.
python runner.py team openai --workers 4
python runner.py judge openai --seed 211
python runner.py team anthropic --workers 4
python runner.py judge anthropic --seed 211

# Render available team result files into a self-contained offline report.
python render.py ../results/openai.json ../results/anthropic.json \
  --fixtures ../fixtures.json --output ../crisp-comparison.html
```

`baseline` uses `openai-codex/gpt-6-luna` with reasoning `low` and no system message. Team runs prepend only that team's frozen `crisp.md` or `crispify.md`; crispify uses the corresponding baseline sample. Judge runs use `openai-codex/gpt-6.1-sol`, reasoning `high`, no system message, and the shared rubric verbatim with its placeholders filled. Provider-default temperature is left unset. No inherited instructions, tools, or default assistant system text are added by this client.

The default generation concurrency is four (`--workers N` can be adjusted); each request is an isolated gateway process. No application-level retries or replacement samples are attempted. A failed stage exits nonzero with fixture/arm/sample provenance. Successful samples/judgments are atomically written as they finish; rerunning that stage skips already-saved indexes. On resume, edits to fixtures, rubric, prompts, model/settings, or judge seed are rejected by frozen-input manifests in `harness/*.freeze.json`. Start a new benchmark in a fresh shared checkout/output root for intentionally changed inputs; do not delete or overwrite an existing frozen run to disguise drift.

## Artifacts

- `../baseline/gpt-6-luna.json`: schema-compatible shared baseline, updated after each completed sample.
- `../results/<team>.json`: schema-compatible team result with baseline samples, both generation arms, and judgments.
- `raw/baseline/` and `raw/<team>/`: per-sample request and response audit records (generated text, finish reason, usage and status; no credentials or hidden reasoning text).
- `*.freeze.json`: hashes of the exact live inputs and run settings used for resume protection.

Words are `len(text.split())`; estimated text tokens use `tiktoken` `o200k_base`. Usage maps provider prompt/completion tokens to schema input/output tokens; absent provider values stay `null`. Report output-token caveat: provider output may include reasoning. Judgments validate all seven 1–5 dimensions, required-fact IDs and preference before persisting; malformed judge output is an error, never a fallback score. Blind order is deterministic for the seed and each fixture/arm/sample, and stored on each judgment.

The HTML report is standalone and network-free. It groups lanes by generator and judge, gives paired summary comparisons including the full system-prompt overhead, and exposes all three samples per fixture and arm with judge scores, notes, and factual losses. With three samples per fixture, model-judge assessments, and no automatic winner selection, interpret summaries alongside the answers. Token reduction is not a cost claim; inspect provider input/output totals and the answer quality.
