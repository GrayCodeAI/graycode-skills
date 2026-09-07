---
name: agent-rule-management
description: "Creates, lists, edits, extracts, and deletes project or user-level rules for coding agents from convention definitions."
license: MIT
tags:
- rules
- agent-config
- conventions
- configuration
---

# Rule Creator

Creates rules at project or user level and manages the rule set at both.

## Triggers

| Signal in input | Load |
|-----------------|------|
| "create / add / new rule", "convention", "standard", or a declarative description with no verb | create.md |
| "list / show rules", "what rules exist" | list.md |
| "edit / update / change rule X" | edit.md |
| "extract / split / move from AGENTS.md / CLAUDE.md", "AGENTS.md / CLAUDE.md is too big" | extract.md |
| "delete / remove rule X" | delete.md |

## Workflow

```text
trigger → dispatch → classify → context → destination → render → write
              |              |
              v              v
           list/edit     refuse (procedural / lifecycle / one-off)
           extract/del
```

Create runs the classifier and context check before rendering the template. The other modes skip classification.
