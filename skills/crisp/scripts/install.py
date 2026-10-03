#!/usr/bin/env python3
"""Add (or remove) the CRISP directive in a project's AGENTS.md / CLAUDE.md.

Usage:
  install.py                 # update AGENTS.md and CLAUDE.md that exist in cwd; create AGENTS.md if neither exists
  install.py --file CLAUDE.md
  install.py --level minimal # /crisp (default) | minimal | full
  install.py --command       # also write .claude/commands/crisp.md so `/crisp` works as a slash command
  install.py --print         # show the block, change nothing
  install.py --remove        # remove the block (and the command file if --command)
  install.py --check         # exit 0 if the block is present and current

The block is delimited by <!-- crisp:start --> / <!-- crisp:end --> and replaced in place on re-run.
Prompt text is read from ../prompts/ so this script never drifts from the skill.
"""
import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROMPTS = HERE.parent / "prompts"
START, END = "<!-- crisp:start -->", "<!-- crisp:end -->"
LEVELS = {"crisp": "crisp.md", "minimal": "crisp-minimal.md", "full": "crisp-full.md"}
COMMAND = pathlib.Path(".claude") / "commands" / "crisp.md"


PROTOCOL_URL = "https://github.com/andreiverdes/crisp/blob/main/skills/crisp/SKILL.md"


def block(level: str) -> str:
    body = (PROMPTS / LEVELS[level]).read_text().strip()
    skill = HERE.parent / "SKILL.md"
    try:
        pointer = f"`{skill.relative_to(pathlib.Path.cwd())}`"
    except ValueError:
        pointer = PROTOCOL_URL  # never write a machine-specific absolute path into a shared file
    return (
        f"{START}\n"
        "## CRISP\n\n"
        "Always reply in CRISP. Run the CRISP pass on your draft before answering; reason as much as the task needs. "
        "A request such as \"crispify this\", \"make this crispier\", or \"/crisp\" asks for the same transformation: "
        "keep the useful meaning, remove the rest.\n\n"
        f"{body}\n\n"
        f"Full protocol (rules, levels, checklist, examples): {pointer}.\n"
        f"{END}\n"
    )


def command_file() -> str:
    body = (PROMPTS / "crisp.md").read_text().strip()
    return (
        "---\n"
        "description: Apply CRISP (concise, relevant, intuitive, simple) to all following output; "
        "with text or a level (1-3) as argument, crispify that text or set the depth.\n"
        "---\n"
        f"{body}\n\n"
        "If an argument follows, treat it as follows: a lone 1, 2, or 3 sets the depth "
        "(1 = answer and essentials only; 2 = default; 3 = add rationale, alternatives, edge cases); "
        "any other text is to be crispified: rewrite it with the rules above and output only the rewrite.\n\n"
        "Argument: $ARGUMENTS\n"
    )


def splice(text: str, new: str) -> str:
    if START in text and END in text:
        head = text[: text.index(START)]
        tail = text[text.index(END) + len(END):].lstrip("\n")
        return head.rstrip("\n") + ("\n\n" if head.strip() else "") + new + ("\n" + tail if tail else "")
    return text.rstrip("\n") + ("\n\n" if text.strip() else "") + new


def strip(text: str) -> str:
    if START not in text or END not in text:
        return text
    head = text[: text.index(START)].rstrip("\n")
    tail = text[text.index(END) + len(END):].lstrip("\n")
    return (head + "\n\n" + tail).strip("\n") + "\n" if (head.strip() or tail.strip()) else ""


def targets(explicit: str | None, root: pathlib.Path) -> list[pathlib.Path]:
    if explicit:
        return [pathlib.Path(explicit)]
    found = [root / n for n in ("AGENTS.md", "CLAUDE.md") if (root / n).exists()]
    return found or [root / "AGENTS.md"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", help="target file (default: AGENTS.md and CLAUDE.md in cwd)")
    ap.add_argument("--level", choices=LEVELS, default="crisp",
                    help="which prompt to embed: crisp (80 words, default), minimal (200), full (590)")
    ap.add_argument("--command", action="store_true", help=f"also write {COMMAND} for a /crisp slash command")
    ap.add_argument("--print", action="store_true", help="print the block, change nothing")
    ap.add_argument("--remove", action="store_true", help="remove the block (and the command file with --command)")
    ap.add_argument("--check", action="store_true", help="exit 0 if present and current, 1 otherwise")
    a = ap.parse_args()

    new = block(a.level)
    if a.print:
        sys.stdout.write(new)
        return 0

    rc = 0
    for path in targets(a.file, pathlib.Path.cwd()):
        old = path.read_text() if path.exists() else ""
        if a.check:
            ok = new in old
            print(f"{path}: {'current' if ok else 'missing or stale'}")
            rc |= 0 if ok else 1
            continue
        out = strip(old) if a.remove else splice(old, new)
        if out == old:
            print(f"{path}: unchanged")
            continue
        path.write_text(out)
        print(f"{path}: {'removed' if a.remove else 'updated' if old else 'created'}")
    if a.command and not a.check:
        cmd = pathlib.Path.cwd() / COMMAND
        if a.remove:
            if cmd.exists() and cmd.read_text() == command_file():
                cmd.unlink()
                print(f"{cmd}: removed")
            elif cmd.exists():
                print(f"{cmd}: left in place (not written by this script)")
        else:
            cmd.parent.mkdir(parents=True, exist_ok=True)
            text = command_file()
            if cmd.exists() and cmd.read_text() == text:
                print(f"{cmd}: unchanged")
            else:
                cmd.write_text(text)
                print(f"{cmd}: written")
    return rc


if __name__ == "__main__":
    sys.exit(main())
