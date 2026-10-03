# Lane: Agents and context engineering

## Approaches
| Approach | Useful ideas | Problems | Use in CRISP? |
|---|---|---|---|
| AGENTS.md / CLAUDE.md | Commands, non-obvious conventions, boundaries; nearest file wins; prune by "would removing this cause mistakes?" | Often bloated with repo overviews; measured gain is small | yes: include only what can't be inferred |
| Cursor rules | <500 lines, composable, reference files not copies, add a rule only after a repeat mistake | Tool-specific frontmatter | partly: borrow scoping and "reference, don't copy" |
| Anthropic context engineering | Smallest high-signal token set, right altitude, just-in-time refs, compaction, sub-agent summaries | Principles, little hard data | yes: core model for "don't restate" |
| Production concision prompts | Numeric caps, banned preamble/postamble, examples | Chat-era "fewer than 4 lines" over-truncates and is superseded | partly: borrow ban list, drop hard caps |
| Claude.ai / Codex formatting rules | Minimal formatting; backticks for paths; no nested bullets | Contradict each other on bullets (see F8) | partly: choose per medium |
| A2A / MCP message models | Role + typed parts; task state; artifacts separate from chat; opaque agents | Specify transport, not prose quality | partly: copy the separation, not the schema |
| Delegation guidance (multi-agent research, MAST) | Objective, output format, tool guidance, boundaries; failure taxonomy | MAST is descriptive, not a fix | yes: sets the agent-message checklist |
| Spec-driven dev (Spec Kit, Kiro, Osmani) | What/why vs how; tasks testable alone; boundaries; one example over prose | Mostly vendor claims; no controlled error-rate data | partly: use structure, skip ceremony |
| EARS "WHEN… THE SYSTEM SHALL…" | Testable, one behavior per line | Is exactly the legalistic voice CRISP rejects | no: use plain "When X, do Y" |
| Manus-style cache discipline | Stable prefix, append-only, keep errors, files as memory | Infra-level, partly irrelevant to prose | partly: append-only and file refs |

## Findings

### F1. Aim for the smallest set of high-signal tokens; minimal does not mean short
- Evidence: "Effective context engineering for AI agents," Anthropic Applied AI, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Strength: well-supported (context rot is measured; the guidance is Anthropic's synthesis)
- Implication for CRISP: the rule is "every sentence changes what the reader does," not "be short." Never cut a constraint to save tokens.

### F2. Wrong altitude fails both ways: brittle if-else rules, or vague text that "falsely assumes shared context"
- Evidence: same Anthropic post, "right altitude" section. Anthropic prompting guide: "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md
- Strength: well-supported (stated by the lab that trains the models; Anthropic reports no ablation)
- Implication for CRISP: "don't restate shared context" has a floor. Skip what the reader already has (files, earlier turns). State what they can't see: goal, constraints, definitions. Test: could a competent engineer with zero history act on it?

### F3. Context files rarely raise success and cost more; they work for non-standard practices, not overviews
- Evidence: Gloaguen et al., "Evaluating AGENTS.md," arXiv 2602.11988, 2026: no general gain in task success, inference cost up >20%; instructions are followed, repo overviews "are not helpful." https://arxiv.org/abs/2602.11988v2. Khatri, arXiv 2607.27250, 2026: 288 runs, correctness effect bounded to ≤10–15pp. https://arxiv.org/html/2607.27250v1
- Strength: well-supported (two studies, small task sets; Python-heavy)
- Implication for CRISP: standing instructions hold only what the agent cannot infer from code (odd commands, gotchas, "never do X"). Drop architecture tours and style rules a linter enforces. Agents obey explicit instructions, so each line costs attention.

### F4. Prune by deletion test; emphasize one line, not many
- Evidence: "Best practices for Claude Code," Anthropic. "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it." "If you emphasize many lines, none of them stands out." https://code.claude.com/docs/en/best-practices
- Strength: reasonable hypothesis (practitioner guidance; consistent with F3)
- Implication for CRISP: allow one emphasis marker per document, on the single rule that keeps being missed. Do not shout (no stacked "IMPORTANT/MUST/NEVER").

### F5. Best agent files lead with commands, show one code example, and set tiered boundaries
- Evidence: Matt Nigh, GitHub Blog, 2025, 2,500+ agent files: commands early with flags; "One real code snippet showing your style beats three paragraphs"; named stack with versions; always / ask first / never. https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
- Strength: reasonable hypothesis (descriptive survey, no outcome measure, GitHub-authored)
- Implication for CRISP: spec template order is commands/checks, then a concrete example, then boundaries. Express limits as Do / Ask first / Don't in plain words.

### F6. Keep rule files short, scoped, and by reference
- Evidence: Cursor docs, "Rules." "Keep rules under 500 lines"; "Reference files instead of copying their contents—this keeps rules short and prevents them from becoming stale"; "Add rules only when you notice Agent making the same mistake repeatedly." https://cursor.com/docs/rules.md
- Strength: stylistic preference (vendor guidance; the staleness argument is sound)
- Implication for CRISP: link to the file/line instead of pasting it. Copied context goes stale and then contradicts the source (see F11).

### F7. Labs' concision wording: numeric caps and ban lists (2025), shifting to short style instructions plus positive examples
- Evidence (verbatim):
  - Claude Code prompt (extracted, c. May 2025): "You MUST answer concisely with fewer than 4 lines (not including tool use or code generation), unless user asks for detail." "Avoid introductions, conclusions, and explanations." "You should NOT answer with unnecessary preamble or postamble (such as explaining your code or summarizing your action), unless the user asks you to." "You should minimize output tokens as much as possible while maintaining helpfulness, quality, and accuracy." (third-party extraction, link omitted)
  - Codex CLI prompt (official repo): "Default: be very concise; friendly coding teammate tone." "Don't dump large files you've written; reference paths only." "Lead with a quick explanation of the change… Do not start this explanation with 'summary', just jump right in." https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/gpt_5_codex_prompt.md
  - Cursor 2.0 prompt (leaked copy): "Bias towards being direct and to the point when communicating with the user." "Do not use too many LLM-style phrases/patterns." (leaked copy, link omitted)
  - Anthropic Opus 5 guide: "Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer." Progress updates: "your first sentence should answer 'what happened'… with supporting detail after it." Documents: "do not pad with filler sections, redundant summaries, or boilerplate." "Positive examples of the communication style you want tend to be more effective than instructions about what not to do." https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md
- Strength: well-supported that these exist and are used; effectiveness of each wording is unmeasured in public
- Implication for CRISP: use "answer first, then detail," a banned-opener list (no restating the question, no "Here is…", no closing summary), and "unless asked for detail." Skip "fewer than N lines": it caps useful detail and is tied to a CLI. Add one short before/after example.

### F8. Production formatting rules disagree on bullets, so CRISP must pick per medium
- Evidence: Claude.ai prompt (official): "It uses the minimum formatting appropriate to make the response clear and readable"; no bullets for reports or explanations; "Bullet points should be at least 1-2 sentences long." https://platform.claude.com/docs/en/release-notes/system-prompts/claude-opus-4-5.md. Codex prompt: bullets "merge related points; keep to one line when possible; 4–6 per list"; "no nested bullets/hierarchies"; backticks for commands and paths. (Codex URL in F7.)
- Strength: stylistic preference
- Implication for CRISP: reasoning and explanations in short prose. Parallel, independent items (findings, steps, options) as flat one-line bullets, 4–6 max, no nesting. Paths/commands in backticks.

### F9. Delegation messages need objective, output format, source/tool guidance, and boundaries; terse hand-offs cause duplicated work
- Evidence: "How we built our multi-agent research system," Anthropic, 2025: "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." A bare "research the semiconductor shortage" led to subagents duplicating work. https://www.anthropic.com/engineering/multi-agent-research-system. Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" arXiv 2503.13657: 1600+ traces, 14 failure modes in 3 clusters (system design, inter-agent misalignment, task verification). https://arxiv.org/abs/2503.13657
- Strength: well-supported (production evidence plus an annotated trace dataset; no per-field ablation)
- Implication for CRISP: agent-to-agent messages are not "as short as possible." Required fields: goal, output shape, scope/not-in-scope, done-check. Cut tone, pleasantries, and history the receiver already has.

### F10. A2A separates chat turns from deliverables and keeps agents opaque
- Evidence: A2A "Core Concepts." Message = role + typed Parts (text/file/data); Artifact = "the actual deliverables"; Task = stateful unit with lifecycle; Agent Card declares skills. https://a2a-protocol.org/latest/topics/key-concepts/. Anthropic multi-agent post, appendix: subagents write outputs to a filesystem and return "lightweight references" to avoid a "game of telephone."
- Strength: reasonable hypothesis (A2A is a transport spec; says nothing about wording; the telephone claim is Anthropic's anecdote)
- Implication for CRISP: status messages state state (working / blocked / done) plus a pointer to the artifact. Put bulk content in a file or code block and link it. Don't re-paste it into the message.

### F11. Contradictory, stale, or early-wrong context sticks; give the full spec up front
- Evidence: Drew Breunig, "How Long Contexts Fail," 2025: poisoning, distraction, confusion, clash. https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html. Laban et al., arXiv 2505.06120: sharded multi-turn prompts averaged a 39% drop; "when LLMs take a wrong turn in a conversation, they get lost and do not recover." https://arxiv.org/abs/2505.06120. Anthropic: Opus 5 "performs best when given the complete task specification up front." (Opus 5 guide, F7.)
- Strength: well-supported (benchmarked on single-vs-multi-turn; agent-spec reading is an inference)
- Implication for CRISP: a correction must say what it replaces ("Ignore my earlier X; use Y"). Do not trickle requirements across turns. Don't paste a second copy of something that may diverge from the first.

### F12. Append-only, stable prefix, restorable references beat rewriting and retelling
- Evidence: Yichao Ji, "Context Engineering for AI Agents: Lessons from Building Manus," 2025: keep the prefix stable; "Make your context append-only"; "leave the wrong turns in the context"; compress only restorably ("dropped… as long as the URL is preserved"). https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus. Anthropic: agents "maintain lightweight identifiers (file paths, stored queries, web links)." (F1 URL.)
- Strength: reasonable hypothesis (one production team's experience; cost numbers vendor-reported)
- Implication for CRISP: refer by path/ID/link, quote only the delta. Report failures plainly instead of hiding them. Updates append ("Update: …"); they don't silently rewrite earlier claims.

### F13. Spec structure that agents run well: what/why separate from how, tasks testable in isolation, a runnable check, explicit boundaries
- Evidence: GitHub Spec Kit post, 2025: "A vague prompt… forces the model to guess at potentially thousands of unstated requirements"; each task "something you can implement and test in isolation." https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/. Claude Code best practices: "Give Claude a check it can run"; "Have Claude show evidence rather than asserting success." (F4 URL.) Osmani, 2026: three-tier boundaries; split big specs; "curse of instructions." https://addyosmani.com/blog/good-spec/. Kiro: requirements.md in EARS, design.md, tasks. https://kiro.dev/docs/specs/feature-specs.md
- Strength: reasonable hypothesis (vendor and practitioner claims; I found no controlled study of spec sections vs error rate)
- Implication for CRISP: spec skeleton = Goal, Context pointers, Constraints/Non-goals, Interfaces/paths, Done-when (commands or observable results), Ask-first. Phrase criteria as plain "When X, Y happens," not SHALL.

### F14. Over-instruction backfires: models follow literally and add their own checks
- Evidence: Anthropic Opus 5 guide: "If your review prompt says 'only report high-severity issues' or 'be conservative,' the model may follow that instruction literally and report less"; explicit verification instructions "cause over-verification." Anthropic prompting guide: give the reason behind a rule ("will be read aloud by a text-to-speech engine, so never use ellipses"). (URLs in F2, F7.)
- Strength: well-supported for Claude models (vendor-measured); model-specific
- Implication for CRISP: prefer "rule + reason" over stacked prohibitions. Don't add "double-check everything." Phrase scope limits positively ("deliver what was asked").

### F15. Tool and parameter text should read like a note to a new hire, with unambiguous names
- Evidence: "Writing effective tools for agents," Anthropic, 2025: "think of how you would describe your tool to a new hire"; name `user_id`, not `user`; vague pairs cause wrong choices. https://www.anthropic.com/engineering/writing-tools-for-agents. "If a human engineer can't definitively say which tool should be used… an AI agent can't be expected to do better." (F1 URL.)
- Strength: well-supported (tool-description edits moved SWE-bench results per Anthropic)
- Implication for CRISP: define each term once, name things by what they are, and give one disambiguating sentence ("use X for…, not Y"). Same rule for identifiers in specs.

## Research questions
- **What improves clarity?** Reader-first context: goal, constraints, definitions, plus a concrete example (F2, F5, F13). The new-hire/colleague test (F2, F15).
- **What reduces ambiguity?** Explicit boundaries and a done-check (F13); unambiguous names (F15); explicit replacement of earlier statements (F11); full spec up front.
- **What reduces verbosity?** Answer first; banned openers/closers; reference not restate (F6, F7, F12). Effort/thinking settings don't shorten visible text; the instruction must (Opus 5 guide, F7).
- **What improves scanability?** Outcome-first first sentence; flat one-line bullets; backticked paths; commands early (F5, F7, F8).
- **Natural vs artificial?** Natural: Codex's "friendly coding teammate" and "no 'above/below', self-contained." Artificial: stacked MUST/NEVER, "fewer than 4 lines," SHALL-style EARS, LLM-isms Cursor bans (F7, F13).
- **What saves or wastes tokens?** Saves: pointers over pastes, deleting inferable content (F3, F6, F12). Wastes: repo overviews (+20% cost, no gain), padded docs, re-verification, spawning subagents for small jobs (Opus 5 guide).
- **Specs vs answers vs coding agents?** Specs: complete, structured, checkable (F13). Answers: short prose, answer first (F7, F8). Coding agents: commands, boundaries, runnable verification (F4, F5, F13). Agent-to-agent: goal/format/scope/done-check, state plus artifact pointer (F9, F10).
- **What can LLMs follow reliably?** Explicit instructions in context files are followed (F3). Literal style rules mostly work; vague ones and long lists degrade (F4, F14). One emphasized line holds better than many.
- **Evidence vs preference?** Evidence: context rot, 39% multi-turn drop, AGENTS.md null result, delegation failures (F3, F9, F11). Preference: bullet limits, 500-line cap, EARS vs prose, formatting taste (F6, F8, F13).

## Sources
1. Anthropic, "Effective context engineering for AI agents" (2025). https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
2. Anthropic, "Writing effective tools for agents" (2025). https://www.anthropic.com/engineering/writing-tools-for-agents
3. Anthropic, "How we built our multi-agent research system" (2025). https://www.anthropic.com/engineering/multi-agent-research-system
4. Anthropic, "Building effective agents" (2024). https://www.anthropic.com/engineering/building-effective-agents (read; supports ACI/tool-doc framing; no separate finding)
5. Claude Code docs, "Best practices." https://code.claude.com/docs/en/best-practices
6. Anthropic, "Prompting best practices" and "Prompting Claude Opus 5." https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md ; https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md
7. Anthropic, Claude.ai system prompts (Opus 4.5 entry). https://platform.claude.com/docs/en/release-notes/system-prompts/claude-opus-4-5.md
8. OpenAI Codex CLI prompt (official repo). https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/gpt_5_codex_prompt.md
9. Claude Code system prompt, third-party extraction (unofficial, c. May 2025; link omitted).
10. Cursor 2.0 system prompt, third-party leak (brad-luo). (leaked copy, link omitted) (unofficial)
11. agents.md site. https://agents.md/ (no required fields; nearest file wins; explicit chat prompts override)
12. Cursor docs, "Rules." https://cursor.com/docs/rules.md
13. GitHub Blog, "How to write a great agents.md" (Nigh, 2025). https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
14. Gloaguen et al., "Evaluating AGENTS.md," arXiv 2602.11988v2. https://arxiv.org/abs/2602.11988v2
15. Khatri, "Do Context Files Help Coding Agents?" arXiv 2607.27250. https://arxiv.org/html/2607.27250v1
16. Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" arXiv 2503.13657. https://arxiv.org/abs/2503.13657
17. Laban et al., "LLMs Get Lost In Multi-Turn Conversation," arXiv 2505.06120. https://arxiv.org/abs/2505.06120
18. A2A Protocol, "Core Concepts." https://a2a-protocol.org/latest/topics/key-concepts/
19. Breunig, "How Long Contexts Fail" (2025). https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html
20. Ji, "Context Engineering for AI Agents: Lessons from Building Manus" (2025). https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
21. GitHub, "Spec-driven development with AI" (Spec Kit, 2025). https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
22. Kiro docs, "Feature Specs." https://kiro.dev/docs/specs/feature-specs.md
23. Osmani, "How to write a good spec for AI agents" (2026). https://addyosmani.com/blog/good-spec/ (secondary; "curse of instructions" cited through him, not fetched)
