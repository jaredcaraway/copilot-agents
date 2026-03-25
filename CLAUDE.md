# Copilot Agents

## What This Repo Is

A version-controlled library of agent instructions for Microsoft Copilot Studio. Claude is used to optimize these instructions for clarity and determinism — the instructions are still deployed to Copilot, not Claude.

## Constraints

- Agent instruction text must not exceed 8,000 characters (Copilot Studio limit). YAML frontmatter and markdown headings used for repo organization don't count toward this limit.
- Copilot Studio strips or corrupts vertical pipe characters (`|`) during processing. Use the `{PIPE}` placeholder token in instruction text; instruct the agent to convert `{PIPE}` to literal `|` only at output time.
- Avoid markdown tables in instruction text — Copilot Studio does not render them reliably.

## Workflow

1. User adds or updates agent files in `agents/` via GitHub
2. Claude optimizes instructions for clarity, conciseness, and deterministic behavior
3. User deploys the optimized instructions to Copilot Studio

## File Format

Each agent file has YAML frontmatter (name, description, platform, status, dates, tags) followed by the instruction text. See `agents/_template.md`.

## When Editing Instructions

- Be concise — every character counts against the 8K limit
- Write deterministic rules (explicit if/then, no ambiguity)
- Prefer numbered lists over markdown tables
- Always check character count after edits: `wc -c agents/<file>.md`
