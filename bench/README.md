# CRISP bench runner

Python 3, stdlib + `tiktoken`. Transport: `omp auth-gateway stdio` (needs `omp` on PATH).

## Install

```
python3 -m pip install --user --break-system-packages tiktoken
```

(Homebrew Python refuses a bare `pip install --user` under PEP 668. Use a venv if you prefer.)

## Commands, in order

`shared/...` paths resolve to `../shared/` when no local `shared/` exists (override: `CRISP_SHARED=/path`).
All steps are resumable: rerun the same command after a failure and only missing items run. Add `--limit` for a smoke run (first fixture, n=1 baseline). `--concurrency N` (default 4) sets gateway processes and threads.

```
# 1. shared baseline (no system prompt). Skip if shared/baseline/<slug>.json exists.
python3 bench/run.py baseline --generator openai-codex/gpt-6-luna --n 3 --reasoning low --out shared/baseline/gpt-6-luna.json

# 2. crisp (direct) and crispify (transform of each baseline sample) arms
python3 bench/run.py arms --team anthropic --generator openai-codex/gpt-6-luna --reasoning low --baseline shared/baseline/gpt-6-luna.json --prompts shared/prompts/anthropic --out bench/out/anthropic-gpt-6-luna-arms.json

# 3. blind pairwise judging against the baseline sample with the same index
python3 bench/run.py judge --arms bench/out/anthropic-gpt-6-luna-arms.json --baseline shared/baseline/gpt-6-luna.json --judge openai-codex/gpt-6.1-sol --reasoning high --out bench/out/anthropic-gpt-6-luna-judged.json

# 4. merge lanes into the results file (repeat --lane per generator/judge pair)
python3 bench/run.py assemble --team anthropic --prompts shared/prompts/anthropic --lane bench/out/anthropic-gpt-6-luna-judged.json --out shared/results/anthropic.json

# 5. print per-lane tables
python3 bench/run.py summary shared/results/anthropic.json
```

Optional HTML report (one or more teams' files, standalone, no network):

```
python3 bench/render.py shared/results/*.json -o bench/out/crisp-comparison.html
```

## Files

| File | Role |
|---|---|
| `gateway.py` | `Gateway` (one `omp auth-gateway stdio` process, id-matched replies, 3 retries with backoff, `chat() -> {text, usage, latency_ms}`) and `GatewayPool` (N processes, least-busy dispatch). |
| `count.py` | `words()` = `len(text.split())`; `tokens_est()` = tiktoken `o200k_base`. |
| `stats.py` | Aggregation shared by `summary` and `render.py`. |
| `run.py` | CLI: `baseline`, `arms`, `judge`, `assemble`, `summary`. |
| `render.py` | Standalone HTML comparison across teams. |
| `out/*-arms.json` | Raw crisp/crispify samples (`crisp-bench/arms-v1`, internal). |
| `out/*-judged.json` | Judgments per test (`crisp-bench/judged-v1`, internal). |
| `shared/results/<team>.json` | Final `crisp-bench/v1` file. |
| `out/smoke/` | Smoke-run output; temporary prompts in `out/smoke/prompts/`. |

## Notes

- Judge order: seeded by `random.Random("<test id>:<arm>:<sample index>")`; `order` is recorded. `useful_lost` and `notes` are the judge's own text and may say "A"/"B"; `order` maps letters (`baseline_first` = A is baseline).
- `usage.reasoning_tokens` is read from `completion_tokens_details.reasoning_tokens`; it is `null` when the gateway does not report it (observed for `openai-codex/gpt-6-luna` and `anthropic/claude-sonnet-5-5`).
- `reasoning_effort` is accepted by `anthropic/claude-sonnet-5-5` (`low` and `high` returned 200).
- One gateway process answers requests serially (4 concurrent requests completed one after another), so parallelism comes from the process pool.
