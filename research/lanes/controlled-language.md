# Lane: Controlled language and requirements-writing standards

## Approaches
| Approach | Useful ideas | Problems | Use in CRISP? |
|---|---|---|---|
| ASD-STE100 (Issue 9, 2025) | 53 rules + ~900 approved / ~1200 unapproved words; one meaning per word; 20/25-word caps; imperative steps; consistent terms | Built for non-native maintenance readers; closed dictionary, no progressive tense, no "should/may" — stilted for engineers | partly — borrow consistency, short steps, not the dictionary |
| EARS (Mavin et al., RE'09) | Fixed clause order: While / When / shall; five patterns + complex | Needs "the system shall" boilerplate; only fits behavior statements | partly — use condition-first order for behavior specs |
| RFC 2119 / RFC 8174 | Few keywords with defined force; uppercase-only meaning; "use sparingly" | Overuse dilutes force; says nothing about prose style | yes — small uppercase keyword set, rare, for real obligations |
| INCOSE GtWR v4 (42 rules) | Singular statements, defined terms, no vague terms/escape clauses/open-ended clauses, explicit conditions, "each" over "all/any" | Heavy; bans "and/or/then/but" and parentheses outright — impossible in conversation | partly — adopt ambiguity rules, drop combinator ban |
| NASA SEH App. C | shall/will/should defined; verifiability word list; one thought, rationale beside requirement; positive form | Contract-style "the product shall"; assumes numbered requirements | partly — adopt vague-word list, "stated positively" |
| NASA FRET / FRETish | Seven fields (scope, condition, component, shall, probability, timing, response); parser feedback; glossary autocomplete | Aimed at temporal-logic semantics; docs call the grammar "not for the faint-hearted" | no — field model good for specs, robotic in prose |
| Kuhn 2014 CNL survey / PENS | Precision, Expressiveness, Naturalness, Simplicity; 100 CNLs; CNL must stay N≥3 | Descriptive, not prescriptive; offers no rule set | yes — frames the trade-off CRISP must pick |
| Requirements smells (Femmer et al., JSS 2017) | Eight detectable smells from ISO 29148 | Automatic detection: 59% precision, 82% recall; context-dependent | partly — word lists as flags, not hard bans |

## Findings
### F1. STE splits writing into procedures (imperative, ≤20 words) and descriptions (≤25 words)
- Evidence: ASD-STE100 official site, "About STE" (2025) https://www.asd-ste100.org/about_STE.html confirms 53 rules in 9 sections and the dictionary model; limits, imperative-only steps, and noun-cluster ≤3 come from a secondary summary of the rules (nuelcyoung/asd-ste100, https://raw.githubusercontent.com/nuelcyoung/asd-ste100/main/references/writing-rules.md). The standard itself is free by request only; I did not read it.
- Strength: well-supported (domain: maintenance manuals)
- Implication for CRISP: Steps are imperative, one action each. For prose, use soft targets (~25 words), not caps.

### F2. STE's "one word, one meaning, one part of speech" is its most transferable idea
- Evidence: ASD-STE100 "About STE" (above); Unwalla, ISTC slides (https://istc.org.uk/wp-content/uploads/2021/11/Mike-Unwalla-To-make-test-as-clear-as-possible-use-Simplified-Technical-English.pdf) lists 9 names for one shipping part ("cargo arm", "Chicksan", "MLA"…) as a failure.
- Strength: well-supported
- Implication for CRISP: Name each thing once and reuse the name. Never rotate synonyms for style ("worker/job/task/process"). Applies to agent prompts and specs.

### F3. Several STE rules make conversation unnatural
- Evidence: Unwalla slides (above) record writer objections: "STE is repetitive… blunt"; the rules summary bans progressive tenses and -ing verbs, and "should/may/might/could/would". Kuhn 2014 (https://aclanthology.org/J14-1005.pdf) notes N⁴ languages have natural single sentences but "complete texts… seem very clumsy and repetitive".
- Strength: well-supported
- Implication for CRISP: Reject the closed dictionary, tense bans, modal bans, ban on phrasal verbs, no-contractions, and the mandatory "keep every article" rule. They serve non-native readers of manuals, not engineers. Note STE's own Rule 6.5 (vary sentence frames) as summarized there — repetitive output is a failure.

### F4. EARS: fixed clause order, five patterns, measured only in one case study
- Evidence: Mavin, Wilkinson, Harwood, Novak, "Easy Approach to Requirements Syntax (EARS)", RE'09, IEEE Xplore abstract (https://ieeexplore.ieee.org/document/5328509): ruleset addresses eight common problems (ambiguity, complexity, vagueness); case study on a jet-engine regulation showed "qualitative and quantitative improvements". Patterns and examples from the official guide (https://alistairmavin.com/ears/): ubiquitous `The X shall Y`; state `While`; event `When`; optional `Where`; unwanted `If … then`; complex = combination. Order: While → When → shall.
- Strength: reasonable hypothesis (single case study; I could not open the full paper — ACM returned 403)
- Implication for CRISP: Behavior specs lead with the trigger: "When X, do Y." "If X fails, do Z." Keep order precondition → trigger → response. Drop "the system shall".

### F5. RFC 2119: keywords carry force only when defined, used sparingly, and capitalized (RFC 8174)
- Evidence: RFC 2119 §6 (Bradner 1997, https://www.rfc-editor.org/rfc/rfc2119): imperatives "must be used with care and sparingly… only where it is actually required for interoperation or to limit behavior which has potential for causing harm". RFC 8174 (Leiba 2017, https://www.rfc-editor.org/rfc/rfc8174): only ALL-CAPS carries the defined meaning; lowercase has "normal English meanings"; normative text "does not require the use of these key words".
- Strength: well-supported
- Implication for CRISP: Use MUST / SHOULD / MAY (and NOT forms) uppercase only, only for hard rules. Lowercase "must" in prose stays ordinary English. Do not capitalize every instruction — that dilutes the signal.

### F6. NASA separates shall (requirement), will (fact), should (goal)
- Evidence: NASA SEH Appendix C.1 (https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/): "Shall = requirement; Will = facts or declaration of purpose; Should = goal". C.3: "stated positively (as opposed to negatively, i.e., 'shall not')". C.4: one thought, one subject and one predicate; rationale kept separate; terms consistent with glossary.
- Strength: well-supported as practice; no effectiveness data in the page
- Implication for CRISP: Keep a three-level force scale (MUST / SHOULD / plain statement). State rules positively when a positive form exists ("Use X", not "Don't use not-X"); keep NOT for true prohibitions. Put the reason next to the rule, not inside it.

### F7. INCOSE v4: the useful rules are ambiguity rules, not syntax rules
- Evidence: INCOSE GtWR v4 Summary Sheet (2023, https://www.incose.org/wp-content/uploads/legacy/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf): R2 active voice; R4 defined terms; R5 definite articles; R7 vague terms; R8 escape clauses; R9 open-ended clauses; R16 avoid "not"; R17 avoid "/"; R18 single thought; R19 avoid combinators ("and, or, then, unless, but, as well as, however…"); R24 avoid pronouns; R26 avoid absolutes (always, never, all, 100%); R27 explicit conditions; R32 "each" over "all/any/both"; R36 consistent terms.
- Strength: well-supported as practice; rules are expert consensus, not experiments
- Implication for CRISP: Adopt: active voice, single thought per statement, no escape clauses, no open-ended lists ("etc."), explicit conditions, "each", no ambiguous pronouns, no absolutes. Reject: R19 (banning "and/or/but/then" cannot work in conversation), R21 (no parentheses), R5 ("the" over "a").

### F8. Vague-word lists work as flags, not bans (precision is low)
- Evidence: Femmer, Méndez Fernández, Wagner, Eder, "Rapid quality assurance with Requirements Smells", JSS 2017 (https://arxiv.org/pdf/1611.08847): detection precision 59%, recall 82%, "high variation"; Krisch & Houdek's weak-word detector averaged 12% precision (cited there). Smells: subjective language, ambiguous adverbs/adjectives, loopholes, open-ended terms, superlatives, comparatives, negative statements, vague pronouns.
- Strength: well-supported
- Implication for CRISP: Treat the vague-word list as "replace with a number, name, or condition, unless the word is the exact meaning". Do not ban words mechanically.

### F9. Kuhn's PENS shows CRISP must stay near N⁴/N⁵ and give up precision
- Evidence: Kuhn, "A Survey and Classification of Controlled Natural Languages", Comput. Linguistics 40(1), 2014 (https://aclanthology.org/J14-1005.pdf; abstract https://arxiv.org/abs/1507.01701): 100 CNLs; PENS = Precision, Expressiveness, Naturalness, Simplicity, five classes each; CNLs sit between English (P¹E⁵N⁵S¹) and propositional logic. PENS "describe[s]… not… rank[s]"; gains in one dimension cost another. Type-F languages (Attempto, PENG) buy machine-parseable precision with naturalness.
- Strength: well-supported (taxonomy, not experiment)
- Implication for CRISP: Target P² E⁵ N⁵ S²: stay fully expressive and natural, reduce ambiguity through word-level and structure-level conventions only. No grammar to learn, no parser.

### F10. FRETish: structured fields buy checkable semantics, cost readability
- Evidence: FRET docs, "Writing Requirements in FRET" (https://github.com/NASA-SW-VnV/fret/blob/v3.1.0/fret-electron/docs/_media/user-interface/writingReqs.md): up to seven fields — scope, condition, component, shall, probability, timing, response; only component, shall, response mandatory; timing words (immediately, eventually, always, never, within N units, until, before). Example: "In flight mode the battery shall always satisfy voltage > 9". Docs call the grammar "not for the faint-hearted".
- Strength: well-supported for formal verification; irrelevant to prose clarity
- Implication for CRISP: Borrow the slot checklist for specs only: scope, trigger, actor, response, timing/limit. Name timing and limits ("within 200 ms", "until X"). Never force prose into slots.

### F11. Named words with unstated meaning cause most "vague" failures: replace with measurable terms
- Evidence: NASA SEH C.4 verifiability list; INCOSE R7/R8 (above). Both tie the vague word to testability: if you cannot check it, it is not a requirement.
- Strength: well-supported
- Implication for CRISP: Every adjective that implies a threshold ("fast", "robust", "large") gets a number, a comparison, or deletion. Specs and agent tasks MUST state how to check done.

### F12. Controlled-language gains are measured in translation and error cost, not in prose speed
- Evidence: Unwalla slides (Braster 2008, cited): STE cuts content up to 20% and translation cost 40% — a trade-publication citation, not read at source. STE is a mandatory part of aviation maintenance docs (ASD site, About STE).
- Strength: reasonable hypothesis for token savings
- Implication for CRISP: Brevity benefits are plausible but unproven for LLM tokens; do not claim a number.

## Research questions
- **What improves clarity?** One thought per statement, consistent terms, explicit actor and condition, active voice, defined terms (F2, F7).
- **What reduces ambiguity?** Consistent names, no vague/escape/open-ended phrases, no dangling pronouns, explicit conditions, "each" over "all/any" (F7, F8).
- **What reduces verbosity?** Cutting purpose phrases and superfluous infinitives ("is able to", "to allow"); INCOSE R10, R20. STE's 20% figure is unverified (F12).
- **What improves scanability?** Condition first (EARS, STE); lists for sequences; one requirement per line; rationale on its own line (F4, F6).
- **Natural vs artificial?** Natural: imperatives, "When X, do Y", plain MUST/SHOULD. Artificial: "the system shall", closed dictionaries, tense bans, banning and/or/but (F3, F7).
- **Token saves/wastes?** Saves: dropping boilerplate, one name per thing, no restating. Wastes: keyword on every line, hedges, synonyms-for-variety, explaining rule meaning each time. Not measured here.
- **Specs vs answers vs coding agents?** Specs: EARS order, FRET slot checklist, testable limits. Answers: plain voice, minimal keywords. Agent tasks: imperatives, one action each, explicit done-check, defined terms.
- **What can LLMs follow reliably?** Not tested in this lane. [INFERENCE] Short lists of concrete rules (consistent names, trigger-first, MUST sparingly) are easier than grammar restrictions (tense bans, 20-word caps).
- **Evidence vs preference?** Evidence (weak-to-moderate): EARS case study, smell detection numbers, STE adoption. Mostly expert consensus: INCOSE, NASA. Preference: sentence caps, keyword choice.

## Rules that transfer to engineer-to-engineer writing
1. Name each thing once; reuse the name (STE, INCOSE R36).
2. One instruction per sentence or list item; imperative form (STE).
3. Condition first: "When/If X, do Y" (EARS, STE).
4. Active voice with a named actor, unless the actor is unknown or irrelevant (INCOSE R2, STE).
5. MUST / SHOULD / MAY uppercase, rare, only for hard rules (RFC 2119/8174).
6. Replace unmeasurable adjectives with a number or check (NASA, INCOSE R7).
7. No escape clauses or open-ended lists ("etc.", "including but not limited to") (INCOSE R8-R9).
8. State rule and reason separately; reason follows (NASA C.4).
9. Prefer positive phrasing; keep NOT for prohibitions (NASA C.3, INCOSE R16).

## Rules to reject
- Closed approved-word dictionary, tense and modal bans, ≤20/25-word hard caps (F3: built for non-native manual readers; hard caps cause fragments).
- "The system shall…" boilerplate, numbering every sentence (contract voice).
- Ban on and/or/but/then/parentheses (INCOSE R19, R21): unnatural; split only when two requirements are joined.
- Rigid slot grammar like FRETish for prose (F10).
- Mechanical word bans (F8: 59% precision at best).

## Merged vague-words list
Replace with a number, name, or condition. Source key: **N** = NASA SEH App. C; **I** = INCOSE GtWR v4 R7/R8/R9/R26/R32/R35; **F** = Femmer et al. 2017 (examples); **S** = STE unapproved examples (Unwalla slides).
- **Quantity:** some (I), any (I, S), several (I), many (I), a lot of (I), a few (I), approximate / about / close to (I; about also S), almost / nearly / very nearly / almost always (I, F), allowable (I), minimal (F), significant (I, F)
- **Quality adjectives:** adequate (N, I), sufficient (N, I), appropriate (N, I, S), efficient (I), effective (I), reasonable (I), robust (N), flexible (N, I), expandable (I), typical (I), common / routine / generic / relevant / ancillary (I), proficient / customary (I), safe (N), usable / user-friendly / easy / easy to use (N, F), portable (N), light-weight (N), small / large (N), fast (N), cost effective (F), ad hoc (N), accommodate (N)
- **Adverbs / "-ly", "-ize":** quickly / easily / clearly / other "-ly" words (N); maximize / minimize / other "-ize" words (N)
- **Escape clauses:** as appropriate, as applicable, as required, when required, if required (N, I); if necessary, if it should prove necessary, to the extent necessary, to the extent practical, if practicable (I); so far as is possible, as little / as much as possible, where possible, as far as possible (I, F)
- **Open-ended:** etc., and so on, including but not limited to, and/or (N, I)
- **Absolutes:** always, never, all, every, 100% (I R26)
- **Superlatives / comparatives:** highest, more exact, "-er" without a baseline (F)
- **Vague pronouns:** this, these, indefinite "it/they" without antecedent (N, I R24, F)
- **Temporal:** eventually, until, before, after, as, once, earliest, latest, instantaneous, simultaneous, at last (I R35); at least, depending, being, allowed (S, STE unapproved; context-specific)
- **Placeholders:** TBD, TBR without owner and date (N C.3)

## Sources
1. RFC 2119, Bradner, 1997 — https://www.rfc-editor.org/rfc/rfc2119 (fetched)
2. RFC 8174, Leiba, 2017 — https://www.rfc-editor.org/rfc/rfc8174 (fetched)
3. NASA SEH Appendix C, "How to Write a Good Requirement" — https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/ (fetched)
4. INCOSE GtWR v4 Summary Sheet, 2023 — https://www.incose.org/wp-content/uploads/legacy/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf (fetched)
5. EARS official guide, Alistair Mavin — https://alistairmavin.com/ears/ (fetched)
6. EARS paper abstract, IEEE Xplore — https://ieeexplore.ieee.org/document/5328509 (fetched; full text not accessed)
7. Kuhn 2014, Computational Linguistics 40(1) — https://aclanthology.org/J14-1005.pdf (fetched); abstract https://arxiv.org/abs/1507.01701 (fetched)
8. Femmer et al. 2017, Requirements Smells — https://arxiv.org/pdf/1611.08847 (fetched, first 300 of 1094 lines)
9. FRET "Writing Requirements" docs, NASA — https://github.com/NASA-SW-VnV/fret/blob/v3.1.0/fret-electron/docs/_media/user-interface/writingReqs.md (fetched)
10. ASD-STE100 official site — https://www.asd-ste100.org/ and https://www.asd-ste100.org/about_STE.html (fetched)
11. Unwalla, ISTC slides on STE — https://istc.org.uk/wp-content/uploads/2021/11/Mike-Unwalla-To-make-test-as-clear-as-possible-use-Simplified-Technical-English.pdf (fetched; secondary)
12. STE rules summary, nuelcyoung/asd-ste100 — https://raw.githubusercontent.com/nuelcyoung/asd-ste100/main/references/writing-rules.md (fetched; unofficial summary; verify limits against the standard)
