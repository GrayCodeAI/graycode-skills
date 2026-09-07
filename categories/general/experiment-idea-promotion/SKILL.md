---
name: experiment-idea-promotion
description: "Promote a lab notebook idea into a concrete experiment with explicit budgets, source links, and provenance."
license: Apache-2.0
tags:
- experiments
- workflow
---

# Promote Idea

This is a flat, standalone `labnb-promote` skill so every AI coding agent can discover it directly. It is a focused companion to the broader `labnb` skill.

Helper scripts referenced as `skills/labnb/scripts/...` ship with the installed `labnb` skill; resolve them relative to that skill's directory (for example `~/.claude/skills/labnb/scripts/` or `~/.agents/skills/labnb/scripts/`), not the repository layout.

Use this skill when an existing idea is ready to become a real experiment run.

## Guardrails

1. Review the notebook index and the idea entry before promotion.
2. Require explicit experiment budgets at promotion time.
3. Preserve the original idea as notebook history; do not delete it.
4. Record the promoted experiment as stemming from the idea through source links and provenance.
5. Carry forward the idea's local rules and durable memory into the new experiment before further work begins.

## Flow

1. Identify the idea entry id.
2. Choose the experiment slug and required budgets.
3. Promote it:

```bash
python skills/labnb/scripts/promote_idea.py \
  --lab-root "$LAB_ROOT" \
  --idea-id "$IDEA_ID" \
  --project-root "$PROJECT_ROOT" \
  --experiment-slug "$EXPERIMENT_SLUG" \
  --metric-name "$METRIC_NAME" \
  --direction "$DIRECTION" \
  --verify-command "$VERIFY_COMMAND" \
  --overall-budget "$OVERALL_BUDGET" \
  --loop-budget "$LOOP_BUDGET"
```

4. Repeat `--source-id` if the new experiment should also stem from other prior entries.
5. Continue the run with `labnb-run`.
