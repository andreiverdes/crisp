#!/usr/bin/env python3
"""Assemble CRISP.md from design/parts/*.md and the frozen prompts. Re-run after any part changes."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTS = ROOT / "design" / "parts"
PROMPTS = ROOT / "skills" / "crisp" / "prompts"
ORDER = ["01-03-research", "04-13-core", "14-19-rules", "20-examples", "21-benchmark", "22-quickref", "23-prompts", "24-checklist"]

HEAD = """# CRISP

**Concise · Relevant · Intuitive · Simple · Protocol**

A writing protocol for humans and LLMs. Say the useful thing once, as clearly as possible, then stop.

Start here: section 7 (the ten rules), section 22 (one-screen reference), section 23 (drop-in prompts). The skill lives in `skills/crisp/`; `python3 skills/crisp/scripts/install.py` adds CRISP to a project's `AGENTS.md` or `CLAUDE.md`.

"""

def toc(text: str) -> str:
    lines = []
    for m in re.finditer(r"^## (\d+)\. (.+)$", text, re.M):
        n, title = m.groups()
        anchor = re.sub(r"[^a-z0-9 -]", "", f"{n} {title}".lower()).replace(" ", "-")
        lines.append(f"{n}. [{title}](#{anchor})")
    return "## Contents\n\n" + "\n".join(lines) + "\n\n"

def main():
    body = []
    for name in ORDER:
        p = PARTS / f"{name}.md"
        if not p.exists():
            raise SystemExit(f"missing part: {p}")
        body.append(p.read_text().rstrip() + "\n")
    text = "\n".join(body)
    for key, fn in [("CRISP", "crisp.md"), ("MINIMAL", "crisp-minimal.md"), ("FULL", "crisp-full.md")]:
        text = text.replace("{{" + key + "}}", (PROMPTS / fn).read_text().strip())
    out = HEAD + toc(text) + text
    (ROOT / "CRISP.md").write_text(out)
    words = len(out.split())
    print(f"CRISP.md: {words} words, {out.count(chr(10))} lines, {len(re.findall(r'^## ', out, re.M))} sections")

if __name__ == "__main__":
    main()


def sync_skill_refs():
    """skills/crisp/reference/* are verbatim copies of sections 18 and 20."""
    rules = (PARTS / "14-19-rules.md").read_text()
    i, j = rules.index("## 18. Anti-patterns"), rules.index("## 19. Crispification process")
    ap = rules[i:j].rstrip().replace("## 18. Anti-patterns", "# CRISP anti-patterns", 1)
    ex = (PARTS / "20-examples.md").read_text().rstrip().replace("## 20. Before/after examples", "# CRISP before/after examples", 1)
    ref = ROOT / "skills" / "crisp" / "reference"
    (ref / "anti-patterns.md").write_text(ap + "\n\nFull protocol: https://github.com/andreiverdes/crisp/blob/main/CRISP.md\n")
    (ref / "examples.md").write_text(ex + "\n\nFull protocol: https://github.com/andreiverdes/crisp/blob/main/CRISP.md\n")
    print("synced skills/crisp/reference/")


if __name__ == "__main__":
    sync_skill_refs()
