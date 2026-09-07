---
name: experiment-idea-capture
description: "Record a promising but not-yet-implemented experiment idea in a shared lab notebook index."
license: Apache-2.0
tags:
- experiments
- notebook
- research
---

# Capture Idea

This is a flat, standalone `labnb-idea` skill so every AI coding agent can discover it directly. It is a focused companion to the broader `labnb` skill.

Helper scripts referenced as `skills/labnb/scripts/...` ship with the installed `labnb` skill; resolve them relative to that skill's directory (for example `~/.claude/skills/labnb/scripts/` or `~/.agents/skills/labnb/scripts/`), not the repository layout.

Use this skill when there is a useful direction to remember, but not enough evidence, time, or scope to run it now.

## Guardrails

1. Respect any parent constitution, project policy, or task-level write constraint already in scope.
2. Review the notebook index first so the idea does not duplicate an existing entry unnecessarily.
3. Capture speculative directions as ideas instead of opening active experiments that would encourage unsafe or premature writes.
4. Record idea status explicitly, defaulting to `ideation` unless a better status is known.
5. Treat provenance as best-effort; deletions still require explicit confirmation.
6. When writing or referring to provenance, use W3C PROV-O terms.
7. Review and update the idea's local rules and durable memory before any substantive follow-up action.

## Flow

1. Review the parent constitution and local project guardrails.
2. Summarize existing entries for the project first.
3. Choose a concise slug for the idea.
4. Register the idea:

```bash
python skills/labnb/scripts/register_experiment.py \
  --lab-root "$LAB_ROOT" \
  --project-slug "$PROJECT_SLUG" \
  --experiment-slug "$IDEA_SLUG" \
  --objective "$OBJECTIVE" \
  --entry-kind idea \
  --overall-budget "$OVERALL_BUDGET" \
  --loop-budget "$LOOP_BUDGET"
```

5. Fill in `idea.md` with:
   - why it matters
   - what prior evidence to revisit
   - the smallest useful first slice
   - what would justify promoting it into an experiment
6. Fill in `memory.md` with durable facts, pending waits, and the safest resume point.

Ideas should be first-class index entries, not buried in an active experiment log.
