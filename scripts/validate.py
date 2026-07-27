#!/usr/bin/env python3
"""Validate agent files in agents/ against Copilot Studio constraints (see CLAUDE.md).

Checks, per agent file (files starting with "_" are skipped):
  1. Instruction text is <= 8,000 characters. Instruction text is the content of
     the "## Instructions" section (up to "## Notes" or end of file) when that
     heading exists; otherwise the entire body after the YAML frontmatter.
  2. No literal vertical bar characters in instruction text — use {PIPE}.
  3. No markdown tables in instruction text.
  4. Frontmatter exists and name, description, platform, status, created,
     updated are all non-empty.

Exit code 0 if all files pass, 1 otherwise. Always prints a per-agent
character-count report so headroom against the 8K limit is visible.
"""

import re
import sys
from pathlib import Path

LIMIT = 8000
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"
REQUIRED_KEYS = ["name", "description", "platform", "status", "created", "updated"]


def split_frontmatter(text):
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def extract_instructions(body):
    m = re.search(r"^## Instructions[ \t]*\r?$", body, re.MULTILINE)
    if not m:
        return body
    rest = body[m.end():]
    n = re.search(r"^## Notes[ \t]*\r?$", rest, re.MULTILINE)
    return rest[: n.start()] if n else rest


def check_file(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    if frontmatter is None:
        errors.append("missing YAML frontmatter")
    else:
        for key in REQUIRED_KEYS:
            m = re.search(rf"^{key}:[ \t]*(.*)$", frontmatter, re.MULTILINE)
            if not m or not m.group(1).strip():
                errors.append(f"frontmatter key '{key}' is missing or empty")

    instructions = extract_instructions(body).strip()
    count = len(instructions)

    if count > LIMIT:
        errors.append(f"instruction text is {count} chars — exceeds the {LIMIT} limit by {count - LIMIT}")

    for i, line in enumerate(instructions.splitlines(), start=1):
        if "|" in line:
            errors.append(f"literal '|' in instruction text (instruction line {i}) — use {{PIPE}} instead")
        if re.match(r"^\s*\|?[\s:-]*-{3,}[\s|:-]*$", line) and "-|-" in line.replace(" ", ""):
            errors.append(f"markdown table detected (instruction line {i}) — Copilot Studio does not render tables")

    return count, errors


def main():
    files = sorted(p for p in AGENTS_DIR.glob("*.md") if not p.name.startswith("_"))
    if not files:
        print("No agent files found in agents/", file=sys.stderr)
        return 1

    failed = False
    print(f"{'agent':<40}{'chars':>8}  status")
    print("-" * 62)
    for path in files:
        count, errors = check_file(path)
        status = "OK" if not errors else "FAIL"
        print(f"{path.name:<40}{count:>5}/{LIMIT}  {status}")
        for e in errors:
            failed = True
            print(f"    - {e}")
    print("-" * 62)
    print("All agents pass." if not failed else "Validation failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
