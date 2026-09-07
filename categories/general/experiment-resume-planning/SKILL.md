---
name: experiment-resume-planning
description: "Summarize prior ideas and experiments for a project and decide whether to resume, promote, branch, or start new work."
license: Apache-2.0
tags:
- experiments
- workflow
---

# Resume From Index

This is a flat, standalone `labnb-resume` skill so every AI coding agent can discover it directly. It is a focused companion to the broader `labnb` skill.

Helper scripts referenced as `skills/labnb/scripts/...` ship with the installed `labnb` skill; resolve them relative to that skill's directory (for example `~/.claude/skills/labnb/scripts/` or `~/.agents/skills/labnb/scripts/`), not the repository layout.

Use this skill before starting new lab notebook work for a project.

## Guardrails

1. Respect any parent constitution, project policy, or task-level write constraint already in scope.
2. Review those rules before deciding whether to resume, branch, or start fresh.
3. Prefer the safer pickup point when two choices would create competing writes to the same source tree.
4. Review status and provenance for matching entries before choosing where to pick up.
5. Treat provenance as best-effort; external changes may exist outside labnb tracking.
6. When reading provenance, expect W3C PROV-O terms rather than custom event keys.
7. Review the selected entry's local rules and memory before recommending the next action.

## Flow

1. Resolve the lab root.
2. Review the parent constitution and local project guardrails.
3. Derive the project slug.
4. Run:

```bash
python skills/labnb/scripts/summarize_index.py \
  --lab-root "$LAB_ROOT" \
  --project-slug "$PROJECT_SLUG"
```

5. Summarize:
   - relevant ideas
   - active experiments
   - completed experiments worth branching from
   - the best current pickup point
   - the entry-local rules and durable memory that still apply
6. Choose one path:
   - resume an active experiment
   - promote an idea into a new experiment
   - create a child experiment from prior work
   - register a new idea or experiment

Do not skip this step when the user is asking to start or continue lab notebook work.
