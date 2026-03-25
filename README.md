# Copilot Agents

A version-controlled library of agent instructions used in Microsoft Copilot Studio.

## Structure

```
agents/
  <agent-name>.md    # One file per agent
```

Each agent file uses a consistent format with YAML frontmatter for metadata and the full instruction text below.

## Agent File Format

```markdown
---
name: Agent Name
description: What this agent does
platform: copilot-studio
status: active | draft | retired
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
---

# Agent Name

## Purpose

Brief description of what this agent does and when to use it.

## Instructions

The full agent instruction text goes here.
```

## Usage

1. Create a new `.md` file in `agents/` using the format above
2. Commit changes — git history tracks every revision
3. Use `git log agents/<name>.md` to view an agent's edit history
4. Use `git diff` to compare versions

## Porting to Claude

Agent files can be adapted for use with Claude by copying the instruction text and adjusting for Claude's prompting patterns. Notes on platform differences can be tracked in each file's frontmatter or in a separate section.
