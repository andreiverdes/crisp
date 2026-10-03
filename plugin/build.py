#!/usr/bin/env python3
"""Assemble the standalone `crisp` plugin for Anthropic's directory into ../crisp-plugin (sibling checkout of horizon-loop/crisp-plugin).

The directory wants one plugin at the root of its own repo, every file inside the plugin folder,
no binaries, no system files. This copies skills/crisp verbatim and writes the manifest, README,
and LICENSE. Run after any change to skills/crisp, then commit and push crisp-plugin.
"""
import json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "crisp-plugin"
SKILL = ROOT / "skills" / "crisp"
VERSION = (ROOT / "plugin" / "VERSION").read_text().strip()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.iterdir():
        if p.name == ".git":
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()

    dst = OUT / "skills" / "crisp"
    shutil.copytree(SKILL, dst, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    # SKILL.md: the hosted <picture> banner is fine on GitHub but is noise inside the model's context; keep a one-line pointer instead.
    s = (dst / "SKILL.md").read_text()
    s = re.sub(r"<picture>.*?</picture>\n\n", "", s, count=1, flags=re.S)
    (dst / "SKILL.md").write_text(s)

    (OUT / ".claude-plugin").mkdir(exist_ok=True)
    (OUT / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": "crisp",
        "displayName": "CRISP",
        "version": VERSION,
        "description": "Say the useful thing once, then stop. A writing protocol for LLM replies, specs, status updates, and agent messages: answer first, no filler, no repetition, plain words, structure only when it helps. Adds /crisp and 'crispify this'.",
        "author": {"name": "HorizonLoop", "url": "https://github.com/horizon-loop"},
        "homepage": "https://andreiverdes.github.io/crisp/",
        "repository": "https://github.com/horizon-loop/crisp-plugin",
        "license": "MIT",
        "keywords": ["writing", "concise", "style", "prompting", "agents", "token-efficiency"],
    }, indent=2, ensure_ascii=False) + "\n")

    shutil.copy(ROOT / "LICENSE", OUT / "LICENSE")
    (OUT / "README.md").write_text((ROOT / "plugin" / "README.md").read_text().replace("{{VERSION}}", VERSION))
    n = sum(1 for p in OUT.rglob("*") if p.is_file() and ".git" not in p.parts)
    print(f"{OUT}: {n} files, version {VERSION}")

if __name__ == "__main__":
    main()
