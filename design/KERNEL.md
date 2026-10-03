# CRISP kernel — design brief for all writers

This is the source of truth. Every section of CRISP.md, every prompt, and every example must agree with it. Writers expand it; they do not change rules, add rules, or rename terms. If something here looks wrong, message the parent, don't fix it locally.

## What CRISP is

CRISP (Concise · Relevant · Intuitive · Simple · Protocol) is a writing protocol for humans and LLMs. Voice: a competent engineer talking to another competent engineer who respects their time. It is conversational, not chatty. It is a protocol because compliance is checkable: each rule has a yes/no test.

Canonical definitions:

- **crispify** (verb): rewrite text using CRISP while preserving its useful meaning. "Crispify this", "make this crispier", "CRISP this", "run a CRISP pass", "/crisp" all request the same transformation.
- **CRISP pass**: the nine-step transformation (below) applied to a draft, by a human or by an LLM before it answers.
- **useful meaning**: facts, decisions, numbers, code, conditions, risks, and uncertainty that change what the reader knows, does, or decides.
- **useful information density**: useful meaning per word. CRISP maximizes it without making the reader decode anything.

## Priorities (in order, from the brief)

1 minimal ambiguity · 2 ease of understanding · 3 ease of scanning · 4 relevance · 5 conversational language · 6 simplicity · 7 concision · 8 low token usage.

Consequence: never trade precision for length. Compress ideas (drop what doesn't matter) before compressing words. Stop compressing when the reader would have to decode.

## The five principles (one line each; CRISP.md expands each to ~80-120 words)

- **Concise**: say everything necessary, nothing unnecessary. Concise ≠ terse: keep words that carry meaning, precision, structure, or tone.
- **Relevant**: include what helps the current question or task. Drop the related, interesting, generic, obvious, repetitive, defensive, and decorative. Add unasked information only when it prevents a likely mistake, changes the decision, exposes a risk, or resolves ambiguity.
- **Intuitive**: understood on first read. Natural sentence order, familiar words, predictable organization, visible relationships between ideas.
- **Simple**: the simplest language that keeps the required precision. "Use the cached value", not "utilize the previously persisted cached representation". Simple ≠ imprecise.
- **Protocol**: explicit, repeatable rules for wording, selection, structure, ambiguity, context, formatting, length, and tokens, each with a check.

## The ten core rules

Each rule: name, one-line statement, the check, the reason (one clause). This exact list is the quick reference.

1. **Answer first.** The first sentence is the answer, decision, result, or ask. Check: can the reader stop after sentence one and know the point? Reason: readers scan and stop early; truncation should lose the least.
2. **Say it once.** No preview of what's coming, no recap of what was said, no restating the question or context the reader already has. Check: does any sentence repeat another, the prompt, or shared context? Reason: redundancy measurably hurts comprehension and costs tokens.
3. **Keep what changes action.** Every sentence changes what the reader knows, does, or decides. Check: delete the sentence; does anything break? If not, it's gone. Reason: padding costs attention and accuracy, not just tokens.
4. **Plain words, same words.** Common verbs and nouns; one term per concept, reused exactly; no synonyms for variety. Check: can every word be replaced by a simpler one with the same meaning? Is any thing called by two names? Reason: inflated vocabulary slows readers; renamed things look like different things.
5. **Name the actor, state the condition.** Who does what, and when: "If X, do Y." "X failed because Y." Check: does every instruction have a subject and every condition a consequence? Reason: missing actors and implicit conditions are the main source of ambiguity in specs and agent tasks.
6. **Replace vague with checkable.** "Soon", "appropriate", "usually", "etc." become a number, a name, a condition, or a stated unknown. Check: could two competent readers act differently on this sentence? Reason: vague words hide missing information; the fix is to supply it, not to ban the word.
7. **Structure is earned.** Prose by default. Numbered list for sequence or priority, bullets for parallel independent items, table for items sharing 2+ attributes, heading only at a real topic boundary, bold for at most one anchor per section, code block for literal code or commands. Check: does each formatting element make the content easier to find or follow? Reason: formatting that doesn't aid scanning is decoration, and over-formatting is itself a mark of generic AI text.
8. **Short is not cryptic.** Keep code, corrections of wrong premises, risks, and real uncertainty (stated once, with what would resolve it). No telegraphese, no dropped articles, no private notation unless shared. Check: would a competent colleague with no context understand it on first read? Reason: concision that forces decoding has lost; concision instructions measurably hurt accuracy when they cut corrections or reasoning.
9. **Sound like a colleague.** Contractions, direct address, light emphasis are fine. No flattery, fake enthusiasm, ceremony, apology, moralizing, or ritual hedges. Disagree plainly. Check: would you say this sentence out loud to a peer? Reason: sycophancy and ceremony are trained-in artifacts, not politeness; they cost trust.
10. **Stop.** When the useful thing has been said, end. No closing summary, no "let me know", no offer of more. Check: does the last sentence still carry useful meaning? Reason: closers restate or decorate.

## Domain rules (CRISP.md sections expand these; keep the rule text, add examples)

### Sentence rules
- One main idea per sentence. Split sentences past ~25 words when they carry two ideas; no hard cap.
- Important information first, in the sentence and in the paragraph.
- Active voice with a named actor when the actor matters; passive is fine when the actor is unknown or irrelevant ("the key was rotated").
- Concrete nouns, strong verbs, common words. Fix hidden verbs: "make a decision" → "decide".
- Condition before consequence: "If login fails, show the error." Cause next to effect: "X failed because Y."
- No nested conditions beyond one level; split long condition chains into a list.
- Patterns: "If X, do Y." "When X, do Y." "Do not X." "Only X when Y." "X failed because Y." "Use X instead of Y." "X, because Y."

### Vocabulary rules
- One term per concept; reuse exactly. Define a term once if the reader may not know it; never rotate synonyms.
- Plain verbs: is, has, shows, uses, means. Not: serves as, boasts, leverages, utilizes, underscores, showcases, facilitates.
- Delete intensifiers and significance adjectives that carry no measurement: very, really, crucial, pivotal, robust, seamless, comprehensive, significant (unless a number follows).
- Delete transition openers that add no logic: Additionally, Notably, Moreover, Furthermore. Keep "but", "so", "because" when they carry logic.
- Expand acronyms on first use unless the reader shares them.
- Normative keywords MUST / SHOULD / MAY (uppercase, RFC 2119 sense) only when the force distinction matters, as in specs. Otherwise plain words: do, don't, only, always, never, if, when, before, after, can, should.
- Compact notation (→, x1, N/A, etc.) only when the reader already uses it.

### Ambiguity rules
- Hedges and vague words are acceptable when they state the real state of knowledge ("probably the cache; I haven't confirmed"). They are unacceptable when they hide information the writer has or should get. Test: can the vague word be replaced by a number, a name, a condition, or "unknown"? If yes, replace it.
- Specific replacements: probably/usually/generally → how often or when, or "unknown"; soon/later → a time or trigger; appropriate/reasonable/as needed/if possible/where appropriate → the actual criterion; sometimes/potentially → the condition; etc./and so on → the full list or "such as A and B" with the scope stated; large/fast/small → a number or a comparison with a reference.
- Pronouns: "this", "it", "they" always have one obvious antecedent in the previous sentence; otherwise repeat the noun.
- "and/or" → "A, B, or both" or just "or".
- Relative terms need a reference point: "faster" than what.
- Hidden assumptions and implicit conditions are stated: "This assumes Redis is reachable."
- Scope is explicit: what is in, what is out.
- Quantities and timing are numbers with units; placeholders (TBD) carry an owner and date.
- Overloaded terms get one meaning for the whole document; say which.

### Relevance rules
- Test for each paragraph, bullet, row, example, caveat: does the reader need this now to act or decide?
- Do not include because it is interesting, related, known, impressive, or anticipates an unlikely follow-up.
- Do include when it prevents a likely mistake, changes the decision, exposes a risk, resolves ambiguity, or is necessary context the reader lacks.
- Answer what was asked. One sentence of unasked information is allowed when it prevents a mistake; it is marked ("Note:") so the reader can skip it.
- Correcting a wrong premise is always relevant.

### Structure rules
- Shape follows content: simple answer → sentence(s); procedure → numbered steps; comparison → one-line verdict + table or bullets; complex subject → TL;DR + sections; spec → requirements grouped by subject; research → findings first, evidence second.
- Progressive disclosure: answer → important details → optional depth. The reader can stop after any layer.
- Headings only at real topic boundaries in long responses; never on short answers; sentence case; never a heading per sentence.
- Bullets: flat, one line to two sentences each, parallel structure, 3-7 per list; no nesting beyond one level; no one-item lists; no bullets for reasoning or narrative.
- Numbers only for sequence or priority.
- Tables when 3+ items share 2+ attributes; never a two-row table; no prose duplicating the table.
- TL;DR at the top when the response is long and the conclusion matters more than the detail; it contains the conclusion, not an announcement; never repeated at the bottom.
- Code blocks for literal code, commands, paths, config; inline code for identifiers.
- Warnings/callouts: one line, only when ignoring it causes damage.
- Whitespace: one blank line between units; no decorative separators, icons, labels, or repeated section intros.

### Token-efficiency rules
- Semantic compression first: remove ideas that don't change action. Then linguistic compression: shorten what remains.
- Cut: duplicated context, repeated conclusions, repeated examples, stylistic synonyms, ceremony, unneeded transitions, obvious explanations, filler adjectives/adverbs, unneeded qualifiers, background the reader has, prose that duplicates a table, summaries that duplicate the body, re-explanations of established context.
- Refer, don't paste: file paths, IDs, links, earlier message, instead of re-quoting content the reader can see.
- Stop compressing when a competent colleague would need to decode.
- Never cut: code the reader needs, a correction, a risk, a real uncertainty, a definition the reader lacks.

### Response-length rules (adaptive; starting points, not caps)
- Simple factual question: 1-4 sentences.
- Simple technical question: direct answer + essential explanation (one short paragraph).
- Troubleshooting: likely cause → how to verify → fix.
- Comparison: one-line verdict + bullets or compact table.
- Procedure: numbered steps, each one action.
- Complex technical subject: TL;DR + structured detail.
- Specification: requirements grouped by subject, each checkable.
- Research: findings first, evidence second.
- Status update: state (done / in progress / blocked) → what changed → asks/risks.
- Agent-to-agent: goal, output shape, scope and non-goals, done-check; results: state + pointer to the artifact.
- More available information never makes an answer longer; the question does.

### Formatting rules
- Headings for real topic boundaries; bullets for independent items; numbers for sequence/priority; tables for genuine comparison; bold for one high-value anchor per section; code blocks for literal code/commands.
- Avoid: heading on short answers, bold on many phrases, "**Term:** description" lists in place of sentences, nested bullets, decorative separators, icons/emoji, labels, title-case headings, a title restating the question, repeated section intros, em dashes as the default connector.

### Context rules
- Established conversation context is shared memory: don't restate the project, requirements, constraints, previous decisions, definitions, or facts the user just gave.
- Restate only to resolve ambiguity, and then in one clause ("the Redis path, not the DB path").
- Floor: state what the reader can't see: goal, constraints, definitions, assumptions. Test: could a competent engineer with zero history act on this?
- A correction names what it replaces: "Ignore the earlier retry limit; use 3."
- Refer by pointer (path, ID, link, "your message above") instead of pasting.
- Give the whole task up front; don't trickle requirements across turns.

### Repetition rules
- Don't preview then repeat; don't repeat the conclusion; don't repeat the question; don't quote the prompt back; don't repeat known context; don't give a table and prose with the same content; don't add a closing summary.
- TL;DR goes at the top, once.
- Repetition is allowed only for safety-critical warnings, and then once more at the point of use.

### Anti-patterns (CRISP.md gives the full catalog grouped a-f with fix for each; this is the shape)
- (a) Preamble/postamble: "Sure!", "Great question", "Here's a breakdown", "In this response I will", restating the question, "In conclusion / In summary", "I hope this helps", "Let me know if", knowledge-cutoff boilerplate.
- (b) Filler vocabulary: delve, underscore, showcase, crucial, pivotal, robust, seamless, comprehensive, tapestry, landscape, realm, leverage, utilize, facilitate, "serves as", "boasts", Additionally/Notably/Moreover.
- (c) Hedging/caveats: stacked modals, "it's important to note", blanket disclaimers, moralizing, vague attribution ("experts say"), fake balance on factual questions, apology paragraphs.
- (d) Formatting overuse: bullets for reasoning, bold everywhere, inline-header lists, headings on short answers, title case, emoji, two-row tables, separators, title restating the topic.
- (e) Repetition: preview+body+recap, same claim twice, echoing the user, "not only X but also Y", rule-of-three padding, trailing "-ing" commentary ("...highlighting its importance").
- (f) Tone: fake enthusiasm, praising the question, "You're absolutely right" before checking, announcing diligence ("I've carefully...").

## The CRISP pass (crispification)

1. Find the message: what must the reader know or do? Write that sentence first.
2. Cut what doesn't change action (relevance).
3. Cut repeats: previews, recaps, restated question or context, duplicate table/prose.
4. Lead with the answer; order the rest by importance.
5. Resolve ambiguity: vague word → number/name/condition/"unknown"; pronoun → noun; implicit condition → "If X"; actor named.
6. Simplify wording: plain verbs, hidden verbs fixed, intensifiers and transitions cut, one term per concept.
7. Shape it: prose, list, table, or heading only where it aids scanning; TL;DR only if long.
8. Check: meaning preserved; nothing the reader needs was cut; a colleague would get it on first read.
9. Stop.

Steps 2-3 before 6: ideas before words.

## Levels (optional depth; all levels obey all rules)

- **CRISP 1 — compact**: the answer and what is essential to act. No optional depth, no alternatives, no rationale unless asked. Use for agent-to-agent, status pings, quick answers, when the reader said "short".
- **CRISP 2 — default**: answer + important details + one line of optional depth when it prevents a likely mistake. Use for normal replies, debugging, explanations.
- **CRISP 3 — detailed**: answer + details + depth: rationale, alternatives, edge cases, risks. Still no repetition or filler. Use for specs, plans, design discussions, research summaries, docs.

Levels control depth, not writing quality. Invocation: "/crisp 1", "CRISP 3", "crispify at level 1".

## Compliance checklist (final form, 14 questions)

1. Did I answer in the first sentence?
2. Is every sentence relevant to what was asked?
3. Did I say anything twice (preview, recap, restated question)?
4. Did I restate context the reader already has?
5. Can any sentence be deleted without losing useful meaning?
6. Is anything vague where a number, name, or condition exists?
7. Is each concept called by one name?
8. Does every heading, list, table, and bold earn its place?
9. Is there an introduction or a closing summary?
10. Did I answer more than was asked?
11. Does it sound like a colleague talking?
12. Is it concise without being cryptic?
13. Did I keep the code, corrections, risks, and real uncertainty?
14. Did I stop?

## The three prompts (frozen text lives in skills/crisp/prompts/; writers quote, don't restate)

- `/crisp` (30-80 words): inject into a live conversation; "apply CRISP to all following output unless told otherwise".
- CRISP Minimal (100-200 words): system prompt when context size matters.
- CRISP Full (300-600 words): system prompt when compliance matters more than overhead.

All three carry the same core behavior: answer first; say it once; keep what changes action; plain and consistent words; explicit actors and conditions; checkable over vague; earned structure; short not cryptic; colleague voice; stop.

## Writing the document itself

CRISP.md must be CRISP. Rule with reason and one before/after pair beats a paragraph of rule. Sentence-case headings. No em-dash habit. No "In this section". No closing summaries. Markdown headings `##` for the 24 numbered sections, `###` inside.
