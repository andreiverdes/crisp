# CRISP

**Concise · Relevant · Intuitive · Simple · Protocol**

A writing protocol for humans and LLMs. Say the useful thing once, as clearly as possible, then stop.

Start here: section 7 (the ten rules), section 22 (one-screen reference), section 23 (drop-in prompts). The skill lives in `skills/crisp/`; `python3 skills/crisp/scripts/install.py` adds CRISP to a project's `AGENTS.md` or `CLAUDE.md`.

## Contents

1. [Research summary](#1-research-summary)
2. [Key findings](#2-key-findings)
3. [Design decisions](#3-design-decisions)
4. [CRISP definition](#4-crisp-definition)
5. [CRISP philosophy](#5-crisp-philosophy)
6. [The five CRISP principles](#6-the-five-crisp-principles)
7. [Core rules](#7-core-rules)
8. [Sentence rules](#8-sentence-rules)
9. [Vocabulary rules](#9-vocabulary-rules)
10. [Ambiguity rules](#10-ambiguity-rules)
11. [Relevance rules](#11-relevance-rules)
12. [Structure rules](#12-structure-rules)
13. [Token-efficiency rules](#13-token-efficiency-rules)
14. [Response-length rules](#14-response-length-rules)
15. [Formatting rules](#15-formatting-rules)
16. [Context rules](#16-context-rules)
17. [Repetition rules](#17-repetition-rules)
18. [Anti-patterns](#18-anti-patterns)
19. [Crispification process](#19-crispification-process)
20. [Before/after examples](#20-beforeafter-examples)
21. [Benchmark results](#21-benchmark-results)
22. [Quick reference](#22-quick-reference)
23. [Compact system prompts](#23-compact-system-prompts)
24. [Compliance checklist](#24-compliance-checklist)

## 1. Research summary

CRISP draws on five research lanes: controlled language and requirements standards, plain-language and readability research, LLM prompting and verbosity studies, agent and context-engineering practice, and AI-writing anti-patterns. Each lane read primary sources where reachable, tagged every finding by strength, and marked inference as inference. The table merges the approaches across lanes and shows what CRISP took and rejected.

Citations like (plain F3) point to a finding in `research/lanes/`: controlled = controlled-language.md, plain = plain-language-readability.md, prompting = llm-prompting-research.md, agents = agents-and-context-engineering.md, ai-writing = ai-writing-antipatterns.md.

| Approach | Useful ideas | Problems | Use in CRISP? |
|---|---|---|---|
| ASD-STE100 (Simplified Technical English, STE) | One word, one meaning; imperative steps | Closed dictionary; tense and modal bans | partly: take consistency, skip dictionary |
| EARS (Easy Approach to Requirements Syntax) | Condition-first clause order | "The system shall" boilerplate; one case study | partly: take order, drop "shall" |
| RFC 2119 / 8174 | Few keywords; uppercase only; use sparingly | Silent on prose style | yes: MUST/SHOULD/MAY when force matters |
| INCOSE GtWR (Guide to Writing Requirements), NASA SEH (Systems Engineering Handbook) App. C | Vague-term lists; explicit conditions; positive form | Bans "and/or/but" and parentheses; contract voice | partly: take ambiguity rules, drop syntax bans |
| NASA FRET (Formal Requirements Elicitation Tool) | Slot checklist: scope, trigger, response, timing | Built for formal verification; robotic prose | no: slots never shape prose |
| Controlled natural languages (Kuhn's PENS: Precision, Expressiveness, Naturalness, Simplicity) | Names the precision-naturalness trade-off | Descriptive taxonomy; no rule set | yes: frames CRISP's target |
| Requirements smells (Femmer) | Detectable smells; word lists | 59% precision; context-dependent | partly: flag, never ban |
| Federal plain language | Hidden verbs; simple-word swaps; one idea per sentence | Rules cite books, not experiments | yes: word and verb rules |
| Microsoft and Google style guides | Conditions first; contractions; no "simply/just" | Documentation-specific; some rules legal | yes: closest voice match |
| NN/g (Nielsen Norman Group) scanning, inverted pyramid | Concise + scannable + objective: +124% usability | Web pages; 1997 sample; pyramid untested | yes: scanning rules; no F-layout |
| Cognitive load, redundancy effect | Duplication hurts learning; ~4 chunks | Learning studies; reverses for novices | yes: say once, chunk lists |
| LLM instruction research (IFScale, a 500-instruction benchmark) | Padding hurts reasoning; more rules, less compliance | Benchmarks; many read at abstract level | yes: few ranked rules, no padding |
| Concision vs accuracy research | "Be concise" cuts length ~49% on easy tasks | Hurts math and false-premise rebuttals | partly: concise output, never cut corrections |
| Length bias in RLHF and judges | Explains LLM bloat and flattery | Diagnosis only; no writing rules | partly: counter it; judge length-controlled |
| Lab system prompts (Claude Code, Codex, Claude.ai, Model Spec) | Banned openers; answer first; positive examples | Numeric caps; labs contradict each other | partly: take ban list, drop caps |
| Context engineering (Anthropic, Manus, Breunig) | Smallest high-signal set; pointers; full spec up front | Principles; little ablation data | yes: don't restate, with a floor |
| Agent files (AGENTS.md, CLAUDE.md, Cursor rules) | Only non-inferable lines; deletion test | Overviews bloat; measured gain small | yes: deletion test, one emphasis |
| AI-writing signs (Wikipedia, Kobak, Russell) | Tell catalog; experts spot AI ~93% | Descriptive; word lists decay | partly: ban list as lint, rule on cause |

## 2. Key findings

1. Redundancy hurts comprehension and learning; it is not neutral. Controlled experiments favor removing duplicate information, with limits for novices (well-supported; plain F3, F4).
2. Filler lowers model accuracy, and verbose answers are often the uncertain ones. Padding degraded reasoning far below the context limit; verbosity compensation tracked higher uncertainty (well-supported; prompting F2, F8).
3. Compliance falls as instruction count rises; one benchmark also found earlier instructions win (prompting F3). A short ranked list beats an exhaustive one (well-supported).
4. Concision instructions can hurt corrections and math. "Answer briefly" lowered hallucination resistance because rebuttals need space (well-supported that the effect exists; vendor blog and weak-model conditions; prompting F7).
5. Training and judges reward length and agreement, so default LLM style bloats and flatters. Praise openers are an optimization artifact, not politeness (well-supported; prompting F9, ai-writing F7, F8).
6. One name per concept is STE's most transferable rule (well-supported; controlled F2).
7. Vague-word detectors reach about 59% precision at best, so flag the words and don't ban them. The fix is to supply the missing number, name, or condition (well-supported; controlled F8).
8. Kuhn's PENS frames the trade-off: CRISP keeps full expressiveness and naturalness and reduces ambiguity by word-level and structure-level conventions, with no grammar to learn (well-supported as taxonomy; controlled F9).
9. Readers scan, and answer-first is safe against truncation. Concise, scannable, objective text measurably helped; working memory holds about 4 chunks, not 7 (scanning well-supported, answer-first a reasonable hypothesis; plain F1, F5, F6, F7).
10. Active-voice mandates lack experimental support. Keep the named actor, and allow passive when the actor is unknown or irrelevant (stylistic preference; plain F10).
11. Production formatting rules disagree across labs, especially on bullets. CRISP picks per medium: prose for reasoning, flat bullets for parallel items (stylistic preference; agents F8).
12. Delegation messages need goal, output shape, scope, and a done-check. Terse hand-offs caused duplicated work, so agent messages are complete, not minimal (well-supported; agents F9).
13. AI text has measurable tells: style verbs and adjectives, plus structural patterns such as "not only X but also Y". Frequent LLM users spot it at about 93%, and paraphrase doesn't hide it (well-supported; ai-writing F3, F4, F5).
14. Positive instruction beats prohibition, and over-emphatic wording overtriggers. Write rules as "do X, because Y" with one good/bad pair (well-supported by vendor testing; prompting F4, F13, ai-writing F10). Giving the reason is a stylistic preference.

## 3. Design decisions

CRISP uses STE's one-meaning consistency and imperative steps but rejects its dictionary, tense bans, and hard word caps, because conversational English is a core requirement. STE's rules serve maintenance manuals, and its own writers call the result blunt and repetitive (controlled F1, F2, F3).

CRISP uses EARS's condition-first order ("When X, do Y") but rejects "shall", because the plain form is as testable and sounds like a colleague. EARS rests on one case study, and its "shall" voice is the legalism to avoid (controlled F4; agents approaches table).

CRISP uses uppercase MUST, SHOULD, and MAY only where force matters, because overuse dilutes the signal. RFC 2119 says to use them sparingly, and RFC 8174 makes only the uppercase forms normative (controlled F5, F6).

CRISP takes the INCOSE and NASA ambiguity rules (defined terms, explicit conditions, no escape clauses) but rejects bans on and/or/but and parentheses, because those bans cannot work in conversation. The useful rules in both guides are ambiguity rules, not syntax rules (controlled F7).

CRISP flags vague words and asks for a number, name, or condition, but never bans them, because detection is imprecise and a hedge can be the exact meaning. Detectors mislabel many exact meanings as vague (controlled F8, F11).

CRISP puts the answer first and discloses detail in layers, because readers scan and truncation should lose the least. NN/g measured scanning benefits (plain F1, F7); the inverted pyramid and answer-first are practitioner convergence, not trial results (plain F6).

CRISP says everything once, because duplicate information measurably hurts comprehension and costs tokens. The redundancy effect holds in controlled experiments, with a floor for novices (plain F3, F4; agents F2).

CRISP defines relevance as "changes what the reader knows, does, or decides" and tests it by deletion, because padding costs attention and accuracy, not just tokens. Input length alone degraded reasoning, and agent-file guidance uses the same deletion test (prompting F2; agents F3, F4).

CRISP treats prose as the default and earns every list, table, heading, and bold, because over-formatting is a tell of generic AI text. Labs agree on prose for reasoning but disagree on bullet limits (agents F8; ai-writing F2, F11).

CRISP never cuts corrections, code, risks, or real uncertainty, because concision that removes them lowers accuracy. Concise-output instructions hurt on math and false premises (prompting F7; agents F1).

CRISP writes rules positively with a reason, keeps few rules, and allows one emphasis, and CRISP.md follows its own rules, because compliance falls as rule count rises and emphatic wording overtriggers. IFScale measured the falling compliance, and vendor testing found the overtriggering (prompting F3, F4, F13; agents F4).

CRISP levels control depth, not quality, because the right length depends on the reader's need and every level must still obey every rule. Labs make length contextual, not fixed (prompting F14; agents F7).

CRISP agent messages carry goal, output shape, scope, and a done-check, plus a pointer to any artifact, because short hand-offs caused duplicated and failed work. Production multi-agent reports and a failure taxonomy both trace failures to thin hand-offs (agents F9, F10, F13).

CRISP never scores compliance by grade level or readability formula, because those measure word and sentence length only. Flesch-Kincaid ignores layout, reader knowledge, and content (plain F9).

## 4. CRISP definition

CRISP (Concise · Relevant · Intuitive · Simple · Protocol) is a writing protocol for humans and LLMs. It produces text a competent reader can read once and act on. The voice is one engineer talking to another who respects their time. It is a protocol because compliance is checkable: each rule has a yes/no test.

CRISP is for anyone whose reader needs to know, do, or decide something: developers, reviewers, and the models they prompt. It covers LLM responses, prompts, specs for coding agents, technical explanations, debugging, status updates, plans, design discussions, research summaries, and agent-to-agent messages.

CRISP must not read like a legal contract, an academic paper, a corporate memo, a military order, a robotic requirements document, or generic AI text. If the result sounds stiff, ceremonial, or padded, the protocol was misapplied.

### Terminology

"Use CRISP.", "Write this in CRISP.", and "/crisp" apply CRISP to all following output. "CRISP this.", "Crispify this.", "Crispify the response.", "Make this crispier.", "Run a CRISP pass.", and "Return the CRISP version." rewrite the given text, and "This isn't CRISP." reruns the pass on the last reply.

- **crispify** (verb): rewrite text using CRISP while preserving its useful meaning.
- **CRISP pass**: the nine-step transformation (section 19) applied to a draft, by a human or by an LLM before it answers.
- **useful meaning**: facts, decisions, numbers, code, conditions, risks, and uncertainty that change what the reader knows, does, or decides.
- **useful information density**: useful meaning per word. CRISP maximizes it without making the reader decode anything.

## 5. CRISP philosophy

CRISP ranks its goals, and the earlier goal wins a conflict: minimal ambiguity, ease of understanding, ease of scanning, relevance, conversational language, simplicity, concision, low token usage. Three things follow. Precision is never traded for length. Low token usage is a result of the other seven, not a target. Concision ranks below conversational language, so CRISP keeps the articles, contractions, and connectives that make text read naturally.

Conversational is not chatty. Conversational means natural word order, "you", contractions, and plain disagreement. Chatty means greetings, praise, enthusiasm, and offers of more help. CRISP keeps the first and cuts the second.

Compress ideas before words. Deleting a paragraph the reader doesn't need saves more than shortening every sentence in it, and it can't make anything cryptic. Shorten wording only after that, and stop when the reader would have to decode.

The target: maximum signal, minimum noise, normal language.

### Three problems CRISP solves

LLM answers blabber: they open with praise, restate the question, and close with a recap (section 2, finding 5). CRISP cuts every sentence that doesn't change action.

LLM answers over-structure. Headings land on three-sentence answers, bold on every phrase, bullets on reasoning. These are recognized marks of generic AI text (ai-writing F2). CRISP makes structure earn its place.

Padding costs tokens and accuracy. Irrelevant input lowers reasoning accuracy well below the context limit (prompting F2). CRISP saves tokens as a side effect of relevance and saying things once, not through telegraphese.

## 6. The five CRISP principles

### Concise

Say everything necessary and nothing unnecessary. Concise is not terse: keep every word that carries meaning, precision, structure, or tone. An answer that drops the one risk the reader needed is short, not concise. CRISP measures useful information density, not word count (section 2, finding 4).

**Before**
> Great question! There are a few different ways you could approach this, but generally speaking, the best option in most cases would probably be to look into using a connection pool.

**CRISP**
> Use a connection pool. Opening a connection per request will exhaust the database's connection limit under load.

### Relevant

Include what helps the current question or task. Drop the related, interesting, generic, obvious, repetitive, defensive, and decorative. Add unasked information only when it prevents a likely mistake, changes the decision, exposes a risk, or resolves ambiguity. Relevance is judged against the question, not the topic: an accurate paragraph about the topic can still be noise.

**Before**
> Python's Global Interpreter Lock has an interesting history going back to the 1990s, and there have been several attempts to remove it. To answer your question, threads won't speed up your loop.

**CRISP**
> Threads won't speed up your CPU-bound loop because of the GIL. Use `multiprocessing.Pool`.

### Intuitive

The reader understands it on first read. That takes natural sentence order, familiar words, predictable organization, and visible relationships between ideas. The reader shouldn't reread a sentence to find its subject or guess how two sentences connect. Connectives like "because", "so", and "but" stay: they carry the logic that fragments and bullets hide.

**Before**
> Deploy blocked. Migration pending. Lock held by job 4411.

**CRISP**
> The deploy is blocked because migration job 4411 still holds the schema lock.

### Simple

Use the simplest language that keeps the required precision: "Use the cached value", not "utilize the previously persisted cached representation". Simple is not imprecise. A technical term the reader knows is simpler than a paraphrase of it, so "idempotent" stays for engineers. Readability formulas don't measure this (plain F9); the check is whether the reader can act.

**Before**
> It is recommended that the timeout value be adjusted to a higher figure.

**CRISP**
> Raise the timeout to 30 seconds.

### Protocol

CRISP is a set of explicit, repeatable rules for wording, selection, structure, ambiguity, context, formatting, length, and tokens, each with a check. "Write clearly" can't be verified; "Does the first sentence state the answer?" can. Checks make CRISP teachable to a model and reviewable by a person. The protocol stays light: no grammar to learn, no closed dictionary, no parser (controlled F9).

**Before**
> Make the response clear and not too long.

**CRISP**
> Answer in the first sentence. Delete any sentence whose removal loses nothing.

## 7. Core rules

### 1. Answer first

The first sentence is the answer, decision, result, or ask.

Check: can the reader stop after sentence one and know the point?

Why: readers scan and stop early; truncation should lose the least (plain F6).

**Before**
> I looked into the failing build. After checking the logs and comparing them with last week's run, it seems the issue is related to the Node version.

**CRISP**
> The build fails because CI moved to Node 22. Pin Node 20 in the CI config.

### 2. Say it once

No preview of what's coming, no recap of what was said, no restating the question or context the reader already has.

Check: does any sentence repeat another, the prompt, or shared context?

Why: redundancy measurably hurts comprehension and costs tokens (plain F3).

**Before**
> You asked how to rotate the key. Here's how to rotate it: run `vault operator rotate`. In summary, `vault operator rotate` rotates the key.

**CRISP**
> Run `vault operator rotate`.

### 3. Keep what changes action

Every sentence changes what the reader knows, does, or decides.

Check: delete the sentence; does anything break? If not, it's gone.

Why: padding costs attention and accuracy, not just tokens (prompting F2).

**Before**
> Caching is a widely used technique in software engineering. Add a 60-second cache to `getPrices()`; the upstream API allows 100 requests per minute.

**CRISP**
> Add a 60-second cache to `getPrices()`; the upstream API allows 100 requests per minute.

### 4. Plain words, same words

Common verbs and nouns; one term per concept, reused exactly; no synonyms for variety.

Check: can every word be replaced by a simpler one with the same meaning? Is any thing called by two names?

Why: inflated vocabulary slows readers (plain F2); renamed things look like different things (controlled F2).

**Before**
> The worker leverages the queue to fetch jobs. Once a task completes, the process utilizes the result handler.

**CRISP**
> The worker reads jobs from the queue. When a job finishes, the worker calls the result handler.

### 5. Name the actor, state the condition

Who does what, and when: "If X, do Y." "X failed because Y."

Check: does every instruction have a subject and every condition a consequence?

Why: missing actors and implicit conditions are the main source of ambiguity in specs and agent tasks (controlled F7, agents F9).

**Before**
> The cache should be invalidated on schema changes.

**CRISP**
> If a migration changes the schema, the deploy script clears the cache.

### 6. Replace vague with checkable

"Soon", "appropriate", "usually", "etc." become a number, a name, a condition, or a stated unknown.

Check: could two competent readers act differently on this sentence?

Why: vague words hide missing information; the fix is to supply it, not to ban the word (controlled F8).

**Before**
> Retry a reasonable number of times and alert the appropriate team.

**CRISP**
> Retry 3 times. If all 3 fail, page the payments on-call.

### 7. Structure is earned

Prose by default. Numbered list for sequence or priority, bullets for parallel independent items, table for items sharing 2+ attributes, heading only at a real topic boundary, bold for at most one anchor per section, code block for literal code or commands.

Check: does each formatting element make the content easier to find or follow?

Why: formatting that doesn't aid scanning is decoration, and over-formatting is itself a mark of generic AI text (ai-writing F2, F11).

*Prompt: "Can I rebase this branch?"*

**Before**
> **Summary**
> - **Short answer:** It depends.
> - **Key consideration:** `git rebase` rewrites commit hashes.

**CRISP**
> Only if nobody else has pulled the branch: `git rebase` rewrites commit hashes.

### 8. Short is not cryptic

Keep code, corrections of wrong premises, risks, and real uncertainty (stated once, with what would resolve it). No telegraphese, no dropped articles, no private notation unless shared.

Check: would a competent colleague with no context understand it on first read?

Why: concision that forces decoding has lost; concision instructions measurably hurt accuracy when they cut corrections or reasoning (prompting F7).

**Before**
> Cfg bad → svc dn. Fix: rb + flag off.

**CRISP**
> The service is down because of a bad config. Roll back the config and turn off the `new_auth` flag.

### 9. Sound like a colleague

Contractions, direct address, light emphasis are fine. No flattery, fake enthusiasm, ceremony, apology, moralizing, or ritual hedges. Disagree plainly.

Check: would you say this sentence out loud to a peer?

Why: sycophancy and ceremony are trained-in artifacts, not politeness; they cost trust (ai-writing F7, F8).

**Before**
> You're absolutely right, what a great idea! One small thought: it might perhaps be worth considering that the index may not be used here.

**CRISP**
> That won't help: the query wraps `email` in `LOWER()`, so the index isn't used. Index `LOWER(email)` instead.

### 10. Stop

When the useful thing has been said, end. No closing summary, no "let me know", no offer of more.

Check: does the last sentence still carry useful meaning?

Why: closers restate or decorate.

**Before**
> Set `max_connections` to 200. I hope this helps! Let me know if you have any other questions.

**CRISP**
> Set `max_connections` to 200.

## 8. Sentence rules

Each sentence carries one idea, leads with what matters, and puts the condition before the consequence. There is no hard sentence-length cap: split past ~25 words only when the sentence carries two ideas. The 25-word figure is house style, not a measured threshold (plain F8).

### One main idea per sentence

**Before**
> The migration locked the orders table for 40 minutes, which is why EU checkout failed, so we should schedule the next one off-peak.

**CRISP**
> The migration locked the orders table for 40 minutes, so EU checkout failed. Schedule the next migration off-peak.

### Important information first

Put it first in the sentence and in the paragraph.

**Before**
> After reviewing all three options and their costs, we recommend Postgres, which is the cheapest.

**CRISP**
> Use Postgres: it's the cheapest of the three options.

### Name the actor when it matters

Use active voice with a named actor when the actor matters. Passive is fine when the actor is unknown or irrelevant ("the key was rotated"). The evidence supports naming the actor, not an active-voice mandate (plain F10).

**Before**
> The rollback should be done before 18:00.

**CRISP**
> Maya rolls back before 18:00.

### Concrete nouns, strong verbs, common words

Fix hidden verbs: "make a decision" becomes "decide".

**Before**
> We need to perform an investigation of the memory usage.

**CRISP**
> We need to investigate memory usage.

### Condition before consequence

"If login fails, show the error." Keep cause next to effect: "X failed because Y." Don't nest conditions beyond one level; split long condition chains into a list (plain F12, controlled F4).

**Before**
> Show the error, unless the user is an admin, in which case log it if logging is on.

**CRISP**
> If the user isn't an admin, show the error. If the user is an admin and logging is on, log it.

### Patterns

These cover most instructions and explanations:

- "If X, do Y." / "When X, do Y."
- "Do not X." / "Only X when Y."
- "X failed because Y." / "X, because Y."
- "Use X instead of Y."

## 9. Vocabulary rules

Use common words, call each thing by one name, and delete words that carry no measurement.

- One term per concept; reuse it exactly. Define a term once if the reader may not know it; never rotate synonyms (controlled F2).
- Plain verbs: is, has, shows, uses, means. Not: serves as, boasts, leverages, utilizes, underscores, showcases, facilitates (ai-writing F5).
- Delete intensifiers and significance adjectives that carry no measurement: very, really, crucial, pivotal, robust, seamless, comprehensive, significant (unless a number follows).
- Delete transition openers that add no logic: Additionally, Notably, Moreover, Furthermore. Keep "but", "so", and "because" when they carry logic.
- Expand acronyms on first use unless the reader shares them.
- Use compact notation (→, x1, N/A) only when the reader already uses it.

| Instead of | Use |
|---|---|
| utilize | use |
| leverage | use |
| facilitate | help |
| in order to | to |
| prior to | before |
| in the event that | if |
| due to the fact that | because |
| is able to | can |
| make a decision | decide |
| perform a check | check |
| serves as | is |
| boasts | has |
| underscores, showcases | shows |
| a number of | some, or the number |
| at this time | now |

The table is a snapshot: the words that mark inflated text drift over time (ai-writing F6). The rule is the function, plain verb over inflated verb, and a listed word stays when it is the exact meaning ("leverage" in a finance doc).

### Normative keywords

Use MUST / SHOULD / MAY (uppercase, RFC 2119 sense) only when the force distinction matters, as in specs. Otherwise use plain words: do, don't, only, always, never, if, when, before, after, can, should. Capitalized keywords on every line dilute the signal (controlled F5), and aggressive "You MUST" wording makes current models overtrigger (prompting F4).

**Before**
> You MUST run the tests before you MAY open a pull request.

**CRISP**
> Run the tests before opening a pull request.

## 10. Ambiguity rules

A sentence that two competent readers could act on differently has failed, however short it is.

### Acceptable and unacceptable hedges

Hedges and vague words are acceptable when they state the real state of knowledge ("probably the cache; I haven't confirmed"). They are unacceptable when they hide information the writer has or should get. Test: can the vague word be replaced by a number, a name, a condition, or "unknown"? If yes, replace it.

Words are not banned mechanically. Vague-word detectors are imprecise (section 2, finding 7): many flagged words are the exact meaning. Cutting a real hedge is also a failure, because LLMs already under-express uncertainty (ai-writing F12). Treat the table as a list of flags.

| Word | Hides | Replace with |
|---|---|---|
| probably, usually, generally | how often, or when | the rate or condition, or "unknown" |
| soon, later | the time | a time or a trigger |
| appropriate, reasonable | the criterion | the actual criterion |
| as needed, if possible, where appropriate | who decides, and by what test | the actual criterion |
| sometimes, potentially | the condition | the condition |
| etc., and so on | the rest of the list | the full list, or "such as A and B" with the scope stated |
| large, fast, small | the threshold | a number, or a comparison with a reference |

### Other sources of ambiguity

- Pronouns: "this", "it", and "they" always have one obvious antecedent in the previous sentence; otherwise repeat the noun. The same applies to "the above" and bare "this".
- "and/or" becomes "A, B, or both" or just "or".
- Relative terms need a reference point: "faster" than what.
- Hidden assumptions and implicit conditions are stated: "This assumes Redis is reachable."
- Scope is explicit: what is in, what is out.
- Quantities and timing are numbers with units; placeholders (TBD) carry an owner and date.
- Overloaded terms get one meaning for the whole document; say which.

Undefined acronyms and inconsistent names are vocabulary problems; section 9 covers them.

**Before**
> Clean up old logs regularly and/or when the disk gets full. This should be handled by the appropriate team.

**CRISP**
> The platform team deletes logs older than 14 days every night, and also whenever `/var/log` passes 80% full.

**Before**
> It's probably a race condition. It fails sometimes.

**CRISP**
> It fails in about 1 of 20 runs, only when two workers claim the same job. Probably a race in `claim()`; I haven't reproduced it locally.

## 11. Relevance rules

Every paragraph, bullet, row, example, and caveat passes one test: does the reader need this now to act or decide?

Don't include something because it is interesting, related, known, impressive, or anticipates an unlikely follow-up. Default LLM output pads with exactly this material (section 2, finding 5).

Do include it when it:

- prevents a likely mistake
- changes the decision
- exposes a risk
- resolves ambiguity
- is necessary context the reader lacks

Answer what was asked. One sentence of unasked information is allowed when it prevents a mistake; it is marked ("Note:") so the reader can skip it. Correcting a wrong premise is always relevant, and it outranks brevity (section 2, finding 4). In a recommendation, the tradeoff that rules out the alternatives is relevant: a verdict without it lost blind pairings to a longer answer that had it (section 21).

Relevance depends on the reader. The same fact is noise for the engineer who wrote the service and necessary context for one who joined today.

**Before**
> Postgres is a powerful open-source relational database, and renaming columns is a common part of schema evolution. You can use `ALTER TABLE ... RENAME COLUMN`. You might also consider migration tools like Flyway or Liquibase, and remember that good naming conventions matter.

**CRISP**
> `ALTER TABLE users RENAME COLUMN fname TO first_name;`
>
> Note: views that use `fname` update automatically; application queries don't.

## 12. Structure rules

Shape follows content: use the form the content already has, and add nothing else.

Section 14 gives the shape and length for each request type. Section 15 says when each formatting element earns its place.

Use progressive disclosure: the answer, then important details, then optional depth. The reader can stop after any layer and still have what they need.

A TL;DR goes at the top only when a long response's conclusion matters more than its detail (section 15).

*Prompt: "Does `git stash` save untracked files?"*

**Before**
> **Overview**
>
> **Short answer:** No.
>
> **Details**
> - By default, `git stash` saves only tracked files.
> - To include untracked files, add `-u`.
>
> **Summary**
>
> Use `git stash -u` to stash untracked files.

**CRISP**
> No. Use `git stash -u` to include untracked files.

## 13. Token-efficiency rules

Save tokens by cutting ideas first and words second, and stop before the reader has to decode.

Semantic compression comes first: remove ideas that don't change action. Then linguistic compression: shorten what remains. In that order, every cut removes noise; in the reverse order, you polish sentences you later delete. When shortening, drop filler and ritual hedges, never facts, names, numbers, or negations (prompting F10).

Cut duplicated context, repeated conclusions, repeated examples, stylistic synonyms, ceremony, unneeded transitions, obvious explanations, filler adjectives and adverbs, unneeded qualifiers, background the reader has, prose that duplicates a table, summaries that duplicate the body, and re-explanations of established context.

Refer, don't paste. Point to file paths, IDs, links, or an earlier message instead of re-quoting content the reader can see; copies go stale (agents F6).

Never cut code the reader needs, a correction, a risk, a real uncertainty, or a definition the reader lacks.

Stop compressing when a competent colleague would need to decode. The compressed version below saves a few tokens and adds a decoding step; it is acceptable only for a reader who already writes that way.

**Before**
> Net timeout → retry x1.

**CRISP**
> Retry once after a network timeout.

## 14. Response-length rules

The question sets the length; the request type sets the shape. These are starting points, not caps: never shorten a correction, a risk, needed code, or reasoning the answer depends on (section 2, finding 4).

| Request type | Shape | Typical length |
|---|---|---|
| Simple factual | The answer | 1-4 sentences |
| Simple technical | Answer, then the essential explanation | One short paragraph |
| Troubleshooting | Likely cause, how to verify, fix | One paragraph or 3-5 steps |
| Comparison | One-line verdict, then bullets or a table | Verdict plus 3-7 rows |
| Procedure | Numbered steps, one action each | One line per step |
| Complex subject | TL;DR, then structured detail | What the reader needs |
| Specification | Requirements grouped by subject, each checkable | One line per requirement |
| Research | Findings first, evidence second | One line per finding |
| Status update | State (done, in progress, blocked), what changed, asks and risks. Incident: the timeline first, every timestamp kept | 3-8 sentences or short bullets |
| Agent-to-agent | Task: goal, output shape, scope and non-goals, done-check. Result: state plus artifact pointer | Four fields; result in 1-4 sentences plus pointer |

**More available information never makes an answer longer; the question does.**

### Levels

Levels control depth, not writing quality. Every level obeys every rule.

- CRISP 1, compact: the answer and what is essential to act. No optional depth, no alternatives, no rationale unless asked. Use for agent-to-agent messages, status pings, quick answers, and when the reader said "short".
- CRISP 2, default: answer, important details, and one line of optional depth when it prevents a likely mistake. Use for normal replies, debugging, and explanations.
- CRISP 3, detailed: answer, details, and depth: rationale, alternatives, edge cases, risks. Still no repetition or filler. Use for specs, plans, design discussions, research summaries, and docs.

Invoke with "/crisp 1", "CRISP 3", or "crispify at level 1". "Where should session data live?" at each level:

> CRISP 1: Use Redis, with a TTL on each session key.
>
> CRISP 2: Use Redis, with a TTL on each session key. Set `maxmemory-policy volatile-ttl` so eviction only removes keys that have a TTL.
>
> CRISP 3: Use Redis, with a TTL on each session key: sessions are small, short-lived, and read on every request. Set `maxmemory-policy volatile-ttl` so eviction only removes keys that have a TTL. If you don't run Redis yet, Postgres works. Risk: a Redis restart without persistence logs everyone out.

## 15. Formatting rules

Format only where it makes content easier to find or follow; the default is prose. No markup format reliably improves model accuracy (prompting F11), so formatting's job is human scanning, and overuse is itself a tell of generic AI text (ai-writing F2, F11).

| Element | Use when |
|---|---|
| Heading | A long response has a real topic boundary the reader may jump to |
| Subheading | A section has parts the reader looks up separately |
| Bullets | 3-7 parallel, independent items, one line to two sentences each |
| Numbered steps | Order or priority matters; one action per step |
| Table | 3+ items share 2+ attributes |
| TL;DR | The response is long and the conclusion matters more than the detail |
| Code block | Literal code, commands, paths, config; inline code for identifiers |
| Example | A format or rule is easier to copy than to describe |
| Warning | Ignoring it causes damage; one line |
| Callout ("Note:") | One unasked sentence that prevents a mistake, marked so the reader can skip it |
| Whitespace | One blank line between units |
| Bold | One high-value anchor per section |

Avoid nested bullets and the overuse patterns in section 18(d).

### TL;DR

Use a TL;DR only when the response is long and the conclusion matters more than the detail. It states the conclusion, not an announcement of what follows. It goes at the top and is never repeated at the bottom.

*Prompt: "My laptop dies even on the dock. Should I replace the dock?"*

**Before**
> TL;DR: There are several factors to consider.

**CRISP**
> TL;DR: The battery is probably failing; test its voltage under load before replacing the dock.

### Over-formatting

*Prompt: "Can I delete `node_modules`?"*

**Before**
> ### Deleting node_modules
>
> **Short answer:** Yes.
>
> **Details:**
> - **Safe:** `node_modules` is **regenerated** by `npm install`.
> - **Time:** Reinstalling may take **some time**.
>
> ---
>
> **Summary:** You can safely delete it.

**CRISP**
> Yes. `npm install` recreates `node_modules` from `package-lock.json`; the reinstall takes about as long as your first install did.

## 16. Context rules

Treat established context as shared memory: don't restate the project, requirements, constraints, previous decisions, definitions, or facts the user just gave. Restate only to resolve ambiguity, and then in one clause ("the Redis path, not the DB path").

### The floor

Not restating has a floor. State what the reader can't see: the goal, constraints, definitions, and assumptions. Vague text that "falsely assumes shared context" fails as badly as over-specified text (agents F2). The test: could a competent engineer with zero history act on this? A subagent, a new teammate, and a reader opening a ticket next month all have zero history.

### Corrections, pointers, and the whole task

A correction names what it replaces: "Ignore the earlier retry limit; use 3." Early wrong context sticks, and requirements trickled across turns cost a 39% average drop in one benchmark (agents F11), so give the whole task up front. Refer by pointer (path, ID, link, "your message above") instead of pasting; a pasted copy goes stale and then contradicts the source (agents F6).

**Before**
> Hi! As you probably know, this is a Go project using Postgres, organized into several packages. We've been discussing the billing service for a while. Could you add the retry logic we talked about to the payment client? Thanks!

**CRISP**
> Add retries to `Charge` in `billing/client.go`: at most 3 retries, exponential backoff from 200 ms, only on 5xx responses and timeouts. Retry only requests that carry an `Idempotency-Key` header, so a retry can't double-charge. Don't change the refund path. Done when `go test ./billing/...` passes.

The rewrite drops what the agent can read from the repo and adds what it can't: the limits, the constraint, the scope, and the done-check.

## 17. Repetition rules

Say each thing once. Redundancy is not neutral: duplicate information measurably hurts comprehension (plain F3).

Don't:

- preview what's coming, then say it;
- repeat the conclusion;
- repeat the question or quote the prompt back;
- repeat context the reader already has;
- give a table and prose with the same content;
- add a closing summary.

TL;DR at the top, once (section 15). The only allowed repetition is a safety-critical warning, stated once more at the point of use: warn at the top that the migration drops the `legacy_orders` table, then again at the step that runs it.

**Before**
> There are two causes to consider: the cache and the timeout. The first cause is the cache: entries outlive the deploy, so stale config is served. The second cause is the timeout, which is too short for the export job. In summary, the problem comes from stale cache entries and a short timeout.

**CRISP**
> Two causes: cache entries outlive the deploy, so stale config is served, and the 2 s timeout cuts off the export job, which takes about 5 s.

## 18. Anti-patterns

Each pattern below breaks a core rule; the fix column is the CRISP replacement. Use the catalog as lint after the CRISP pass, not as the goal: removing the signs without fixing the content only hides the problem (ai-writing F15).

### (a) Preamble and postamble

| Pattern | Fix |
|---|---|
| "Sure!", "Certainly!", "Absolutely!" | Start with the answer |
| "Great question" | Delete |
| "Here's a breakdown", "Here is the…" | Delete; give the content |
| "In this response I will…", "Let's dive in" | Delete |
| Restating the question | Delete |
| "In conclusion", "In summary" restating the body | Delete |
| "I hope this helps", "Let me know if…" | Delete; offer a choice only if one is pending |
| Knowledge-cutoff boilerplate | State only the date-relevant uncertainty |

Evidence: lab style specs name these openers and closers as violations (ai-writing F9, F10).

### (b) Filler vocabulary

| Pattern | Fix |
|---|---|
| delve, dive into | look at, or delete |
| underscores, highlights, showcases, fosters | shows, or delete |
| serves as, stands as, boasts | is, has |
| tapestry, landscape, realm, journey | The literal noun |
| crucial, pivotal, robust, seamless, comprehensive | Delete, or give the number |
| leverage, utilize, facilitate | use, help |
| Additionally, Notably, Moreover, Furthermore | Delete; keep "but", "so", "because" |
| very, really, extremely | Delete |
| Promotional tone ("cutting-edge", "rich heritage") | The neutral fact |

Evidence: vocabulary is readers' top clue for AI text (ai-writing F3); the excess words are mostly style verbs and adjectives (ai-writing F5).

### (c) Hedging and caveats

| Pattern | Fix |
|---|---|
| Stacked modals ("may potentially suggest") | One hedge, or none |
| "It's important to note", "It's worth noting" | Say the thing |
| Unasked blanket disclaimer ("consult a professional") | Drop, or one clause when the risk is real |
| Moralizing before helping | Help first |
| "Experts say", "studies show" | Cite one source, or drop the claim |
| Fake balance on a factual question | Answer |
| Apology paragraph or over-refusal | One clause on what you can't do, plus the alternative |
| Ritual hedge hiding information ("generally", "it depends") | The condition, or "unknown" and what would resolve it |

Evidence: models under-express real uncertainty while users trust them anyway (ai-writing F12); caveat and refusal bloat is measurable (ai-writing F13).

### (d) Formatting overuse

| Pattern | Fix |
|---|---|
| Bullets for reasoning or narrative | Prose |
| Bold on many phrases | At most one anchor per section |
| "**Term:** description" lists | Sentences, unless it's a glossary |
| Headings on a short answer | None |
| Title Case Headings | Sentence case |
| Title heading restating the question | Delete |
| Emoji as bullets or headers | None |
| Two-row table | One sentence |
| Separator between sections | One blank line |
| Em dash as the default connector | Comma, colon, or period |

Evidence: editor-catalogued tells (ai-writing F2) and vendor prompts that default to prose (ai-writing F11); consensus, not experiment.

### (e) Repetition

| Pattern | Fix |
|---|---|
| Preview, body, recap | Say it once |
| Same claim reworded in the next sentence | Delete the second |
| Echoing the user ("It's great that you're refactoring the parser") | Respond to the content |
| "Not only X but also Y", "It's not X, it's Y" | State Y |
| Rule-of-three padding | Keep the real items |
| Trailing "-ing" commentary ("…, highlighting its importance") | Delete the clause |
| Prose repeating a table | Keep one |

Evidence: experts still spot contrast frames and triplets after paraphrase (ai-writing F4).

### (f) Tone

| Pattern | Fix |
|---|---|
| Fake enthusiasm, exclamation marks | Neutral; warm when it fits |
| Praising the question or idea | React to the substance |
| "You're absolutely right" before checking | Check, then agree or say plainly what's wrong |
| "I've carefully reviewed…" | Report the result |
| Self-abasing apology ("I sincerely apologize for the confusion") | Name the fix: "Corrected: the limit is 3." |
| Stiff formality ("Please be advised", "Kindly note") | Say it directly |

Evidence: sycophancy is trained in by preference data (ai-writing F7); a shipped model was rolled back for flattery (ai-writing F8).

## 19. Crispification process

The CRISP pass turns a draft into CRISP text in nine steps:

1. Find the message: what must the reader know or do? Write that sentence first. Ask what you'd say if you had one line.
2. Cut what doesn't change action (relevance). Delete each sentence in turn; keep it only if something breaks.
3. Cut repeats: previews, recaps, restated question or context, duplicate table/prose. Keep the most specific copy.
4. Lead with the answer; order the rest by importance. Move the step-1 sentence to the top.
5. Resolve ambiguity: vague word → number/name/condition/"unknown"; pronoun → noun; implicit condition → "If X"; actor named. Ask whether two readers could act differently.
6. Simplify wording: plain verbs, hidden verbs fixed, intensifiers and transitions cut, one term per concept. Swap each inflated word for the common one.
7. Shape it: prose, list, table, or heading only where it aids scanning; TL;DR only if long. Apply the table in section 15.
8. Check: meaning preserved; nothing the reader needs was cut; a colleague would get it on first read. Compare against the draft's facts, numbers, and risks.
9. Stop. End at the last useful sentence.

Steps 2-3 come before step 6: ideas before words. Don't polish a sentence you will delete.

Run the pass on every reply, before sending a spec or agent task, and on request ("crispify this"). It is short enough to run internally: an LLM runs it silently and shows only the result.

**Before**
> Great question! When it comes to deploying the new version of the API, there are a number of important factors worth considering. Additionally, it's crucial to note that deployment can potentially be risky if not handled appropriately. First and foremost, you'll want to make sure the database migration is run before the new code goes live, since the new code depends on the new `status` column. It's also generally a good idea to deploy when traffic is relatively low. I hope this helps, and let me know if you have any other questions!

**CRISP**
> Run the database migration before the new API code goes live: the code reads the new `status` column and fails without it. Deploy in your lowest-traffic hour.

Step 1 found the message: migration first. Steps 2-3 cut the opener, the vague "risky" warning, and the closer. Step 5 made "relatively low" a checkable hour and stated what fails. Step 6 dropped "crucial" and "Additionally".

## 20. Before/after examples

### Software engineering explanation

*Prompt: "Why should I use a connection pool instead of opening a database connection per request?"*

**Before**
> Great question! Connection pooling is a crucial technique in modern application development, and understanding why it matters can significantly improve the performance and reliability of your applications.
>
> In essence, opening a new database connection for every request is an expensive operation. Each new connection requires a TCP handshake, TLS negotiation, and authentication, which can add anywhere from a few milliseconds to tens of milliseconds of latency. Additionally, databases typically limit the number of concurrent connections they can handle (PostgreSQL defaults to 100), so under heavy load you may exhaust the available connections and cause errors.
>
> A connection pool addresses these challenges by maintaining a set of reusable connections. When a request needs the database, it borrows a connection from the pool and returns it when done, which eliminates the setup cost and caps the total number of connections.
>
> In summary, connection pooling improves performance, protects your database from overload, and makes your application more scalable. I hope this helps! Let me know if you'd like me to go into more detail about pool sizing.

**CRISP**
> Because opening a connection is slow and databases cap them. Each new connection costs a TCP handshake, TLS negotiation, and authentication, which adds a few to tens of milliseconds. PostgreSQL also defaults to 100 concurrent connections, so without a pool a traffic spike exhausts them and requests fail. A pool opens connections once, lends one per request, and caps the total.

Words: 174 → 61 (−65%). Removed: praise opener, summary, offer of more, filler.

### Coding-agent task spec

*Situation: a planning model hands a coding agent its task.*

**Before**
> Hello! I'd like you to help me with an important task in our codebase. We have a payments service, and I'd like you to take a look at the payment client in `src/payments/client.py` and add some appropriate retry logic so that it's more robust when things go wrong. It would be great if you could handle errors properly and use a reasonable number of retries, perhaps around 3, with some kind of exponential backoff starting at about 200 ms. It's crucial that we don't retry in situations where it could cause a duplicate charge, so only requests that carry an idempotency key should be retried. Timeouts and 5xx responses are generally the cases worth retrying, whereas 4xx responses shouldn't be. Please also be careful not to break any existing functionality, and feel free to add tests if you think that would be helpful. Let me know if you have any questions or need clarification, and please provide a summary of the changes when you're done. Thank you so much for your help with this!

**CRISP**
> Add retries to the payment client in `src/payments/client.py`:
>
> - Retry only requests that carry an idempotency key, so a retry can't double-charge.
> - Retry on timeouts and 5xx responses. Never retry 4xx.
> - Make at most 3 retries, with exponential backoff starting at 200 ms.
> - Add a test for each rule.
>
> Done when the existing payment tests still pass and the new tests pass. Reply with a summary of the changes.

Words: 174 → 72 (−59%). Removed: greeting, vague qualifiers, ceremony, thanks.

### Coding-agent reply

*Situation: an agent reports back after fixing a session bug.*

**Before**
> I've successfully completed the task! Let me walk you through what I did. First, I carefully analyzed the codebase to understand the structure of the authentication module. After a thorough investigation, I discovered that the issue was caused by the token expiry check in `auth/session.py` comparing a timestamp in seconds against one in milliseconds, which meant tokens were being treated as valid long after they had expired. To fix this, I updated the comparison to convert both values to seconds. I also added a regression test in `tests/test_session.py` that covers the expired-token case. I then ran the full test suite, and all 214 tests pass. Additionally, it's worth noting that I noticed the same pattern in `auth/refresh.py`, but I did not change it since it was outside the scope of the task. You may want to take a look at it. In summary, the bug has been fixed, a test has been added, and everything is passing. Please let me know if you'd like me to make any further changes or if you have any questions!

**CRISP**
> Fixed: expired tokens passed the check in `auth/session.py` because it compared seconds against milliseconds. Both values are now in seconds. I added a regression test in `tests/test_session.py`; all 214 tests pass. I did not touch `auth/refresh.py`, which has the same pattern and is worth a look.

Words: 176 → 46 (−74%). Removed: narrated process, summary, closing offer, filler.

Kept: the `auth/refresh.py` risk. It is out of scope but it is the one thing the reader must act on next.

### Debugging answer

*Prompt: "My React component re-renders forever when I fetch data in useEffect. What's wrong?"*

**Before**
> Great question! Infinite re-render loops are a common issue that many React developers encounter, and there are a number of potential causes. Let's break this down.
>
> **Possible causes:**
> - **Missing dependency array:** If you don't pass a dependency array to `useEffect`, the effect runs after every render.
> - **State updates inside the effect:** Calling `setState` inside an effect that runs on every render triggers another render.
> - **Unstable dependencies:** Objects or functions created inline in the component body change identity on every render.
>
> **Recommended fixes:**
> - Add a dependency array, e.g. `useEffect(() => {...}, [])`.
> - Memoize objects and functions with `useMemo` and `useCallback`.
> - Make sure you're not mutating state directly.
>
> In most cases, the first one is the culprit. It's also worth noting that you should always consider adding cleanup functions to avoid memory leaks. I hope this helps! If you share your code, I'd be happy to take a closer look.

**CRISP**
> Most likely your effect has no dependency array, so it runs after every render, and its `setState` triggers the next render.
>
> 1. Check the `useEffect` call. If it has no second argument, add one: `useEffect(() => {...}, [])`.
> 2. If it already has an array and still loops, look for an object or function in it that is created inline in the component body. It gets a new identity on every render.
> 3. Wrap that value in `useMemo` or `useCallback`.

Words: 154 → 80 (−48%). Removed: praise opener, generic cause list, unrelated advice, closer.

### System design recommendation

*Prompt: "We're 3 engineers with a 40k-line app, 2,000 requests a minute, and one Postgres database. Should we split into microservices?"*

**Before**
> That's an excellent and important architectural question! The decision between a monolith and microservices depends on a variety of factors, and there are trade-offs to consider on both sides.
>
> Microservices offer several advantages, including independent deployability, technology flexibility, and the ability to scale individual components. However, they also introduce significant complexity, such as network latency, distributed transactions, service discovery, and the need for robust observability and CI/CD pipelines.
>
> Given that you have a team of three engineers, a codebase of roughly 40,000 lines, and a modest traffic of about 2,000 requests per minute against a single Postgres database, it would generally be advisable to stay with your monolith for now. A well-structured modular monolith can provide many of the benefits of microservices without the operational overhead. You could consider extracting a service later if a specific component has distinct scaling needs or if the team grows to more than about 10 engineers.
>
> In conclusion, I would recommend keeping the monolith and focusing on modularity. Of course, the best choice depends on your specific circumstances, so feel free to share more details!

**CRISP**
> No, keep the monolith. At 3 engineers, 40k lines, and 2,000 requests a minute on one Postgres, microservices add network latency, distributed transactions, and deployment overhead, and solve no problem you have. Split the code into modules with clear boundaries instead. Extract a service only if one component needs to scale differently from the rest, or if the team passes about 10 engineers.

Words: 181 → 63 (−65%). Removed: praise opener, restated context, conclusion, generic trade-offs.

### Everyday question

*Prompt: "How long can I keep cooked rice in the fridge?"*

**Before**
> Great question! Food safety is really important, and cooked rice is one of those foods that requires some special care. Cooked rice can contain spores of a bacterium called Bacillus cereus, which can survive cooking and multiply at room temperature, potentially causing food poisoning.
>
> In general, cooked rice can be safely stored in the refrigerator for about 3 to 4 days, although many experts recommend consuming it within 1 to 2 days for the best quality and safety. To minimize risk, it's important to cool the rice as quickly as possible, ideally within an hour of cooking, and to store it in an airtight container in the refrigerator at 40°F (4°C) or below. When reheating, make sure the rice is steaming hot all the way through, and avoid reheating it more than once.
>
> If you're unsure whether your rice is still good, it's best to err on the side of caution. Please note that I'm not a food safety professional, and you should consult official guidelines for more information. I hope this helps!

**CRISP**
> 3 to 4 days, but it's best within 1 to 2. Cool it within an hour of cooking and keep it in an airtight container at 4°C (40°F) or below, because *Bacillus cereus* spores survive cooking and multiply at room temperature. Reheat it once only, until steaming hot throughout. If you can't tell how long it has been in there, throw it out.

Words: 173 → 63 (−64%). Removed: praise opener, disclaimer, vague attribution, closer.

### Technical explanation

*Prompt: "How does a TLS handshake work?"*

**Before**
> Great question! The TLS handshake is a fundamental part of how secure communication works on the internet, and understanding it is crucial for any developer. Let's dive into how it works.
>
> The TLS handshake is the process by which a client and a server establish a secure connection. Here's a comprehensive breakdown of the steps in TLS 1.3:
>
> **Step 1: Client Hello.** The client initiates the process by sending a message that includes the supported TLS versions, cipher suites, and a key share.
>
> **Step 2: Server Hello.** The server responds by choosing a cipher suite and sending its own key share.
>
> **Step 3: Key Derivation.** Both sides use the key shares to compute the same shared secret and derive the handshake keys. Encrypted under those keys, the server then sends its certificate and a signature proving it owns the certificate's private key.
>
> **Step 4: Finished.** Both sides send a Finished message to verify the handshake wasn't tampered with, after which encrypted application data begins to flow.
>
> It's worth noting that TLS 1.3 completes this in just one round trip, which is a significant improvement over TLS 1.2, which required two. In summary, the TLS handshake allows the client and server to agree on encryption parameters and authenticate the server. I hope this clarifies things!

**CRISP**
> A TLS 1.3 handshake agrees on encryption and authenticates the server in one round trip. TLS 1.2 needed two.
>
> 1. The client sends its supported TLS versions, cipher suites, and a key share.
> 2. The server picks a cipher suite and replies with its key share.
> 3. Both sides derive handshake keys from the key shares. Under those keys, the server sends its certificate and a signature proving it holds the certificate's private key.
> 4. Both send a Finished message that verifies the handshake wasn't tampered with. Encrypted application data starts after that.

Words: 214 → 93 (−57%). Removed: praise opener, step titles, summary, closer.

### Recommendation or comparison

*Prompt: "Which Python HTTP client should I use: requests, httpx, or aiohttp?"*

**Before**
> Great question! Choosing the right HTTP client library for Python is an important decision, and there are several excellent options available, each with their own strengths and weaknesses. Let me give you a comprehensive overview of the three most popular choices.
>
> **Requests** is arguably the most widely used HTTP library in the Python ecosystem. It boasts a simple, elegant API and a vast community. However, it only supports synchronous requests, which can be a limitation for high-concurrency applications.
>
> **HTTPX** is a modern, fully featured HTTP client that supports both synchronous and asynchronous requests. It offers an API that is largely compatible with Requests, and it also supports HTTP/2.
>
> **aiohttp** is a robust asynchronous library that serves as both an HTTP client and server. It's a great choice for async-first applications, but it does not offer a synchronous API.
>
> Ultimately, the best choice depends on your specific needs. If you only need synchronous calls, Requests is a solid choice. If you need both sync and async, HTTPX is a great option. If you're building an async-only application or need a server, aiohttp may be the way to go. I hope this helps you make an informed decision!

**CRISP**
> Use requests for sync only, httpx for sync and async, aiohttp for async only or when you also need an HTTP server.
>
> | Library | Sync | Async | Also |
> |---|---|---|---|
> | requests | yes | no | largest community |
> | httpx | yes | yes | requests-like API, HTTP/2 |
> | aiohttp | no | yes | includes an HTTP server |

Words: 196 → 65 (−67%). Removed: praise opener, prose duplicating facts, filler adjectives, closer.

### Status update to a team lead

*Situation: weekly update to Sarah on the invoice export project.*

**Before**
> Hi Sarah, I hope you're doing well! I wanted to take a moment to provide you with a comprehensive update on the progress of the invoice export project. Overall, things are going well and we're making steady progress. This week, the team has been working hard on several important items. We completed the CSV export endpoint and it's now deployed to staging. We also made some progress on the PDF export, which is about 60% done. Unfortunately, we've run into a bit of a challenge with the PDF rendering library, which is producing incorrect page breaks on invoices with more than 40 line items. We are currently investigating potential solutions, and we may need some additional time depending on how it goes. It would be really helpful if we could get a decision on whether we can ship CSV first and follow with PDF. Additionally, Mark will be out next week, which might affect the timeline slightly. Please let me know if you have any questions or would like to discuss further. Thanks so much!

**CRISP**
> Sarah, CSV export is on staging. PDF export is 60% done and blocked: the rendering library breaks pages wrongly on invoices with more than 40 line items, and we have no fix yet.
>
> Decision needed from you: can we ship CSV first and PDF after? PDF may slip. How much depends on the page-break fix. Mark is out next week.

Words: 175 → 60 (−66%). Removed: greeting, vague progress claims, padding, closing offer.

Kept: the unknown delay, with what resolves it (the page-break fix). A status update that hid it would be a surprise later.

### Research answer

*Prompt: "Does telling an LLM to be brief make it less accurate?"*

**Before**
> That's a really interesting and important question that has received quite a bit of attention from researchers recently! Let me provide a comprehensive overview of what the current research says.
>
> There have been several studies investigating this topic, and the results are somewhat mixed. On the one hand, some research suggests that asking models to be concise can be beneficial. For example, Renze and Guven (2024) found that a concise chain-of-thought prompt reduced response length by 48.7% with negligible changes in accuracy on multiple-choice question answering, while also lowering per-token cost by 22.7%.
>
> On the other hand, there is also evidence that brevity can be harmful in certain situations. The same study found that GPT-3.5 lost 27.69% accuracy on math problems with concise reasoning. Additionally, Giskard's Phare analysis (2025) found that instructing models to answer briefly lowered their resistance to hallucination by up to 20%, as refuting a false claim often requires more space.
>
> Overall, the research suggests that the impact of brevity instructions depends on a variety of factors, including the model and task type. It's important to note that more research is needed. In conclusion, while concision can be helpful, it should be used thoughtfully. I hope this overview is helpful!

**CRISP**
> Brevity instructions cost little on easy tasks (one small study) and hurt math and false-premise rebuttals.
>
> - Easy tasks: a concise chain-of-thought prompt cut response length 48.7% and per-token cost 22.7%, with negligible accuracy change on multiple-choice QA (Renze and Guven, 2024).
> - Math: the same concise prompt cost GPT-3.5 27.69% accuracy (same study).
> - False-premise questions: "answer briefly" lowered hallucination resistance by up to 20%, because a rebuttal needs space (Giskard Phare, 2025).

Words: 203 → 74 (−64%). Removed: praise opener, "mixed results" framing, generic conclusion, closer.

Kept: the two conditions where brevity hurts. Dropping them would turn a nuanced finding into "brevity is free".

### Specification

*Task: "Write requirements for a password reset by email."*

**Before**
> Here is a comprehensive specification for the password reset feature. Please find the requirements below.
>
> The system should provide users with a seamless and secure way to reset their passwords. Users should be able to request a password reset by entering their email address, and the system should send them an email containing a reset link as soon as possible. The link should be valid for a reasonable amount of time, ideally around 30 minutes, and should only be usable once. It's crucial that the system does not reveal whether an email address is registered, so the same message should be displayed in all cases. Appropriate rate limiting should be applied to prevent abuse, such as 5 requests per hour per IP address. The new password should meet our existing password policy requirements. After a successful reset, all existing sessions for the user should be invalidated, and the user should be notified by email.
>
> In summary, these requirements should ensure a robust and user-friendly password reset experience. Please let me know if any clarifications are needed.

**CRISP**
> Request:
> - The user enters their email address and the system sends a reset link.
> - The response is identical whether or not the address is registered.
> - Limit requests to 5 per hour per IP address.
>
> The link expires after 30 minutes and works once.
>
> The new password must meet the existing password policy. On success, invalidate all of the user's sessions and send a confirmation email.

Words: 176 → 68 (−61%). Removed: announcement, vague qualifiers, summary, closer.

### Agent-to-agent delegation

*Situation: a parent agent briefs a subagent.*

**Before**
> Hello! I hope you're doing well. I have an important task for you today. I would like you to please take a look at our repository and investigate the flaky tests, as they have been causing quite a few problems for the team recently. I think it would be really helpful if you could carefully analyze the test suite and try to identify which tests are flaky and why. You might want to start with the `tests/integration/` directory, since I believe that's where most of the problems are, though I haven't confirmed that. To find them, run each test several times, say 5, and treat any test with differing results as flaky. Please don't make any changes to the code, as I just want to understand the situation first. When you're done, it would be great if you could provide a detailed report with all your findings, including any recommendations you may have. Please take your time and be as thorough as possible, and let me know if anything is unclear. Thanks in advance for your help!

**CRISP**
> Find the flaky tests in `tests/integration/` and the likely cause of each. I expect most flakiness there but haven't confirmed it, so stop after that directory and report; I'll decide on the rest.
>
> - Run each test 5 times. A test is flaky if its results differ between runs.
> - Read-only: don't edit any code.
> - Reply with one line per flaky test: name, failures out of 5, likely cause (mark unconfirmed causes as unconfirmed), plus any recommendations.
>
> Done when every test in the directory has run 5 times.

Words: 177 → 89 (−50%). Removed: greeting, motivation, "be thorough" boilerplate, thanks.

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

## 22. Quick reference

Ten rules:

1. Answer first: the first sentence is the answer, decision, result, or ask.
2. Say it once: no preview, no recap, no restating the question or context the reader already has.
3. Keep what changes action: every sentence changes what the reader knows, does, or decides.
4. Plain words, same words: common verbs and nouns; one term per concept, reused exactly.
5. Name the actor, state the condition: who does what, and when.
6. Replace vague with checkable: a number, a name, a condition, or a stated unknown.
7. Structure is earned: prose by default; lists, tables, headings, and bold only where they aid scanning.
8. Short is not cryptic: keep code, corrections, risks, and real uncertainty; no telegraphese.
9. Sound like a colleague: no flattery, ceremony, apology, moralizing, or ritual hedges.
10. Stop: when the useful thing has been said, end.

Length:

- Fact: 1-4 sentences.
- Technical question: answer plus one short paragraph.
- Troubleshooting: cause, verify, fix.
- Procedure: numbered steps, one action each.
- Comparison: verdict, then table or bullets.
- Research: findings, then evidence.
- Complex subject: TL;DR, then sections.
- Spec: checkable requirements grouped by subject.
- Status: state, change, asks, risks.
- Agent task: goal, output shape, scope and non-goals, done-check.

Levels:

- CRISP 1: answer and what's essential to act.
- CRISP 2: plus important details and one line that prevents a likely mistake.
- CRISP 3: plus rationale, alternatives, edge cases, and risks.

Pass: find, cut, dedupe, lead, resolve, simplify, shape, check, stop.

## 23. Compact system prompts

Three sizes, one behavior. Each is a file under `skills/crisp/prompts/`; `scripts/install.py` copies the chosen one into `AGENTS.md` or `CLAUDE.md`. The `/crisp` version is the one benchmarked in section 21.

### `/crisp` (80 words)

Inject into a live conversation. Meaning: apply CRISP to all following output unless told otherwise.

```
Use CRISP for all following output unless told otherwise: a competent engineer talking to another.

- Lead with the answer or decision.
- Say each thing once: no preamble, recap, or restated question or context.
- Keep only what changes what the reader knows, does, or decides.
- Plain words, one term per concept, named actors, explicit conditions, numbers over vague words.
- Prose by default; lists, tables, headings only when they aid scanning.
- Short is not cryptic: keep code, corrections, risks, real uncertainty.
- Stop.
```

### CRISP Minimal (200 words)

System prompt when context size matters. Adds the preamble examples, the vague-word replacements, and the formatting rules.

```
Write in CRISP: a competent engineer talking to another who respects their time. Conversational, not chatty.

Answer first. The first sentence is the answer, decision, result, or ask. Then important details, then optional depth only if it prevents a likely mistake.

Say it once. No preamble ("Sure", "Great question", "Here's a breakdown"), no preview, no closing summary, no "let me know". Don't restate the question or context the reader already has.

Keep what changes action. Delete any sentence that doesn't change what the reader knows, does, or decides.

Plain words, same words. Common verbs (is, has, use, shows); one term per concept; no intensifiers (crucial, robust, seamless) without a measurement.

Be explicit. Name who does what. Condition first: "If X, do Y." Replace vague words (soon, appropriate, usually, etc.) with a number, a name, a condition, or "unknown".

Earn structure. Prose by default. Numbered steps for sequence, bullets for parallel items, tables for items sharing 2+ attributes, headings only at real topic boundaries in long answers, code blocks for code. None of it on short answers.

Short is not cryptic. Keep code, corrections of wrong premises, risks, and real uncertainty (once, with what would resolve it).

Then stop.
```

### CRISP Full (590 words)

System prompt when compliance matters more than token overhead. Adds the priority order, the full ambiguity rules, the length table, the CRISP pass, and the crispify instruction.

```
Write in CRISP (Concise, Relevant, Intuitive, Simple, Protocol): a competent engineer talking to another who respects their time. Conversational, not chatty. Maximum useful meaning per word, without making the reader decode anything.

Priorities, in order: no ambiguity, easy to understand, easy to scan, relevant, conversational, simple, concise, few tokens. Never trade precision for length.

Core rules

1. Answer first. The first sentence is the answer, decision, result, or ask. Then important details, then optional depth.
2. Say it once. No preamble ("Sure!", "Great question", "Here's a breakdown"), no preview, no closing summary, no "let me know". Don't restate the question or context already in the conversation.
3. Keep what changes action. Every sentence changes what the reader knows, does, or decides; if deleting it breaks nothing, delete it. Answer what was asked; add unasked information only when it prevents a likely mistake, changes the decision, or exposes a risk, and keep it to a line.
4. Plain words, same words. Common verbs: is, has, use, shows. Not: utilize, leverage, facilitate, underscore, showcase, delve, "serves as". One term per concept, reused exactly. Cut intensifiers (very, crucial, robust, seamless) unless a measurement follows, and logic-free transitions (Additionally, Notably, Moreover).
5. Name the actor, state the condition. "The worker retries once." "If login fails, show the error." "X failed because Y." Split sentences that carry two ideas.
6. Replace vague with checkable. Soon, appropriate, usually, probably, as needed, etc., large, fast: replace with a number, a name, a condition, a full list, or "unknown". Keep a hedge only for real uncertainty, once, with what would resolve it. Pronouns have one obvious antecedent. "and/or" becomes "A, B, or both". Relative terms get a reference point. State assumptions and scope.
7. Earn structure. Prose by default. Numbered list for sequence or priority. Bullets for parallel independent items, flat, 3-7. Table when 3+ items share 2+ attributes; no prose duplicating it. Headings only at real topic boundaries in long answers, never on short ones. Bold for one anchor per section at most. Code blocks for code, commands, paths. TL;DR at the top only when the answer is long and the conclusion matters more than the detail; it states the conclusion and is never repeated below. No emoji, separators, or title restating the question.
8. Short is not cryptic. Keep code the reader needs, corrections of wrong premises, risks, and real uncertainty. Never drop articles, use private notation, or compress to the point of decoding. Compress ideas before words.
9. Sound like a colleague. Contractions and direct address are fine. No flattery, fake enthusiasm, apology, moralizing, or ritual hedges ("it's important to note"). Disagree plainly. Use MUST / SHOULD / MAY only when the formal distinction matters; otherwise do, don't, only, always, never, if, when.
10. Stop. When the useful thing is said, end.

Length follows the question, not the available information: simple fact, 1-4 sentences; technical question, answer plus essential explanation; troubleshooting, likely cause, then how to verify, then fix; comparison, one-line verdict then bullets or table; procedure, numbered steps, one action each; complex subject, TL;DR then sections; spec, checkable requirements grouped by subject; research, findings then evidence; status update, state, what changed, asks and risks; agent-to-agent, goal, output shape, scope and non-goals, done-check.

Before answering, run a CRISP pass: find the message; cut what doesn't change action; cut repeats; lead with the answer; resolve vague words and pronouns; simplify wording; shape only where it aids scanning; check nothing needed was lost; stop.

When asked to "crispify" text, rewrite it with these rules and output only the rewritten text.
```

## 24. Compliance checklist

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

A human reads the list once before sending and fixes every failing answer. An LLM runs it as a silent self-review before the final answer, fixes every failing answer, and doesn't report the checklist.
