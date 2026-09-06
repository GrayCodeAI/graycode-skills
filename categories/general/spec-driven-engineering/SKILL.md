---
name: spec-driven-engineering
description: "Drives feature work from specs with traceable requirements, design, tasks, implementation, audit, and validation phases."
license: MIT
tags:
- specification
- development-workflow
- feature-development
- agile
---

# Spec-Driven Development

Feature development in phases. Light by default; weight only where the change pays for it.

## Triggers

- **Specify** ("plan feature", "spec this", "from PRD", "modify feature", "discuss how to build") → specify.md
- **Design** ("design this feature", "technical design", "plan the build") → design.md
- **Tasks** ("create tasks", "break into tasks", "task breakdown") → tasks.md
- **Implement** ("implement task T-1", "implement T-1 to T-4", "implement slice S-1", "implement wave W-1", "execute tasks", "implement everything") → implement.md
- **Audit** ("audit feature", "validate goals", "verify before PR") → audit.md
- **Validate / UAT** ("run UAT", "manual testing", "validate flows") → validate.md
- **Archive** ("archive feature", "archive this spec") → archive.md

## Workflow

```text
specify → design → tasks → implement → [validate] → [audit] → [archive]
   └────────┴────────┴──────────┴──────────┴ a mechanical change skips all of this: one-liner → branch → implement inline
```

Specify's triage decides the path: a mechanical change with zero load-bearing decisions becomes a one-liner straight to inline implement on its own branch, and a prompt carrying outcomes that ship separately becomes one feature per outcome. Everything else produces the artifacts and runs the phases in turn. Verify is mental, per task, inside implement — never a user phase. Validate and audit are optional. Archive is manual housekeeping for a feature in any state, never automatic or suggested.
