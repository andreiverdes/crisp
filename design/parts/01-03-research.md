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
