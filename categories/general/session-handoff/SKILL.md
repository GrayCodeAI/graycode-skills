---
name: session-handoff
description: "Captures conversation state to a consolidated handoff file for resuming work across sessions: save, load, and clear operations scoped to the current project."
license: MIT
tags:
- handoff
- session
- context
- workflow
---

# Handoff

## Triggers

- **Save** ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff") → save.md
- **Load** ("resume session", "load handoff", "continue from last") → load.md
- **Clear** ("clear handoff", "reset handoff") → clear.md

Capture conversation state in one consolidated `.artifacts/HANDOFF.md` so a later session resumes with prior context. Three operations: save, load, clear.

## Workflow

```text
save  → consolidate current context into .artifacts/HANDOFF.md
load  → read the consolidated handoff
clear → overwrite .artifacts/HANDOFF.md with empty content
```
