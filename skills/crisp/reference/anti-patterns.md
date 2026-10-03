# CRISP anti-patterns

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

Full protocol: https://github.com/andreiverdes/crisp/blob/main/CRISP.md
