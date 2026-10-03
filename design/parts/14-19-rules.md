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
