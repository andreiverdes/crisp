## 21. Benchmark results

CRISP's `/crisp` prompt cuts 41-47% of words on a verbose model and wins 21 of 30 blind pairings; on a model that is already terse it cuts 15% and ties. The transform arm (crispify an existing answer) never lost on the verbose model and kept 99-100% of required facts. The direct arm's losses cluster in two places: a dropped timestamp in a status update and a dropped cause in a debugging answer. Both are rule 8 failures ("short is not cryptic") and are the reason the shipped prompt lists what to keep.

### Setup

Ten prompts, two per scenario: technical Q&A, debugging, spec/plan for a coding agent, status update from raw notes, comparison with recommendation. Each prompt carries 3-7 required facts a complete answer must state. Three arms per prompt, n = 3 samples each:

- baseline: no system prompt at all;
- crisp: the 80-word `/crisp` prompt (section 23) as the system prompt;
- crispify: the same prompt with a rewrite instruction, applied to each baseline sample.

A judge saw each crisp or crispify sample next to the baseline sample with the same index, in random order, without knowing which was which, and scored both 1-5 on correctness, clarity, ambiguity, scanability, relevance, conversational tone, and completeness; marked each required fact present or absent; and picked a winner. Words are whitespace-split; tokens are a tiktoken `o200k_base` estimate on the text. Fixtures, rubric, and schema were shared with a competing team so both results render in one report (`shared/crisp-comparison.html`).

Two lanes:

| Lane | Generator (reasoning low) | Judge (reasoning high) | Baseline length |
|---|---|---|---|
| Primary (shared with the competing team) | openai-codex/gpt-6-luna | openai-codex/gpt-6.1-sol | 208 words |
| Second (this team only) | anthropic/claude-sonnet-5-5 | anthropic/claude-opus-5-5 | 457 words |

Judge and generator share a vendor in both lanes; the second lane is the cross-check on the first.

### Results, direct arm (`/crisp` as system prompt)

| Lane | Words | Tokens (est.) | Facts kept | Wins / ties / losses | Relevance | Completeness |
|---|---|---|---|---|---|---|
| Sonnet 5.5, v1 prompt (shipped) | 457 → 245 (−46%) | 706 → 377 (−47%) | 97% | 21 / 1 / 8 | 3.7 → 5.0 | 5.0 → 4.4 |
| Sonnet 5.5, v2 prompt | 457 → 270 (−41%) | 706 → 415 (−41%) | 96% | 17 / 1 / 12 | 3.8 → 4.9 | 5.0 → 4.4 |
| gpt-6-luna, v2 prompt (shared) | 208 → 176 (−15%) | 289 → 246 (−15%) | 92% of baseline's | 12 / 6 / 12 | 5.0 → 5.0 | 4.1 → 4.0 |

Scores are the judge's mean on a 1-5 scale, baseline → arm. On the Sonnet lane every dimension except completeness and correctness rose; clarity 4.6 → 5.0, scanability 4.2 → 4.6, conversational 3.7 → 4.4, correctness 4.7 → 4.6. On the gpt-6-luna lane ambiguity rose 4.2 → 4.4 and correctness 4.7 → 4.9; the rest moved within 0.1.

### Results, transform arm (crispify a baseline answer)

| Lane | Words | Facts kept | Wins / ties / losses | Overall score |
|---|---|---|---|---|
| Sonnet 5.5, v1 | 457 → 364 (−20%) | 99% | 27 / 0 / 3 | 4.5 → 4.8 |
| Sonnet 5.5, v2 | 457 → 372 (−19%) | 100% | 23 / 7 / 0 | 4.6 → 4.8 |
| gpt-6-luna, v2 | 208 → 174 (−16%) | 99% of baseline's | 9 / 18 / 3 | 4.7 → 4.6 |

Crispify is the safer transformation: it starts from a complete answer and removes, so it rarely loses a fact. It also saves less, because it keeps the baseline's structure.

### Where compression lost

The judge's notes name the same losses across samples:

- Status update (s4b): the direct arm dropped the 14:05 deploy time in 3 of 3 gpt-6-luna samples, breaking the timeline. The baseline had it.
- Debugging (s2b): the v2 prompt's "cause, tradeoffs, risks" line made Sonnet give the fix without the cause ("why does this error happen") in 3 of 3 samples. v1, which says "keep code, corrections, risks, real uncertainty", kept the cause in 3 of 3.
- Comparison (s5a): both prompt versions dropped the per-listener connection cost of Postgres LISTEN/NOTIFY in 2-3 of 3 samples. The judge preferred the baseline's longer tradeoff discussion.
- Plan for a coding agent (s3a): the direct arm wrote shorter plans that lost operational detail (fail-open decision, Retry-After derivation) in 2 of 3 Sonnet samples; the judge preferred the longer baseline plan for an executor.

Pattern: the direct arm compresses the reasons behind a recommendation and the small facts in a narrative. Those are exactly what section 11 calls relevant (they change the decision) and what rule 8 says to keep.

### What changed in the protocol

- Rule 8 names what concision must not cut: code, corrections, risks, real uncertainty. v1 says this in the prompt; v2 replaced it with "depth follows the task" and lost 4 pairings. v1 ships.
- Section 14's status-update shape says an incident report puts the timeline first and keeps every timestamp, because the dropped-timestamp failure recurred.
- Section 11 says the tradeoff that rules out the alternatives is relevant in a recommendation, because comparison answers lost pairings when they gave the verdict without it.
- The three prompt sizes exist because an 80-word prompt cannot carry the keep-list in full; Minimal and Full state it.

### Caveats

- Thirty pairings per arm per lane; a 3-pairing swing is within noise. The v1/v2/v3 ranking (21, 17, 19 wins) is suggestive, not significant.
- Judges share a vendor with their generator. The two lanes agree on direction, which is the only mitigation applied.
- The gpt-6-luna baseline is short without any prompt, so that lane measures what CRISP does to an already-terse model: small savings, no quality loss, one recurring timestamp omission.
- Length-controlled judging was not applied; the rubric tells the judge that length is not a virtue, and the judge's notes show it penalizing padding and rewarding kept detail in both directions.

Raw samples, judgments, and the renderer: `bench/` in this repo; shared fixtures, rubric, and both teams' results: `shared/`.
