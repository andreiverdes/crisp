# Lane: Plain language, style guides, readability, cognitive load

## Approaches
| Approach | Useful ideas | Problems | Use in CRISP? |
|---|---|---|---|
| Federal Plain Language Guidelines (US gov, Plain Writing Act 2010) | Audience first; one idea per sentence; hidden-verb fix; "use simple words" substitution table; before/after examples | Built for public/legal text; guidance cites books, not experiments; "omit *it is*, *there is*" is mechanical | yes: word and verb rules, with the tests below |
| ISO 24495-1:2023 | International standard; applies to technical writing; "does not cover accessibility" | Full text paywalled; I read only the abstract | partly: cite as legitimacy, not as rule source |
| Microsoft Writing Style Guide | "Bigger ideas, fewer words"; read aloud; contractions; lead with what matters; sentence-case headings; cut *there is/are* | Marketing-flavored ("project friendliness"); "shorter is always better" is overstated | yes: voice, front-loading, weak-phrase list |
| Google developer docs style | Best fit for engineers: conversational not frivolous; conditions before instructions; no *please/simply/easy/just*; no pre-announcing; list-vs-table rules | Documentation-specific; some rules are legal/inclusion driven | yes: closest voice match |
| NN/g web-reading research (1997, 2006, 2017–18) | Measured: concise +58%, scannable +47%, objective +27%, all three +124% usability | Web pages, small 1997 sample; F-pattern describes *unformatted* text, not a goal | yes: scanning rules; no to "F-layout" |
| Readability formulas (Flesch, FK) and sentence-length claims | Cheap lint for outlier sentences | Only measure word/sentence length; ignore layout, reader, content; headline stats are secondhand | partly: lint, never target |
| Cognitive load theory (Sweller; Kalyuga) + working memory (Miller, Cowan) | Redundancy effect: removing duplicate or unneeded info improves learning; few novel items fit in working memory | Mostly instructional-learning experiments; reverses for novices | yes: no-repeat rule, chunking, expertise caveat |
| BLUF / inverted pyramid / Minto Pyramid | Answer first, group support under it | Evidence is practitioner tradition plus NN/g observation, not controlled trials | yes: answer-first as idea, not slogan |
| Tufte data-ink / chartjunk | Analogy: formatting that carries no information is noise | Not fetched; about charts, no text experiments | partly: analogy only, uncited |

## Findings
### F1. Concise, scannable and objective text each measurably helped web users; combined +124%
- Evidence: How Users Read on the Web, Nielsen, NN/g, 1997. https://www.nngroup.com/articles/how-users-read-on-the-web/ (79% scanned, 16% read word-by-word; concise 58%, scannable 47%, objective 27%.)
- Strength: well-supported for web tasks (small study, replicated in spirit by later NN/g work)
- Implication for CRISP: Cut words, add structure, and drop hype and filler. Promotional adjectives cost accuracy, not only taste.

### F2. Promotional or inflated language slows readers; plain authors are judged more trustworthy
- Evidence: Same NN/g 1997 page (objective version beat control on time, errors, memory); Cringeworthy Words to Cut, Loranger, NN/g, 2016, https://www.nngroup.com/articles/cringeworthy-words/ (cites Oppenheimer 2006, *Applied Cognitive Psychology*: needless long words lower perceived intelligence).
- Strength: well-supported
- Implication for CRISP: Ban intensifiers (*very, really, extremely*), "we understand that…", and *utilize*. State facts; skip persuasion.

### F3. Redundancy hurts learning: duplicate or unneeded information is not neutral
- Evidence: The Redundancy Principle in Multimedia Learning, Kalyuga & Sweller, Cambridge Handbook of Multimedia Learning, 2021, https://unsworks.unsw.edu.au/bitstreams/e72f23bb-b577-45fd-8513-4cd1716672b6/download ("overwhelming evidence… from a very large number of controlled experiments"). Includes Reder & Anderson: summaries ~20% of chapter length beat full chapters over 10 experiments, retained up to 12 months; Carroll's minimal manual beat conventional manuals. Review of 63 studies: Trypke et al., *Frontiers in Psychology*, 2023, https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1148035/full
- Strength: well-supported, with limits (learning tasks, not all agent work)
- Implication for CRISP: "Say it once" is evidence-backed. Don't restate the question, summarize what was just said, or end with a recap.

### F4. Redundancy reverses for novices, and short cueing repetition can help
- Evidence: Kalyuga & Sweller 2021 (expertise reversal; "partial redundancy" labels helped); Trypke et al. 2023 (content redundancy helps low-prior-knowledge learners; short keyword cues help).
- Strength: well-supported
- Implication for CRISP: Target a competent peer. Allow one-line orientation (a headline plus detail) for newcomers, never a verbatim repeat. Cut harder for experts.

### F5. Working memory holds few novel items; "7±2" is an overstated rule
- Evidence: Cowan, "The magical number 4…", *Behavioral and Brain Sciences*, 2001, https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/magical-number-4-in-shortterm-memory-a-reconsideration-of-mental-storage-capacity/44023F1147D4A1D44BDC0AD226838496 (abstract: ~4 chunks; Miller's 7 "a rough estimate and a rhetorical device"). NN/g warns against using 7 as a hard UI limit: How Chunking Helps, 2016, https://www.nngroup.com/articles/chunking/
- Strength: well-supported (the ~4 figure); list-length caps are a heuristic
- Implication for CRISP: Group items into labeled chunks and keep parallel items to roughly 3–5 per group. Don't use "7" as a rule.

### F6. Answer-first helps comprehension and skimming; BLUF is a tradition, not a trial result
- Evidence: Inverted Pyramid, Schade, NN/g, 2018, https://www.nngroup.com/articles/inverted-pyramid/ (claims: faster mental model, lower interaction cost, safe truncation; no experiment cited there). Minto: https://www.barbaraminto.com/concept (group ideas, "guide the reader down the pyramid"). BLUF in Army Regulation 25-50 appears only as a search-result snippet; I did not read the passage, so treat that as unverified.
- Strength: reasonable hypothesis (strong practitioner convergence)
- Implication for CRISP: First line = result, decision, or ask. Details follow in order of importance, so truncation loses the least.

### F7. Readers scan; unformatted text invites the F-pattern and loses content
- Evidence: F-Shaped Pattern, Pernice, NN/g, 2017 (research from 2006), https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ (F appears when text is unformatted, readers want efficiency; fix with front-loaded headings, bold keywords, lists, cutting).
- Strength: well-supported (eye-tracking, ~45–47 participants per study); describes web pages
- Implication for CRISP: Front-load every heading, list item and paragraph with the information-carrying word. Don't design around "F"; design so nothing important depends on position.

### F8. Sentence-length statistics are secondhand; use as a lint threshold only
- Evidence: Sentence length: why 25 words is our limit, GOV.UK blog, 2014, https://insidegovuk.blog.gov.uk/2014/08/04/sentence-length-why-25-words-is-our-limit (relays Ann Wylie's "14 words → >90%, 43 words → <10%" from an API study; correction in comments: it is share of *information*, not share of *people*). I could not reach the original study.
- Strength: unverified headline numbers; the direction (shorter is easier) is common sense and in federal guidelines
- Implication for CRISP: Don't cite "43 words = 10% comprehension". Use "one idea per sentence; split sentences past ~25 words" as house style.

### F9. Flesch-Kincaid measures word and sentence length, nothing else
- Evidence: Jindal & MacDermid, Uses and Limitations of Flesch Formula, *Education for Health*, 2017, https://pubmed.ncbi.nlm.nih.gov/28707643 (ignores layout, reader knowledge, motivation, style, and charts/tables).
- Strength: well-supported
- Implication for CRISP: Never score CRISP compliance by grade level. Technical terms raise the score without harming expert readers; clarity needs a task-based check (can the reader act on it?).

### F10. Active-voice mandates lack experimental support; keep the actor, not the dogma
- Evidence: Federal hidden-verbs page (rule, no experiment), https://raw.githubusercontent.com/GSA/plainlanguage.gov/main/_pages/guidelines/words/avoid-hidden-verbs.md; Rhodes, *The active and passive voice are equally comprehensible in scientific writing*, PhD thesis, U. Washington, 1997, https://digital.lib.washington.edu/researchworks/items/214d8593-77d9-40e8-b735-d92d83fca1c4 (two experiments, no difference in reading speed or comprehension). Google ties active voice to "who's performing the action": https://developers.google.com/style/highlights
- Strength: stylistic preference; small evidence base (one thesis read)
- Implication for CRISP: Rule: name who does what (essential in bug reports, plans, agent messages). Don't ban passive where the actor is irrelevant. Hidden verbs (*make an application* → *apply*) are a cheap, safe length win.

### F11. Lists for sequences, tables for multi-attribute data; one-item lists are noise
- Evidence: Google Lists, https://developers.google.com/style/lists (numbered = sequence, bulleted = unordered, description lists for term/definition pairs, parallel structure, no single-item lists, avoid trailing *etc.*); Microsoft scannable content, https://learn.microsoft.com/en-us/style-guide/scannable-content/ (consistent patterns, parallel structure, keywords first). I did not find a fetched controlled study on list-vs-prose procedures.
- Strength: stylistic preference (consistent across guides); experimental support not verified
- Implication for CRISP: Numbered list for ordered steps, bullets for sets, table when items share 2+ attributes. Prose for reasoning and tradeoffs.

### F12. Put the condition first; drop pre-announcing and politeness fillers
- Evidence: Google highlights (https://developers.google.com/style/highlights): "Put conditions before instructions"; Future features (https://developers.google.com/style/future): don't pre-announce; Voice and tone (https://developers.google.com/style/tone): no *please* in instructions, no *simply/easy/quickly*, no *please note*, *at this time*.
- Strength: stylistic preference (the *future* rule is partly legal)
- Implication for CRISP: "If X, do Y", not "Do Y if X". Don't announce what you're about to say ("Here's a summary:"), just say it.

### F13. Tone: speak like a knowledgeable friend, but don't copy speech
- Evidence: Google tone page: "Don't try to write exactly the way you speak… you probably speak more colloquially and verbosely than you should write." Microsoft Top 10 tips, https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice (read aloud, contractions, "Get to the point fast").
- Strength: stylistic preference
- Implication for CRISP: Contractions OK. Read-aloud test finds stilted text, but cut the filler that speech adds. Avoid both "legalese" and chatty padding.

## Weak and filler word lists in the guides (fetched)
- **Federal "Don't say → Say"** (use-simple-words-phrases, https://raw.githubusercontent.com/GSA/plainlanguage.gov/main/_pages/guidelines/words/use-simple-words-phrases.md). Dirty dozen: *addressees, assist/assistance, commence, implement, in accordance with, in order that, in the amount of, in the event of, it is, promulgate, this activity/command, utilize/utilization*. Omit or shorten: *in order to → to; due to the fact that → since; it is / there is / there are → (omit); the use of; in the process of; on a regular basis; take action to; at the present time → now; prior to → before; subsequent → later; however → but; therefore → so; ensure → make sure; facilitate → help; provide → give; numerous → many; a number of → some; terminate → end; initiate → start; demonstrate → show*. Hidden verbs: *make an application → apply; conduct an analysis of → analyze; carry out a review → review*.
- **Microsoft** (Top 10 tips): avoid *there is / there are / there were*; delete *you can* when unnecessary; "prune every excess word"; start statements with a verb.
- **Google word list** (https://developers.google.com/style/word-list): *just* (avoid, usually deletable); *simple/simply, quick/quickly, easy* (delete); *please* (only when asking a favor), *please note*; *in order to → to*; *leverage → use*; *access (verb)* → see/edit/use; *actionable, performant, proper/properly* (vague, subjective); *since → because*; *allows you to → lets you*; *at present, presently, now, soon, new, latest* (time-bound); *etc., and so on* (use "such as" or "include"); *should* (ambiguous, use must/can); *tl;dr*; *let's*; *i.e.* (use "that is"); bare *this/that* without a noun.
- **NN/g** (https://www.nngroup.com/articles/cringeworthy-words/): *utilize; enables / allows you to; very, really, extremely, quite; "We understand that…", "In today's fast-paced world…"; end user*.
- **Missing:** Microsoft's A–Z bloated-phrase page returned 404; Plain English Campaign page also 404. Those lists are not covered.

## Research questions
- **What improves clarity?** Reader-first scope, one idea per sentence, consistent terms (Microsoft: "if you mean the same thing, use the same word"), concrete verbs, objective claims (F1–F2).
- **What reduces ambiguity?** Same word for same thing; noun after *this/that*; *must/can* instead of *should/may*; *if…then* kept explicit; conditions first; dates and versions instead of *now/latest/soon* (Google word list, F12).
- **What reduces verbosity?** Delete restatement and filler (F3), hidden verbs, intensifiers, pre-announcements, trailing *etc.* Summaries beat full text in experiments (F3).
- **What improves scanability?** Front-loaded headings and first words, short chunks, lists for sets and sequences, tables for attribute data, bold keywords (F6–F7, F11). NN/g's chunk advice: ~3–7 line paragraphs (Microsoft), clear hierarchy.
- **Natural vs artificial?** Natural: contractions, "you", plain verbs, no hype. Artificial: *please note*, *utilize*, "it is important to note", shouting emphasis, legal modal pile-ups (F13).
- **What saves or wastes tokens?** Saves: answer-first, no restatement, tables over repeated prose labels. Wastes: preambles, recaps, politeness, redundant headings. Over-compression (dropping articles and connectives) can hurt clarity (Google keeps *then* in if/then) [INFERENCE for LLM token trade-offs].
- **Specs vs normal answers vs coding agents?** Specs: precise terms, conditions first, numbered steps, one requirement per sentence. Answers: BLUF plus reasoning in prose. Coding agents: same as specs; explicit imperative with success criteria [INFERENCE, outside this lane's sources].
- **What can LLMs follow reliably?** Not testable from these sources. Concrete rules (ban list, "first line is the answer") are checkable; vague ones ("be natural") are not [INFERENCE; defer to the prompting lane].
- **Evidence vs preference?** Evidence: concise/scannable/objective (F1), redundancy (F3–F4), capacity limits (F5), formula limits (F9). Preference: active voice (F10), sentence-length cutoffs (F8), list rules (F11), tone (F13), BLUF (F6, practitioner).

## Sources
1. How Users Read on the Web, Nielsen, NN/g, 1997 — https://www.nngroup.com/articles/how-users-read-on-the-web/ (fetched)
2. F-Shaped Pattern of Reading, Pernice, NN/g, 2017 — https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ (fetched)
3. Inverted Pyramid, Schade, NN/g, 2018 — https://www.nngroup.com/articles/inverted-pyramid/ (fetched)
4. How Chunking Helps Content Processing, Moran, NN/g, 2016 — https://www.nngroup.com/articles/chunking/ (fetched)
5. Cringeworthy Words to Cut, Loranger, NN/g, 2016 — https://www.nngroup.com/articles/cringeworthy-words/ (fetched)
6. Kalyuga & Sweller, The Redundancy Principle in Multimedia Learning, 2021 — https://unsworks.unsw.edu.au/bitstreams/e72f23bb-b577-45fd-8513-4cd1716672b6/download (fetched)
7. Trypke, Stebner, Wirth, Two types of redundancy in multimedia learning, 2023 — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1148035/full (fetched, partial)
8. Cowan, The magical number 4, 2001 — https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/magical-number-4-in-shortterm-memory-a-reconsideration-of-mental-storage-capacity/44023F1147D4A1D44BDC0AD226838496 (abstract fetched)
9. Federal plain language: use-simple-words-phrases, avoid-hidden-verbs, write-short-sentences (GSA repo; site moved to digital.gov/guides/plain-language) — https://raw.githubusercontent.com/GSA/plainlanguage.gov/main/_pages/guidelines/words/use-simple-words-phrases.md (fetched); https://digital.gov/guides/plain-language (fetched; Plain Writing Act of 2010)
10. Microsoft Writing Style Guide: Top 10 tips; Scannable content; Word choice — https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice (fetched)
11. Google developer documentation style guide: tone, highlights, lists, future, word list — https://developers.google.com/style/tone (fetched; others fetched)
12. ISO 24495-1:2023 abstract — https://www.iso.org/standard/78907.html (fetched; the four principles are not on this page and I did not verify them)
13. Jindal & MacDermid 2017, Flesch limits — https://pubmed.ncbi.nlm.nih.gov/28707643 (fetched)
14. GOV.UK sentence length post, 2014 — https://insidegovuk.blog.gov.uk/2014/08/04/sentence-length-why-25-words-is-our-limit (fetched; secondhand stats)
15. Rhodes 1997, active/passive thesis — https://digital.lib.washington.edu/researchworks/items/214d8593-77d9-40e8-b735-d92d83fca1c4 (fetched)
16. Minto Pyramid Principle concept — https://www.barbaraminto.com/concept (fetched)

## Gaps
- Not verified: Sweller 1988 and Miller 1956 (found via search only); Tufte; the original API sentence-length study; Army BLUF regulation text (fetch did not reach the passage); Reder & Anderson 1980 PDF (text extraction failed; relied on the Kalyuga chapter's account); ISO's four principles; Plain English Campaign and Microsoft bloated-phrase lists (404).
- No fetched controlled study on list-vs-prose procedures. Search found Wright & Reid (1973) and flowchart-vs-prose work via citations only. Next step: locate Wright's papers.
- Nothing here tests LLM compliance; hand off to the prompting and benchmark lanes.
