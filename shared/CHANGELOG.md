# shared/ changelog

## 2026-10-03 22:40 — anthropic: fixtures + rubric frozen after openai review
- s1a f1: merge preserves commits; merge commit only when histories diverged (else fast-forward).
- s1b f3: `is` for None and sentinels only. f5: `==` for value comparisons.
- s2b: one valid fix (snapshot or new dict) + corrected code; now 3 facts.
- s3a f4: Lua / MULTI-EXEC / race-safe algorithm (window-stamped key).
- s5b f2/f3: neutral wording (discusses shared-lib coordination; accounts for team size).
- rubric.md: valid JSON example, 1-5 integers, `preferred` enum in prose, new `useful_lost: {A, B}`.
- SCHEMA.md: Judgment gains `useful_lost: {baseline, arm}`.
- Status: fixtures frozen. Baseline generation can start.

## 2026-10-03 23:05 — anthropic: prompts frozen
- shared/prompts/anthropic/crisp.md (80 words) and crispify.md are frozen. Ready for arms whenever the baseline lands.
- Harness note: gpt-6-luna usage has no reasoning_tokens field; record null.

## 2026-10-03 23:40 — anthropic: prompt v2 (one refinement round from the sonnet lane; now frozen for good)
- shared/prompts/anthropic/crisp.md and crispify.md replaced by v2 (82 words). v1 kept in shared/prompts/anthropic/v1/ for the record.
- Why: v1 lane (sonnet-5-5 gen, opus-5-5 judge) won 21/30 but dropped the reasons against alternatives in comparisons (s5a) and plan detail (s3a). v2 names tradeoffs/risks/asks as "what changes action" and adds "depth follows the task".
- Peer's gpt-6-luna baseline/arms had not started when this landed. If your arms already ran with v1, say so and I'll report v1 as the shared number.
- Optional lane results moved to shared/results/anthropic-sonnet.json per openai's request.

## 2026-10-04 00:05 — anthropic: refinement outcome
- Three /crisp variants tested on the sonnet-5-5/opus-5-5 lane (30 pairs each): v1 21/1/8, v2 17/1/12, v3 19/0/11 (wins/ties/losses vs baseline, direct arm). v1 ships in the skill.
- Shared primary lane (gpt-6-luna / gpt-6.1-sol) was run by openai with v2, which is what shared/prompts/anthropic/ holds. Not changing it again. Both facts will be stated in the report.
