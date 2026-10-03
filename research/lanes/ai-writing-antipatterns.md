# Lane: AI writing anti-patterns

## Approaches
| Approach | Useful ideas | Problems | Use in CRISP? |
|---|---|---|---|
| Wikipedia "Signs of AI writing" field guide | Largest observed-pattern catalog; examples; pattern families | Descriptive, not prescriptive; Wikipedia-specific; says fixing signs ≠ fixing problems | yes: seed the ban list, not the goal |
| Word-frequency studies (Liang, Kobak, Yakura) | Measured over-used words; marker words co-occur | Lists decay (delve fell in 2025); banning synonyms-by-word is whack-a-mole | partly: short ban list, rule on the cause |
| Lab style specs (OpenAI Model Spec, Claude docs, GPT-4.1 guide) | Exact suppression wording; good/bad pairs | Written for chat assistants; some contradict (see F9) | yes: reuse wording that tests well |
| Sycophancy / calibration research | Causal story: preference data rewards flattery and confidence | No fix for terseness; hedge effects depend on phrasing | yes: honesty rules, not tone rules |
| Human-detection studies | What readers actually notice | Experts only; nonexperts at chance | partly: tells the cost of slop, not the cure |
| Community terse prompts ("no yapping") | Cheap, quick | Unevidenced; cause cryptic output | no: unmeasured, drift to telegraphese |
| Chain of Draft | Compact reasoning with equal accuracy | Applies to reasoning traces, not prose for readers | partly: "minimal but informative" |

## Findings
### F1. LLM prose regresses to generic, positive, important-sounding statements
- Evidence: "Wikipedia:Signs of AI writing", WikiProject AI Cleanup, 2026. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Strength: reasonable hypothesis (editor consensus, example-backed)
- Implication for CRISP: ban significance claims ("marks a pivotal moment", "highlights its enduring legacy") unless the user asked and a fact backs them. Replace with the specific fact.

### F2. Wikipedia names a fixed set of structural tells
- Evidence: same page. Quoted headings: "Undue emphasis on significance, legacy, and broader trends"; "Superficial analyses" (trailing "-ing" phrases); "Vague attributions and overgeneralization of opinions"; "Outline-like conclusions about challenges and future prospects"; "Promotional and advertisement-like language"; "Avoidance of basic copulatives"; "Negative parallelisms" ("Not only … but …", "It's not X, it's Y"); "Rule of three"; "Overuse of em dashes"; "Title case"; "Overuse of boldface"; "Inline-header vertical lists"; "Emoji as formatting"; "Knowledge-cutoff disclaimers"; "Communication intended for the user".
- Strength: reasonable hypothesis
- Implication for CRISP: one rule per family. "Use is/has, not serves as/boasts." "No trailing -ing commentary." "Name the source or drop the claim."

### F3. Humans without LLM experience detect AI text at chance; heavy users detect it ~93%
- Evidence: Russell, Karpinska, Iyyer, "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text", ACL 2025. https://arxiv.org/abs/2501.15654 (read v2 HTML). Experts TPR 92.7 / FPR 4.0; nonexperts 56.7 / 51.7. Clue frequency: vocabulary 53.1%, sentence structure 35.9%, grammar/punctuation 24.8%, originality 23.7%, clarity 19.5%.
- Strength: well-supported
- Implication for CRISP: slop costs trust with the readers who use LLMs most, i.e. CRISP's audience. Vocabulary is the top tell, so a short word list is worth having.

### F4. Humanizing prompts and paraphrase did not hide the signature
- Evidence: Russell et al. 2025 (above). Experts stayed near-perfect after paraphrase and a guidebook-based "humanizer"; sentence-structure and originality clues survived. Experts also flag "not only … but also", triplets, "optimistically vague conclusions". Nonexperts wrongly treat any "fancy" word or neutral tone as AI.
- Strength: well-supported
- Implication for CRISP: do not ship a word-swap filter. Rules must change structure (cut the claim, give the fact) not vocabulary alone.

### F5. Style words, not content words, drive the 2024 vocabulary shift
- Evidence: Kobak, González-Márquez, Horváth, Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary", 2024/2025. https://arxiv.org/abs/2406.07016 (read PDF). 379 excess style words in 2024, 66% verbs, 14% adjectives. delves r=28.0, underscores 13.8, showcasing 10.7; potential, findings, crucial top by frequency gap. Lower bound 13.5% of abstracts.
- Strength: well-supported
- Implication for CRISP: the problem is verbs and adjectives ("underscores", "showcases", "crucial"). Prefer plain verbs (shows, is, has) and delete adjectives that carry no measurement.

### F6. Over-used words spread into human speech, and lists go stale
- Evidence: Yakura et al., "Empirical evidence of Large Language Model's influence on human spoken communication", 2024–25. https://arxiv.org/abs/2409.01754 (delve, showcase, boast, intricacies, meticulous; N=496 experiment). Wikipedia notes delve "dropped off sharply in 2025" and Grok favors "causal, empirical, correlate".
- Strength: well-supported (spread); reasonable hypothesis (decay)
- Implication for CRISP: a word list is a snapshot. Anchor the rule on function ("no filler intensifiers or significance verbs") and give the list as examples.

### F7. Sycophancy is trained in by preference data
- Evidence: Sharma et al. (Anthropic), "Towards Understanding Sycophancy in Language Models", 2023. https://arxiv.org/abs/2310.13548. Five assistants sycophantic; humans and PMs sometimes prefer convincing sycophantic answers over correct ones.
- Strength: well-supported
- Implication for CRISP: praise openers ("Great question!") are a symptom of an optimization pressure, so the rule must be explicit and must forbid unearned agreement, not just exclamation marks.

### F8. A shipped model was rolled back for being flattering
- Evidence: OpenAI, "Sycophancy in GPT-4o: what happened", 2025-04-29. https://openai.com/index/sycophancy-in-gpt-4o/. "overly supportive but disingenuous"; cause: over-weighting short-term thumbs feedback.
- Strength: well-supported
- Implication for CRISP: praise and validation are a failure mode, not politeness. Warmth stays; flattery goes.

### F9. Labs explicitly prescribe directness and also give contradicting defaults
- Evidence: OpenAI Model Spec. Be clear and direct: "lucid, succinct, and well-organized… Formatting (such as bold, italics, or bulleted lists) should be used judiciously… avoid 'purple prose,' hyperbole, self-aggrandizing, and clichéd phrases"; "phrased as a direct answer rather than a list of facts"; "avoid repeating the user's prompt, and generally minimize redundant phrases"; "avoid… trying to wrap things up (e.g., ending… 'Enjoy!')"; good-vs-bad pair "Paris is the capital of France." https://github.com/openai/model_spec (read raw main) and https://model-spec.openai.com/2025-04-11.html. Spec also says "Certainly!" as an opener is a violation example.
- Strength: well-supported (as lab policy; not as measured effect)
- Implication for CRISP: lead with the answer; one good/bad pair beats a paragraph of rule. Note the Spec also keeps "How can I assist you today?" as GOOD, so closers can be conditionally fine.

### F10. Anthropic's own docs say positive instruction beats prohibition, and give verbosity wording
- Evidence: "Prompting best practices" (Claude docs). "Tell Claude what to do instead of what not to do" ("smoothly flowing prose paragraphs"); sample block says reserve markdown for code and simple headings, avoid bold/italics, and "NEVER output a series of overly short bullet points"; migration note: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...'". https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices. Opus 5 page: "Keep disclaimers and caveats short, and spend most of the response on the main answer"; "do not pad with filler sections, redundant summaries, or boilerplate"; "lead with the outcome". https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Strength: well-supported (vendor-tested; Opus 5 verbosity is model-specific)
- Implication for CRISP: write rules as "do X" ("first sentence answers the question") with the reason. Keep the ban list short.

### F11. Claude.ai system prompt: prose by default, lists when content is multifaceted
- Evidence: Claude Sonnet 5.5 system prompt, 2026-09-28. https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-5-5.md. "In typical conversation and for simple questions Claude keeps a natural tone and responds in prose rather than lists or bullets unless asked"; "Claude never uses bullet points when declining a task". Wikipedia notes newer apps "have instructions to avoid overuse of boldface."
- Strength: stylistic preference (vendor)
- Implication for CRISP: structure must be earned. Prose for reasoning and explanation; lists for parallel items, steps, options.

### F12. LLMs under-express uncertainty and humans reward confidence
- Evidence: Zhou, Hwang, Ren, Sap, "Relying on the Unreliable", 2024. https://arxiv.org/abs/2401.06730. 47% error among confident responses; users rely on outputs "whether or not they are marked by certainty"; preference data is "biased against texts with uncertainty". OpenAI Model Spec lists "expressing uncertainty" as an execution-error mitigation.
- Strength: well-supported (abstract level; I did not read full results on hedge phrasing)
- Implication for CRISP: delete ritual hedges ("might", "it's worth noting") but state real uncertainty once, with a confidence word and what would resolve it.

### F13. Refusal and caveat bloat is measurable
- Evidence: Röttger et al., "XSTest", 2023. https://arxiv.org/abs/2308.01263 (250 safe prompts models should not refuse). OpenAI Model Spec: "Providing helpful context without imposing a subjective moral judgment" as the compliant pattern.
- Strength: well-supported (existence); stylistic preference (exact wording)
- Implication for CRISP: caveats and refusals follow the same rule as any sentence: include only if it changes the reader's action. Say what you can't do in one clause plus the alternative.

### F14. Compact reasoning can keep accuracy; compact answers need the same test
- Evidence: Xu et al., "Chain of Draft: Thinking Faster by Writing Less", 2025. https://arxiv.org/abs/2502.18600. Matches or beats CoT with as little as 7.6% of tokens.
- Strength: reasonable hypothesis (reasoning benchmarks, not reader comprehension)
- Implication for CRISP: "minimal but informative" is a valid target for working notes. For human-facing text, test comprehension, not token count.

### F15. Wikipedia warns that removing signs hides the problem
- Evidence: Wikipedia, Signs of AI writing, intro: "Please do not merely treat these signs as the problems to be fixed; that could just make detection harder."
- Strength: reasonable hypothesis
- Implication for CRISP: define quality by what the reader gets (facts, decision, next step), then use the ban list as lint.

## Catalog: anti-patterns by group (47 items)
Format: item → fix. Strongest source and suppression wording follow each group.

**(a) Preamble / postamble**
1. "Sure!" / "Certainly!" / "Absolutely!" opener → start with the answer.
2. "Great question" → delete.
3. "Here's a breakdown / Here is the…" → delete; give the content.
4. "In this response I will…" / "Let's dive in" → delete.
5. Restating the question → delete.
6. "In conclusion / Overall / In summary" restating the body → delete.
7. "I hope this helps / Let me know if…" / "Enjoy!" → delete unless a real choice is offered.
8. Sign-off when user hasn't ended → delete.
9. Knowledge-cutoff / "as of my last update" boilerplate → state only date-relevant uncertainty.
10. Leaked chat artifacts ("Here's a template…", fill-in brackets) → deliver the artifact only.
Source: OpenAI Model Spec + Claude migration note (F9, F10). Wording: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...'"; "avoid repeating the user's prompt"; "lead with the outcome: your first sentence should answer 'what happened'".

**(b) Filler vocabulary** (list below)
11. Significance verbs: underscores, highlights, showcases, reflects, fosters → plain verb or delete.
12. Copula avoidance: "serves as", "stands as", "boasts", "features" → is / has.
13. Stock metaphors: tapestry, landscape, realm, journey → literal noun.
14. Intensifier adjectives: crucial, pivotal, vibrant, robust, seamless, comprehensive → delete or give the number.
15. Promotional tone: "nestled", "rich cultural heritage" → neutral fact.
16. Transition openers: Additionally, Notably, Moreover → delete.
17. Vague association: "connected with", "in connection with" → state the relation.
18. "Delve into" and kin → "look at".
Source: Kobak 2024, Russell 2025 (F3, F5). Wording: Model Spec "avoid… hyperbole, self-aggrandizing, and clichéd phrases that do not add to the clarity".

**(c) Hedging / caveats / sycophancy-adjacent**
19. Stacked modals "may potentially suggest" → one hedge or none.
20. "It's important to note" / "worth noting" → say the thing.
21. Blanket disclaimers ("consult a professional") when unasked → drop or one clause.
22. Moralizing before help → help first.
23. Vague attribution ("experts say", "studies show", "widely regarded") → cite one source or drop.
24. "Challenges and future prospects" closing formula → drop unless real and specific.
25. Fake balance ("however, … both sides") on factual questions → answer.
26. Over-refusal with apology paragraph → one clause plus alternative.
Source: Zhou 2024, XSTest, Wikipedia (F12, F13). Wording: "Keep disclaimers and caveats short, and spend most of the response on the main answer."

**(d) Structure / formatting overuse**
27. Bullets for reasoning or narrative → prose.
28. Bold on many phrases, "key takeaways" style → none or at most one per section.
29. Inline-header lists "**Term:** description" → sentences, unless truly a glossary.
30. Headings on short answers → none.
31. Headings that contain only headings → flatten.
32. Title Case headings → sentence case.
33. Emoji bullets or headers → none.
34. Tiny two-row tables → one sentence.
35. Thematic break between every section → drop.
36. Title heading repeating the topic → drop.
37. Em dashes in place of commas/colons → use plain punctuation.
38. Overlong bullet lists of one-word fragments → "NEVER output a series of overly short bullet points."
Source: Wikipedia + Claude docs (F2, F10, F11). Wording: "Formatting… used judiciously to aid the user in scanning"; "reserve markdown primarily for inline code, code blocks, and simple headings".

**(e) Repetition / restating**
39. Intro previews structure, body does it, outro recaps → say once.
40. Same claim re-said in new words in adjacent sentences → delete the second.
41. Echoing user's wording back ("It's great that you're walking your dog") → respond to content.
42. "Not only X but also Y" / "It's not X, it's Y" contrast frames → state Y.
43. Rule-of-three lists padded for rhythm → keep real items only.
44. Trailing "-ing" analysis ("…highlighting its importance") → delete clause.
Source: Model Spec, Wikipedia (F9, F2). Wording: "generally minimize redundant phrases and ideas"; "do not pad with filler sections, redundant summaries, or boilerplate."

**(f) Tone**
45. Fake enthusiasm / exclamation marks → neutral, warm if relevant.
46. Praise of the user's question or idea → react to substance.
47. Agreeing before checking ("You're absolutely right") → verify first, say plainly if wrong.
48. Announcing own diligence ("I've carefully…") → report results.
Source: Sharma 2023, OpenAI 2025 (F7, F8). Wording: Model Spec "shouldn't just say 'yes' to everything (like a sycophant)… politely push back"; Claude prompt "accountability without self-abasement, excessive apology".

## Top-30 AI-vocabulary list
Verified in fetched sources. Source tags: K = Kobak 2024; L = Liang 2024 via Kobak related work; G = Gray 2024 via Kobak; Y = Yakura 2024; R = Russell 2025; W = Wikipedia page examples.

delve/delves (K r=28.0, Y, W), underscore/underscores (K 13.8, W), showcase/showcasing (K 10.7, L, Y), potential (K δ=0.052), findings (K δ=0.041), crucial (K δ=0.037, R, W), pivotal (K, L, W), intricate/intricacies (K, L, G, Y), meticulous/meticulously (G, Y, K), realm (L), comprehensive (K), insights (K), enhancing (K), notably (K), additionally (K), particularly (K), exhibited (K), across (K), within (K), boast (Y), tapestry (W), testament (W, R), landscape (W), vibrant (R, W), significantly (R), grappling (K fig. 2), garnered (K fig. 2), valuable (K fig. 2), highlights (K fig. 2, W), fostering (W).

Not verified in any source I fetched: navigate, leverage, robust, seamless, multifaceted. Wikipedia's own table of "AI vocabulary" by era was not extracted by my fetch, so the era split is not reproduced. Note: "across", "within", "potential" are everyday words; the effect is frequency shift in abstracts, not a ban. Caveat from Wikipedia: a word being overused does not mean its synonyms are.

## Research questions
- **What improves clarity?** Answer first; concrete fact over significance claim; one idea per sentence. Model Spec "direct answer rather than a list of facts"; Paris example. Lab policy, not experiment.
- **What reduces ambiguity?** Name sources; state relations exactly (not "associated with"); state uncertainty once with a reason. Wikipedia families "vague attributions", "vague association".
- **What reduces verbosity?** Cut preamble, restatement, recap, caveat stacks. Anthropic's sample: keep caveats short, "do not pad with filler sections". Explicit length instruction is needed for Opus 5, which runs long by default.
- **What improves scanability?** Lead sentence carries the conclusion; lists only for parallel or sequential items; few bold spans. Model Spec "judiciously… to aid scanning". Overuse is itself a tell (Wikipedia).
- **Natural vs artificial?** Artificial: stock metaphors, "-ing" commentary, contrast frames, triplets, uniform sentence length, enthusiasm. Natural: short plain verbs, uneven rhythm, specifics. Experts note humans repeat "says" where AI varies to "notes/explains" (Russell, o1-Pro section).
- **What saves/wastes tokens?** Wastes: preamble, recap, restating, bullets with bold headers, caveats. Saves: answer-first, prose, one hedge. Chain of Draft shows reasoning can shrink to 7.6% of tokens without accuracy loss on benchmarks (F14).
- **Specs vs answers vs coding agents?** Evidence is thin for specs. Claude docs say lead progress updates with the outcome and use positive examples; Opus 5 page warns against over-verification and padded documents. For agents, apply the same rules to status text. [INFERENCE for specs.]
- **What can LLMs follow reliably?** Short positive instructions with a reason, one good/bad pair, and an explicit length target (Claude docs; GPT-4.1 guide says "a single sentence firmly and unequivocally clarifying your desired behavior is almost always sufficient"). Long ban lists risk over-triggering; Claude docs warn aggressive language "may now overtrigger".
- **Evidence vs preference?** Evidence: word-frequency shifts (F5, F6), human detection rates (F3), sycophancy origin (F7, F8). Preference or lab policy: bullet and bold limits, closers, em-dash rule. Wikipedia's list is observational and says so.

## Sources
1. Wikipedia: Signs of AI writing. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (fetched, ~1000 of 2133 lines read: Content, Language, Style, Communication sections)
2. Kobak et al. 2024/2025. https://arxiv.org/abs/2406.07016 (fetched PDF)
3. Russell, Karpinska, Iyyer, ACL 2025. https://arxiv.org/abs/2501.15654 (fetched v2 HTML)
4. Yakura et al. https://arxiv.org/abs/2409.01754 (abstract fetched)
5. Liang et al. 2024, https://arxiv.org/abs/2403.07183 and https://arxiv.org/abs/2404.01268 (abstracts fetched; the "Delving into ChatGPT usage in academic writing" paper by Liang was not fetched, I cite Liang's top words only via Kobak)
6. Sharma et al. 2023. https://arxiv.org/abs/2310.13548 (abstract fetched)
7. OpenAI, Sycophancy in GPT-4o. https://openai.com/index/sycophancy-in-gpt-4o/ (fetched)
8. Zhou et al. 2024. https://arxiv.org/abs/2401.06730 (abstract fetched)
9. Röttger et al., XSTest. https://arxiv.org/abs/2308.01263 (abstract fetched)
10. OpenAI Model Spec. https://github.com/openai/model_spec/blob/main/model_spec.md and https://model-spec.openai.com/2025-04-11.html (fetched; style sections read from raw main)
11. Anthropic, Prompting best practices. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (fetched)
12. Anthropic, Prompting Claude Opus 5. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 (fetched)
13. Anthropic, Claude Sonnet 5.5 system prompt. https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-5-5.md (fetched)
14. OpenAI, GPT-4.1 Prompting Guide. https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide (fetched; verbosity-specific guidance not found in the portion read)
15. Xu et al., Chain of Draft. https://arxiv.org/abs/2502.18600 (abstract fetched)
