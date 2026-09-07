---
name: experiment-run-loop
description: "Create and run a concrete lab notebook experiment with an isolated workspace, explicit budgets, and iterative logging."
license: Apache-2.0
tags:
- experiments
- workflow
- research
---

# Run Experiment

This is a flat, standalone `labnb-run` skill so every AI coding agent can discover it directly. It is a focused companion to the broader `labnb` skill.

Helper scripts referenced below as `skills/labnb/scripts/...` ship with the installed `labnb` skill; resolve them relative to that skill's directory (for example `~/.claude/skills/labnb/scripts/` or `~/.agents/skills/labnb/scripts/`), not the repository layout.

Use this skill when the work is concrete enough to execute now.

## Guardrails

1. Respect any parent constitution, project policy, or task-level write constraint already in scope.
2. Review the notebook index and the parent constitution before creating a new experiment.
3. If project files will change, work in a dedicated experiment git worktree when the source is under git, or a copied workspace otherwise, not the shared source tree.
4. Never let two active experiments write to the same worktree, checkout, or output directory.
5. If write scopes may overlap, separate the workspaces first and only then continue.
6. Set and review experiment status explicitly, defaulting to `started` unless a better state is known.
7. Track labnb-managed actions in provenance files, but treat that provenance as best-effort.
8. Require explicit confirmation before labnb performs deletions of artifacts, workspaces, or entry files.
9. When writing provenance, use W3C PROV-O terms instead of ad hoc event keys.
10. Use provenance as the source of truth for monitored slice state.
11. Re-read and update both the experiment's local rules and `memory.md` before substantive actions, waits, or handoffs.

## Flow

1. Review the parent constitution and local project guardrails.
2. Summarize prior notebook entries for the project.
3. Decide whether this should resume an existing run, branch from one, or start fresh.
4. Register the experiment:

```bash
python skills/labnb/scripts/register_experiment.py \
  --lab-root "$LAB_ROOT" \
  --project-root "$PWD" \
  --project-slug "$PROJECT_SLUG" \
  --experiment-slug "$EXPERIMENT_SLUG" \
  --objective "$OBJECTIVE" \
  --entry-kind experiment \
  --metric-name "$METRIC_NAME" \
  --direction "$DIRECTION" \
  --verify-command "$VERIFY_COMMAND" \
  --overall-budget "$OVERALL_BUDGET" \
  --loop-budget "$LOOP_BUDGET" \
  --source-id "$SOURCE_ENTRY_ID"
```

5. Budgets are required at experiment creation time; do not leave them implicit.
6. Repeat `--source-id` when the run stems from multiple ideas or previous experiments.
7. Start the monitored slice:

```bash
python skills/labnb/scripts/monitor_slice.py start \
  --experiment-dir "$EXPERIMENT_DIR"
```

8. Work in the dedicated workspace git worktree if the source is under git, or a copied workspace otherwise, when source files change.
9. Keep the loop small:
   - smallest useful first slice
   - verify mechanically
   - log outcome
   - continue only if the checkpoint justifies it
   - if comparing two alternatives by a metric, where one side may be one or more prior runs, design the smallest asynchronous evaluation path that can decide the comparison
   - if parallel follow-up experiments help answer the comparison, you may use subagents to run them as separate experiments, but count their resource usage against the same budget
10. Unless absolutely necessary, do not run long-lived work blindly; add enough logging, checkpoints, and external observability to inspect progress and consumption while it runs.
11. Before leaving any background command unattended, run `monitor_slice.py check` and decide whether a timer or watchdog should be started within the remaining budget. `check` can break the slice not only on budget but on governance (unauthorized/drifted, via `--governance-file`), engineering (pace too slow, stalled, runaway memory), correctness (repeated failures), or validity (no improvement, metric guardrail) signals; pass the relevant flags (`--reserve-seconds`, `--patience`, `--stall-seconds`, `--max-failures`, `--metric-guardrail`, `--usage-file`, `--governance-file`/`--min-trust-score`/`--break-on-drift`) and treat a non-zero exit as "stop, do not iterate again".
12. Before scheduling a new wait job, check whether this experiment already has a pending wait:
   - if the earlier wait still covers the needed follow-up, do not submit a duplicate; just wait on it
   - if the new wait supersedes the older one, cancel or replace the earlier wait first
   - do not leave overlapping waits for the same experiment unless you record why in `log.md`
13. Probe the run periodically from the outside by checking logs, checkpoint files, progress signals, and resource/consumption indicators.
14. If no timer or watchdog is appropriate or available, stop deliberately instead of leaving the run hanging:
   - `python skills/labnb/scripts/monitor_slice.py finish --experiment-dir "$EXPERIMENT_DIR" --final-status stopped`
   - write a resume checkpoint in `log.md`
   - note what command or verification step to restart on resume
15. Update `plan.md`, `memory.md`, and `log.md` when the local rules, waits, instrumentation, or safest resume point change.
16. Run `monitor_slice.py check` before continuing and `monitor_slice.py finish` when the slice ends.

Treat the overall budget as the cap for the whole proposed path, and the loop budget as the cap for the current slice. If the budget is exceeded, prefer the explicit status `budget_exhausted` and record the safest next resume point. If the goal is metric comparison, prefer a minimal asynchronous comparison checkpoint over waiting for the whole loop to conclude, and count any subagent follow-up work against the same budget unless it is explicitly deferred.
