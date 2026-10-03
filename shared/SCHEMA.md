# CRISP benchmark — shared contract (crisp-bench/v1)

Two teams (`anthropic`, `openai`) build CRISP independently. Only the tests, result files, and the combined report are shared.

## Files

```
shared/
  SCHEMA.md                 this file
  fixtures.json             10 prompts (5 scenarios x 2) + required-fact checklists
  rubric.md                 judge prompt text (identical for both teams)
  prompts/<team>/crisp.md     frozen /crisp system prompt (30-80 words), direct arm
  prompts/<team>/crispify.md  frozen system prompt for the transform arm
  baseline/<generator-slug>.json   shared neutral baseline, generated once, reused byte-for-byte
  results/<team>.json       one file per team (schema below)
  harness/                  owned by openai team; renders results/*.json -> crisp-comparison.html
```

## Arms

| Arm | System prompt | User message | Notes |
|---|---|---|---|
| `baseline` | none | fixture `prompt` | Generated once (shared), n=3 samples per fixture |
| `crisp` | `prompts/<team>/crisp.md` | fixture `prompt` | Direct arm, n=3 |
| `crispify` | `prompts/<team>/crispify.md` | `Crispify this:\n\n<baseline sample text>` | One transform per baseline sample (n=3); `source_sample` records which |

## Generation settings

- Primary lane: generator `openai-codex/gpt-6-luna`, reasoning `low`, provider default temperature, stateless single-turn, no tools, no inherited agent/system style. Baseline has **no** system prompt at all.
- Optional second lane: generator `anthropic/claude-sonnet-5-5`, same settings. Run by anthropic team for both teams' frozen prompts.
- Judge: `openai-codex/gpt-6.1-sol` (same family as primary generator — disclosed in the report). Optional second judge `anthropic/claude-opus-5-5`.
- Lanes are keyed by `(generator, judge)` and rendered as separate tables; primary lane first.

## Counting

- `words`: `len(text.split())`
- `tokens_est`: tiktoken `o200k_base` on the response text (label as estimate)
- `usage`: provider-reported `input_tokens`, `output_tokens`, `reasoning_tokens` (null if unavailable). Output tokens may include reasoning; keep `tokens_est` as the text-only number.
- Prompt overhead: `tokens_est` of each team's `crisp.md`, plus `usage.input_tokens` delta vs baseline when available.

## Judging

- Blind, pairwise: each `crisp`/`crispify` sample vs the baseline sample with the same index.
- Randomize display order per pair; record `order`.
- Judge prompt: `rubric.md` verbatim with placeholders filled. Judge returns JSON (schema in rubric.md).
- Dimensions, 1-5 each: `correctness`, `clarity`, `ambiguity` (5 = no ambiguity), `scanability`, `relevance`, `conversational`, `completeness`.
- Facts: judge marks each fixture `required_facts` id as present/absent in each response. `facts_lost` = present in baseline, absent in arm (only facts the baseline actually had count as lost). `useful_lost` = judge's free-text note of useful non-required content each side lacks, mapped back to `baseline`/`arm`.
- `preferred`: `A`/`B`/`tie` as shown, mapped back to `baseline`/`arm`/`tie` in results.

## results/<team>.json

```jsonc
{
  "schema": "crisp-bench/v1",
  "team": "anthropic",
  "generated_at": "2026-10-03T22:00:00Z",
  "prompts": {
    "crisp": "<frozen text>", "crisp_tokens_est": 61,
    "crispify": "<frozen text>", "crispify_tokens_est": 80
  },
  "lanes": [
    {
      "generator": "openai-codex/gpt-6-luna",
      "generator_settings": {"reasoning": "low", "temperature": null},
      "judge": "openai-codex/gpt-6.1-sol",
      "tokenizer_est": "tiktoken/o200k_base",
      "baseline_file": "baseline/gpt-6-luna.json",
      "tests": [
        {
          "id": "s1a",
          "arms": {
            "baseline": {"samples": [ /* Sample */ ]},
            "crisp":    {"samples": [ /* Sample */ ]},
            "crispify": {"samples": [ /* Sample, with source_sample */ ]}
          },
          "judgments": [ /* Judgment */ ]
        }
      ]
    }
  ]
}
```

```jsonc
// Sample
{
  "index": 0,
  "text": "...",
  "words": 212,
  "tokens_est": 280,
  "usage": {"input_tokens": 120, "output_tokens": 300, "reasoning_tokens": 20},
  "latency_ms": 4100,
  "source_sample": 0            // crispify only: index of the baseline sample transformed
}

// Judgment
{
  "arm": "crisp",               // or "crispify"
  "sample": 0,                  // arm sample index
  "baseline_sample": 0,
  "order": "baseline_first",    // or "arm_first"
  "judge": "openai-codex/gpt-6.1-sol",
  "scores": {
    "baseline": {"correctness": 5, "clarity": 3, "ambiguity": 4, "scanability": 3, "relevance": 3, "conversational": 3, "completeness": 5},
    "arm":      {"correctness": 5, "clarity": 5, "ambiguity": 4, "scanability": 5, "relevance": 5, "conversational": 4, "completeness": 4}
  },
  "facts": {
    "baseline": {"present": ["f1","f2","f3","f4","f5"], "total": 5},
    "arm":      {"present": ["f1","f2","f3","f5"],      "total": 5}
  },
  "facts_lost": ["f4"],
  "useful_lost": {"baseline": "", "arm": "Baseline explained the Retry-After calculation; arm does not."},
  "preferred": "arm",           // "baseline" | "arm" | "tie"
  "notes": "short judge rationale"
}
```

## baseline/<generator-slug>.json

```jsonc
{
  "schema": "crisp-bench/baseline-v1",
  "generator": "openai-codex/gpt-6-luna",
  "generator_settings": {"reasoning": "low", "temperature": null},
  "generated_at": "...",
  "tests": { "s1a": {"samples": [ /* Sample x3 */ ]}, "...": {} }
}
```

## Report (harness output)

Per lane: summary table (per team: mean words, mean tokens_est, % reduction vs baseline, mean rubric scores, facts retained %, win rate), then per fixture: baseline | openai crisp | anthropic crisp | openai crispify | anthropic crispify, with scores and facts_lost under each. Standalone HTML, no network.
