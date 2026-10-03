# Lane: LLM prompting, instruction following, verbosity, token efficiency

Method note: arXiv sources were read at abstract level (via the arXiv API fetch). Official docs and the Giskard post were read in full or in the relevant sections. Claims beyond what those pages state are marked as inference.

## Approaches
| Approach | Useful ideas | Problems | Use in CRISP? |
|---|---|---|---|
| Plain clear/direct instructions (Anthropic, OpenAI, Google guides) | State the output format, constraints and the reason for them; one-line fixes steer modern models | Vendor guidance, mostly untested outside vendor evals | yes: core of the voice |
| XML/section structure for prompts | Separates instructions, context, examples, input | Evidence is vendor-reported; effect size varies by model | partly: use headings/labels, not tag soup |
| "Be concise" instructions | Cuts length 30-50% on easy tasks (Renze & Guven) | Can hurt math and factual rebuttals (Phare, Renze & Guven) | partly: bound by content, not by word count |
| Chain of Draft / constrained CoT | Terse reasoning at a fraction of the tokens | Author-reported; math with weaker models degrades | partly: terse reasoning is fine, answers must stay complete |
| Token-level prompt compression (LLMLingua) | Redundancy in prose is real; 2-5x compression is feasible | Machine-compressed text is unreadable; benchmarked on QA/reasoning, not specs | no: write short, don't post-process |
| Rule lists / many constraints | Explicit rules work for a few instructions | Compliance falls as instruction count grows (IFScale, RuLES) | partly: few rules, ranked, no contradictions |
| Strict JSON/format restriction | Parseable output | Hurt reasoning in Tam et al. | partly: reason first, format last |
| LLM-judge / preference-tuned "good" style | Reveals what graders reward | Rewards length and agreement, not truth | no: never optimize for judge-pleasing style |

## Findings

### F1. Models use the middle of long inputs worst
- Evidence: Liu et al., "Lost in the Middle", TACL 2023/24. https://arxiv.org/abs/2307.03172
- Strength: well-supported (for the models tested; newer long-context models are better, but vendors still warn of degradation)
- Implication for CRISP: Put the ask and the constraints at the start, and repeat a one-line restatement at the end of long messages. Never bury the key instruction mid-document.

### F2. Input length alone degrades reasoning, well below the context limit
- Evidence: Levy, Jacoby, Goldberg, "Same Task, More Tokens", ACL 2024. https://arxiv.org/abs/2402.14848 — padding of different types and locations lowered reasoning accuracy at lengths far below the technical maximum, even with irrelevant padding.
- Strength: well-supported
- Implication for CRISP: Every sentence of filler costs accuracy as well as tokens. Cutting padding is a correctness rule, not just a cost rule.

### F3. Instruction following falls as instruction count rises; early instructions win
- Evidence: Jaroslawicz et al., "How Many Instructions Can LLMs Follow at Once?" (IFScale), 2025. https://arxiv.org/abs/2507.11538 — best frontier model reached 68% at 500 keyword instructions, with a bias toward earlier instructions. Mu et al., "Can LLMs Follow Simple Rules?" (RuLES), 2023. https://arxiv.org/abs/2311.04235 — almost all models broke rules even on simple cases.
- Strength: well-supported for density; the primacy bias is one benchmark's finding
- Implication for CRISP: Cap rules per message, order them by importance, and put hard constraints first. A short ranked list beats an exhaustive one.

### F4. Contradictory or vague instructions are costly; redundancy is not the worst failure
- Evidence: OpenAI, "GPT-5 prompting guide". https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide.md — contradictions make the model burn reasoning tokens reconciling them. The Cursor case reports an emphatic "Be THOROUGH" (all caps) instruction caused tool overuse. Anthropic, "Prompting best practices" says that on Opus 4.5/4.6 aggressive "CRITICAL: You MUST" language now overtriggers. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Strength: well-supported by vendor testing (not independent)
- Implication for CRISP: Remove conflicts before trimming words. Use normal-strength wording ("Use X when...") and reserve emphasis for the rare hard stop.

### F5. Modern models follow literal, explicit instructions; they don't infer unstated intent
- Evidence: OpenAI GPT-4.1 guide: one firm sentence "is almost always sufficient" to steer. https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide. Anthropic: "can you suggest changes" gets suggestions, "change this function" gets edits. Opus 5 guide: "only report high-severity issues" is followed literally and misses findings; ask for everything and filter separately. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Strength: well-supported (vendor-reported)
- Implication for CRISP: Use imperative verbs for actions ("Change X", not "could you"). State the scope and the stop condition. Don't add soft hedges like "be conservative" without a definition.

### F6. Concision instructions can cut length with little loss on easy tasks
- Evidence: Renze & Guven, "Benefits of a Concise Chain of Thought", 2024. https://arxiv.org/abs/2401.05618 — response length down 48.7%, negligible accuracy change on MCQA, per-token cost down 22.7%. Xu et al., "Chain of Draft", 2025. https://arxiv.org/abs/2502.18600 — matches or beats CoT using as little as 7.6% of the tokens (author-reported).
- Strength: reasonable hypothesis (small benchmarks, author-run, older models in Renze)
- Implication for CRISP: Terse reasoning and no-preamble answers are safe defaults for structured and easy tasks.

### F7. Concision instructions can hurt correctness: on math, and on factual rebuttal
- Evidence: Renze & Guven (same paper): GPT-3.5 with concise CoT lost 27.69% on math. Giskard, Phare hallucination analysis, 2025. https://www.giskard.ai/knowledge/good-answers-are-not-necessarily-factual-answers-an-analysis-of-hallucination-in-leading-llms — "answer briefly" lowered hallucination resistance in most models, up to a 20% drop, because rebuttals need space; models picked brevity over accuracy. Jin et al., "Impact of Reasoning Step Length", 2024. https://arxiv.org/abs/2401.04925 — shortening reasoning steps in prompts reduced reasoning ability; complex tasks gain from longer inference.
- Strength: well-supported that the effect exists; condition (weak model, multi-step, false-premise question) is the key variable. Giskard is a vendor blog, not peer-reviewed.
- Implication for CRISP: Never cap the length of reasoning, caveats or corrections. Concision applies to the final deliverable. Correcting a false premise outranks brevity.

### F8. Verbose answers are often the uncertain ones
- Evidence: Zhang, Das, Zhang, "Verbosity ≠ Veracity", 2024. https://arxiv.org/abs/2411.07858 — verbosity compensation (repeating the question, ambiguity, excess enumeration) appeared across all 14 models; GPT-4 showed it 50.4% of the time; verbose answers scored lower (27.61% gap on Qasper) and had higher uncertainty.
- Strength: well-supported (one study, QA tasks)
- Implication for CRISP: Padding, restating the question, and enumerating every option are tells of low confidence. Rule: answer first; say "unknown" or "unverified" instead of padding.

### F9. Training and graders reward length and agreement, which causes LLM bloat
- Evidence: Singhal et al., "A Long Way to Go", 2023. https://arxiv.org/abs/2310.03716 — a length-only reward reproduces most RLHF gains. Dubois et al., Length-Controlled AlpacaEval, 2024. https://arxiv.org/abs/2404.04475 — automatic judges favor longer outputs; controlling length lifts Arena correlation from 0.94 to 0.98. Sharma et al., "Towards Understanding Sycophancy", 2023. https://arxiv.org/abs/2310.13548 — humans and preference models sometimes prefer sycophantic over correct answers.
- Strength: well-supported
- Implication for CRISP: Default LLM style is biased toward length and agreement, so CRISP must counter both explicitly: no flattery openers, no restating, state disagreement directly. A CRISP benchmark must use length-controlled or rubric judging, never raw preference.

### F10. Redundancy in prose is large and can be removed with small loss, but compression must keep the instruction intact
- Evidence: Jiang et al., LLMLingua, 2023. https://arxiv.org/abs/2310.05736 — up to 20x compression with little loss on GSM8K/BBH-style tasks. Pan et al., LLMLingua-2, 2024. https://arxiv.org/abs/2403.12968 — 2-5x compression, token-classification for faithfulness. Li et al., Prompt Compression survey, 2024. https://arxiv.org/abs/2410.12388 (abstract only read; it analyzes limitations).
- Strength: well-supported for context compression; [INFERENCE] results on instruction text and specs are not established by these abstracts
- Implication for CRISP: Drop function words and hedges, not facts, names, numbers or negations. Don't drop articles to the point of telegraphese; that is unnatural and untested for instruction-following.

### F11. Prompt format changes accuracy by model, so no single markup is universally best
- Evidence: He et al., "Does Prompt Formatting Have Any Impact?", 2024. https://arxiv.org/abs/2411.10541 — GPT-3.5 varied up to 40% across plain/Markdown/JSON/YAML templates on code translation; GPT-4 was more robust. Schulhoff et al., The Prompt Report, 2024. https://arxiv.org/abs/2406.06608 — taxonomy of 58 techniques plus a meta-analysis (abstract only read).
- Strength: well-supported for sensitivity; no winner format
- Implication for CRISP: Pick a consistent, plain structure (labeled sections, short lists) and keep it consistent across a prompt. Don't claim Markdown improves model accuracy; its benefit is human scanability.

### F12. Strict structured output hurts reasoning; reason first, format after
- Evidence: Tam et al., "Let Me Speak Freely?", 2024. https://arxiv.org/abs/2408.02442 — format restrictions caused a significant decline in reasoning, and stricter formats degraded more. Anthropic and Google both recommend structured-output features or schemas for complex JSON, over hand-written prose instructions. https://ai.google.dev/gemini-api/docs/prompting-strategies
- Strength: well-supported (one paper plus vendor advice; later work disputes parts of the paper, which I did not read)
- Implication for CRISP: For agent-to-agent messages, allow free reasoning, then a short fixed-field result block. Don't force JSON on the thinking step.

### F13. Positive, example-matched formatting instructions work better than prohibitions
- Evidence: Anthropic best practices: "Tell Claude what to do instead of what not to do"; prompt style influences output style (removing Markdown from the prompt reduces Markdown in the output); explain the reason behind a rule. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices. Google: few-shot examples show the format; examples can replace instructions. https://ai.google.dev/gemini-api/docs/prompting-strategies
- Strength: well-supported (vendor testing), stylistic preference for the "reason" part
- Implication for CRISP: Write rules as "Lead with the result", not "Don't ramble". The CRISP spec should itself be written in the style it asks for, plus one short good/bad example per rule.

### F14. Explicit length instructions work, and brevity guidance needs a "when" clause
- Evidence: Anthropic Opus 5 guide: default responses run longer; effort controls thinking not visible length; use a short explicit conciseness instruction plus a reminder at the end of a long system prompt; calibrate document length ("don't pad with filler sections, redundant summaries"); state "lead with the outcome" for updates. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 OpenAI GPT-5: a verbosity parameter plus natural-language overrides per context (Cursor: low globally, high for code). https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide.md
- Strength: well-supported (vendor-reported)
- Implication for CRISP: Make length contextual: short status and answers, full detail where the reader needs it (code, rebuttals, specs). Use "outcome first, detail after" as the universal shape.

### F15. Redundant verification and "double-check" instructions waste tokens on current models
- Evidence: Anthropic Opus 5 guide: explicit verification steps and "double-check" instructions cause over-verification and add cost with no quality gain. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Strength: reasonable hypothesis (single vendor, one model)
- Implication for CRISP: Don't pad agent specs with generic "be careful/verify" boilerplate. Give a concrete check (command, expected result) or nothing.

### F16. Placement: instructions at both ends of long context, or at least above it; query last also helps
- Evidence: OpenAI GPT-4.1 guide: instructions at the beginning and end beat either alone. Anthropic: documents first, query at end can improve quality up to 30% in their tests. The two disagree on single placement, so repeat at both ends. https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- Strength: reasonable hypothesis (vendor tests conflict on single placement)
- Implication for CRISP: In long prompts, state the task first and restate the output requirement last, in one line.

## Research questions
- **What improves clarity?** Specific output format and constraints, the reason behind a rule, concrete examples, one instruction per sentence, and no contradictions (F4, F5, F13).
- **What reduces ambiguity?** Imperative verbs, defined scope and stop condition, and explicit unknowns. Vague hedges ("be conservative") get followed literally and unpredictably (F5, F4).
- **What reduces verbosity?** Explicit, contextual length instructions; answer-first shape; ban on restating the question. Defaults drift long because training rewards length (F9, F14, F8).
- **What improves scanability?** Evidence is mostly for humans, not models: labeled sections and short lists. Vendors say too many bullets fragment prose (Anthropic), so use lists for discrete items only. Model-accuracy gain from Markdown is unproven (F11).
- **What sounds natural vs artificial?** Anthropic describes its current models as "more conversational, less machine-like" and recommends the "new employee" test: a colleague with no context should be able to follow it. [INFERENCE] telegraphic compression like LLMLingua output fails that test.
- **What saves/wastes tokens?** Saves: no preamble, no restating, terse reasoning, one-line outcome (F6, F8). Wastes: padding in input (accuracy cost, F2), repeated verification boilerplate (F15), long emphatic rule lists (F3, F4). Output tokens cost more than input, but cutting reasoning can cost accuracy (F7).
- **Specs vs normal answers vs coding agents?** Specs: complete task up front, unambiguous scope, concrete acceptance checks (Anthropic Opus 5). Answers: outcome first, short. Coding agents: persistence/stop conditions, explicit tool-use instructions, verbosity high for code and low for chat (Cursor, GPT-5 guide). Agent-to-agent: free reasoning, then a fixed short result (F12).
- **What can LLMs follow reliably?** A few explicit, non-conflicting, literal instructions on format and scope; positive phrasing; examples (F3, F5, F13). Unreliable: dozens of rules, conflicting priorities, adversarial or ambiguous rules (RuLES, IFScale). IFEval-style verifiable constraints (word count, keyword) are testable, but I read only its abstract, so I have no per-type reliability numbers.
- **Evidence vs preference?** Evidence: length hurts reasoning (F2); instruction density hurts compliance (F3); length bias in training and judges (F9); concision can hurt facts and math (F7). Preference or vendor-only: XML tags, ordering of query and context, casual tone, "no verification boilerplate".

## Sources
1. Liu et al., Lost in the Middle (2023). https://arxiv.org/abs/2307.03172
2. Levy et al., Same Task, More Tokens (2024). https://arxiv.org/abs/2402.14848
3. Zhou et al., IFEval (2023). https://arxiv.org/abs/2311.07911 (abstract: 25 verifiable instruction types, ~500 prompts)
4. Jaroslawicz et al., IFScale (2025). https://arxiv.org/abs/2507.11538
5. Mu et al., Can LLMs Follow Simple Rules? (2023). https://arxiv.org/abs/2311.04235
6. Wallace et al., The Instruction Hierarchy (2024). https://arxiv.org/abs/2404.13208 (abstract only; used for system-prompt priority: models treat system and user text as equal priority unless trained otherwise)
7. Singhal et al., A Long Way to Go (2023). https://arxiv.org/abs/2310.03716
8. Dubois et al., Length-Controlled AlpacaEval (2024). https://arxiv.org/abs/2404.04475
9. Zhang et al., Verbosity ≠ Veracity (2024). https://arxiv.org/abs/2411.07858
10. Sharma et al., Towards Understanding Sycophancy (2023). https://arxiv.org/abs/2310.13548
11. Renze & Guven, Concise Chain of Thought (2024). https://arxiv.org/abs/2401.05618
12. Nayab et al., Concise Thoughts (2024). https://arxiv.org/abs/2407.19825 (abstract only; no numbers cited)
13. Xu et al., Chain of Draft (2025). https://arxiv.org/abs/2502.18600
14. Jin et al., Impact of Reasoning Step Length (2024). https://arxiv.org/abs/2401.04925
15. Giskard, Phare hallucination analysis (2025). https://www.giskard.ai/knowledge/good-answers-are-not-necessarily-factual-answers-an-analysis-of-hallucination-in-leading-llms
16. Jiang et al., LLMLingua (2023). https://arxiv.org/abs/2310.05736
17. Pan et al., LLMLingua-2 (2024). https://arxiv.org/abs/2403.12968
18. Li et al., Prompt Compression survey (2024). https://arxiv.org/abs/2410.12388
19. He et al., Does Prompt Formatting Have Any Impact? (2024). https://arxiv.org/abs/2411.10541
20. Tam et al., Let Me Speak Freely? (2024). https://arxiv.org/abs/2408.02442
21. Schulhoff et al., The Prompt Report (2024). https://arxiv.org/abs/2406.06608
22. Anthropic, Prompting best practices. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
23. Anthropic, Prompting Claude Opus 5. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
24. OpenAI, GPT-4.1 prompting guide. https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
25. OpenAI, GPT-5 prompting guide. https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide.md
26. Google, Gemini prompt design strategies. https://ai.google.dev/gemini-api/docs/prompting-strategies
