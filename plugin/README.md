# CRISP

**Say the useful thing once, as clearly as possible, then stop.**

CRISP (Concise · Relevant · Intuitive · Simple · Protocol) is a writing protocol for humans and LLMs. This plugin adds it to Claude: one skill, `/crisp`, that makes replies read like one competent engineer talking to another instead of a chatbot.

## What it does

Once added, Claude applies ten checkable rules to its answers whenever you say `/crisp`, "use CRISP", "crispify this", or "make this crispier", and whenever a project's `CLAUDE.md` or `AGENTS.md` asks for CRISP:

1. **Answer first.** The first sentence is the answer, decision, result, or ask.
2. **Say it once.** No preview, recap, restated question, or restated context.
3. **Keep what changes action.** Every sentence changes what you know, do, or decide.
4. **Plain words, same words.** Common verbs; one term per concept; no intensifiers without a measurement.
5. **Name the actor, state the condition.** "If X, do Y." "X failed because Y."
6. **Replace vague with checkable.** Soon, appropriate, usually become a number, a name, a condition, or "unknown".
7. **Structure is earned.** Prose by default; lists, tables, headings only when they aid scanning.
8. **Short is not cryptic.** Code, corrections, risks, and real uncertainty stay.
9. **Sound like a colleague.** No flattery, ceremony, apology, or ritual hedges.
10. **Stop.** No closing summary, no "let me know".

Three depths: `/crisp 1` (just the answer), `/crisp 2` (default), `/crisp 3` (plus rationale, alternatives, risks). Levels change how much is said, never how well.

## Example

**Prompt:** "My React component re-renders forever when I fetch data in useEffect. What's wrong?"

Without CRISP, a typical answer opens with "Great question!", lists every possible cause, adds unrelated advice about cleanup functions, and closes with "I hope this helps!" (154 words).

With CRISP (80 words):

> Most likely your effect has no dependency array, so it runs after every render, and its `setState` triggers the next render.
>
> 1. Check the `useEffect` call. If it has no second argument, add one: `useEffect(() => {...}, [])`.
> 2. If it already has an array and still loops, look for an object or function in it that is created inline in the component body. It gets a new identity on every render.
> 3. Wrap that value in `useMemo` or `useCallback`.

## Measured

Blind pairwise judging against the same model with no instructions, 10 prompts × 3 samples (Claude Sonnet 5.5, judged by Claude Opus 5.5): **47% fewer tokens, 21 of 30 pairings preferred, 97% of required facts kept.** Rewriting an existing answer with CRISP ("crispify this") scored 27 of 30. Full method, raw data, and a second lane on GPT-6: [andreiverdes.github.io/crisp/benchmark](https://andreiverdes.github.io/crisp/benchmark/).

## For projects

`skills/crisp/scripts/install.py` writes a CRISP block into a project's `AGENTS.md` and `CLAUDE.md` so every agent in that repo replies in CRISP, with or without this plugin. Run it from the project root; `--level crisp|minimal|full` picks the prompt size, `--command` also creates a `/crisp` slash command, `--check` and `--remove` do what they say. The script only touches those files in the current directory and reads nothing else.

## What this plugin runs, sends, or fetches

Nothing. It is one `SKILL.md` with instructions, four prompt files, two reference files, and the optional `install.py` above. No hooks, no MCP servers, no network calls, no credentials.

## Source

The protocol, the research behind each rule, and the benchmark harness live at [github.com/andreiverdes/crisp](https://github.com/andreiverdes/crisp). This repository is the plugin bundle built from it, published by [HorizonLoop](https://github.com/horizon-loop). Version {{VERSION}}, MIT.
