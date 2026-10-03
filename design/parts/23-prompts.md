## 23. Compact system prompts

Three sizes, one behavior. Each is a file under `skills/crisp/prompts/`; `scripts/install.py` copies the chosen one into `AGENTS.md` or `CLAUDE.md`. The `/crisp` version is the one benchmarked in section 21.

### `/crisp` (80 words)

Inject into a live conversation. Meaning: apply CRISP to all following output unless told otherwise.

```
{{CRISP}}
```

### CRISP Minimal (200 words)

System prompt when context size matters. Adds the preamble examples, the vague-word replacements, and the formatting rules.

```
{{MINIMAL}}
```

### CRISP Full (590 words)

System prompt when compliance matters more than token overhead. Adds the priority order, the full ambiguity rules, the length table, the CRISP pass, and the crispify instruction.

```
{{FULL}}
```
