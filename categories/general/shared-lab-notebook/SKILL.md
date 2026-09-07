---
name: shared-lab-notebook
description: "Maintain a concurrency-safe global lab notebook across projects and sessions, with ideas, experiments, and isolated workspaces."
license: Apache-2.0
tags:
- notebook
- experiments
- research
---

# Lab Notebook

Use this skill when the user wants a reusable lab notebook that survives across tasks, projects, investigations, and sessions.

The key difference from repo-local `.lab/` workflows is that the lab root lives in a general location and must stay safe under parallel use.

## Constitution

This skill must inherit and obey any higher-level constitution, parent skill, project policy, task instruction, or user constraint already in scope.

Before taking action:

1. Review the parent instructions that govern the current task.
2. Review the notebook index for related ideas and experiments.
3. If you are resuming an existing idea or experiment, review its local rules, checklist, and durable memory in `idea.md`, `plan.md`, and `memory.md` before acting.
4. If the parent rules are stricter than this skill, follow the stricter rule.
5. If this skill is missing a guardrail required by the parent context, add the missing guardrail locally in your plan instead of assuming it is safe.

This skill never overrides:

- user instructions
- project-specific safety or contribution rules
- higher-level constitutions about writes, approvals, secrets, or external side effects

## Companion Skills

Use these focused companion skills when a narrower task is enough:

- `labnb-resume`: summarize prior ideas and experiments for a project and decide where to pick up
- `labnb-idea`: register an unimplemented experiment idea in the shared notebook
- `labnb-promote`: turn an existing idea into a concrete experiment with explicit budgets and provenance
- `labnb-run`: create and run a concrete experiment with budgets, isolated workspace, and iteration logging

Each focused action installs as its own flat top-level `labnb-*` skill directory rather than as a skill nested inside this one. Keeping every skill flat (no `SKILL.md` nested under another skill) is what lets the whole `skills/` tree install into agents such as Claude Code that do not support skills nested inside other skills, while Codex and other agents discover the same flat entries directly.

## Helper Script Location

The commands below write paths like `skills/labnb/scripts/<name>.py`. That is the path **inside this repository**, and it only resolves when you run from the repo root. When this skill is installed into an agent, the helpers live next to this `SKILL.md`, under `<this-skill-dir>/scripts/<name>.py` — for example `~/.claude/skills/labnb/scripts/` or `~/.agents/skills/labnb/scripts/`. Resolve the script path relative to wherever this `SKILL.md` actually lives rather than assuming the repository layout, e.g.:

```bash
# Directory of the installed labnb skill (the folder containing this SKILL.md).
LABNB_SCRIPTS="<this-skill-dir>/scripts"
python "$LABNB_SCRIPTS/register_experiment.py" --help
```

The `labnb-*` companion skills do not bundle these scripts; they call the ones from the installed `labnb` skill.

## Default Root

Use this location unless the user explicitly wants another path:

```bash
${LAB_NOTEBOOK_ROOT:-${XDG_STATE_HOME:-$HOME/.local/state}/lab-notebook}
```

This keeps the notebook outside any single project tree and outside any specific agent runtime, while still making it easy to override.

## Interactive Setup Gate

Before starting a new experiment, gather or infer these fields:

1. Goal
2. Mechanical metric
3. Direction: higher or lower is better
4. Verify command
5. Writable scope
6. Workspace placement: use the default notebook workspace path, or link the workspace to a different location for large worktrees, datasets, or rich outputs
7. Time budget or timebox, if the user gave one
8. Stop condition: target metric, iteration count, checkpoint, or manual stop

If any of the first four are missing and cannot be inferred safely, ask before starting. The notebook is global, but the experiment loop still needs a clear local objective.

If the user gives a time budget, treat it as a hard ceiling, not a target to consume.

The setup must answer three planning questions early:

1. What is the smallest useful iteration that can produce information or a decision?
2. What checkpoint would justify continuing into a second iteration?
3. If the budget is too small for even one useful iteration, say so clearly instead of pretending the work fits.

Treat the budget as applying to the whole proposed path, including any parallel branches, delegated work, or downstream follow-up experiments that you are suggesting now.

## Required Guarantees

1. Never use a fixed experiment directory name.
2. Never let two runs compete to rewrite the central index without a lock.
3. Never store the only copy of experiment state inside the project being studied.
4. Never delete or rewrite prior experiment rows from the central index.
5. Prefer deterministic helpers in `scripts/register_experiment.py` and `scripts/summarize_index.py` instead of ad hoc shell snippets.
6. Track labnb-managed creates and updates with best-effort provenance using W3C PROV-O terms inside each entry directory.
7. Require explicit user confirmation before labnb performs deletions.
8. Treat provenance as the source of truth for monitored slice state; do not rely on a separate mutable loop-state file.
9. Let `monitor_slice.py check` decide when to break a slice, and honor a break: it can stop on governance (unauthorized, policy-violating, or drifted), budget, engineering (pace, stall, resource), correctness (repeated failures), or validity (no improvement, guardrail) signals, and a non-zero exit means stop rather than start another iteration.

## Local Guardrails

Apply these guardrails even when the parent constitution does not spell them out explicitly:

1. Review the notebook index and the active task constitution before starting new work.
2. Never edit the original source tree directly when the experiment is supposed to use an isolated workspace.
3. If project files may change and the source is a git repository, create a dedicated git worktree in the experiment workspace first and do the edits there. If the source is not a git repository, copy it instead.
4. Never let two active experiments write to the same worktree, checkout, branch working tree, or results directory.
5. Treat parallel operations as potentially conflicting until the write scopes are proven disjoint.
6. If multiple experiments touch the same upstream source, keep their workspaces separate and link them only through notebook metadata, not shared writes.
7. Preserve append-only notebook history; record new state with new rows or child entries instead of rewriting prior conclusions.
8. Before resuming or branching, summarize related entries so you understand what has already been tried and what constraints still apply.
9. If the safe workspace strategy is unclear, pause and choose the safer option rather than writing into an ambiguous location.
10. Keep secrets, auth state, and external credentials outside experiment artifacts unless the parent constitution explicitly allows otherwise.
11. Treat provenance as best-effort only: external changes or deletions may still occur without labnb observing them.
12. Do not perform notebook-managed deletions without explicit confirmation from the user.
13. Unless absolutely necessary, do not run work blindly; instrument it well enough to inspect logs, checkpoints, progress, and resource consumption from outside the running process.

## Action Gate

Before any action that writes, waits, launches background work, or hands off control:

1. Review the parent constitution, notebook summary, and the entry-local rules/checklist plus `memory.md`.
2. Confirm that you have actually completed those checks; do not rely on memory from an earlier step.
3. If the local rules or checklist are stale, incomplete, or newly contradicted by the current situation, update them before proceeding.
4. Check whether there is already a pending wait job for this entry before creating another one.
5. Confirm the run is instrumented enough that you can inspect logs, checkpoints, progress, and resource usage periodically without guessing.
6. If the action changes the local operating rules or durable memory, write the updated rules and memory back into the idea or experiment entry and note the change in `log.md` when applicable.

## Lab Layout

```text
lab-notebook/
  ideas/
    <idea-id>/
      metadata.json
      idea.md
      memory.md
      provenance.jsonl
      provenance.md
  experiments/
    <experiment-id>/
      metadata.json
      plan.md
      memory.md
      log.md
      provenance.jsonl
      provenance.md
      results.tsv
      summary.md
      artifacts/
  workspaces/
    <experiment-id>/
  index/
    experiments.tsv
    index.md
  locks/
```

- `ideas/<idea-id>/`: not-yet-started or not-yet-promoted experiment ideas
- `experiments/<experiment-id>/`: one experiment per directory; no sharing across active runs
- `provenance.jsonl`: best-effort append-only provenance log using W3C PROV-O terms for labnb-managed actions
- `provenance.md`: human-readable provenance policy and caveats
- `memory.md`: durable local memory that should be re-read and updated as rules, waits, or resume points change
- `experiments/<experiment-id>/plan.md`: the setup gate plus current hypothesis
- `experiments/<experiment-id>/results.tsv`: local iteration ledger for this experiment
- `workspaces/<experiment-id>/`: per-experiment working area for an isolated git worktree or copied source tree
- `index/experiments.tsv`: append-only registry of ideas and experiments
- `index/index.md`: generated readable summary of known entries
- `locks/`: lock directories used for central updates

## Experiment Identity

Each experiment id must be unique and stable:

```text
<utc-timestamp>--<project-slug>--<experiment-slug>--<random-suffix>
```

Example:

```text
20260411T154512Z--speech-foundations--prosody-ablation--a1b2c3d4
```

The random suffix is mandatory. A timestamp plus slug alone is not enough for parallel work.

## Setup Flow

1. Resolve the global lab root.
2. Review the parent constitution, project rules, and any task-specific guardrails that apply to this run.
3. Derive a `project_slug` from the current project, investigation, source tree, or working directory name.
4. Pick an `experiment_slug` that describes the current investigation.
5. Before creating a new experiment, summarize the existing notebook entries for the project:

```bash
python skills/labnb/scripts/summarize_index.py \
  --lab-root "$LAB_ROOT" \
  --project-slug "$PROJECT_SLUG"
```

6. Use that summary to decide whether to:
   - resume an existing experiment
   - promote an existing idea into an experiment
   - create a child experiment from a prior run
   - or start a new experiment
7. Create the entry by running the helper:

```bash
python skills/labnb/scripts/register_experiment.py \
  --lab-root "$LAB_ROOT" \
  --project-root "$PWD" \
  --project-slug "$PROJECT_SLUG" \
  --experiment-slug "$EXPERIMENT_SLUG" \
  --objective "Short statement of the experiment goal" \
  --entry-kind experiment \
  --metric-name "$METRIC_NAME" \
  --direction "$DIRECTION" \
  --verify-command "$VERIFY_COMMAND" \
  --overall-budget "$OVERALL_BUDGET" \
  --loop-budget "$LOOP_BUDGET" \
  --source-id "$SOURCE_ENTRY_ID"
```

8. To record an idea that is not yet being run, use `--entry-kind idea` and omit experiment-only fields that are still unknown.
9. To promote an existing idea into a concrete experiment, use the dedicated helper:

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

10. Experiments must be created with explicit `--overall-budget` and `--loop-budget`; do not leave them unspecified.
11. Use one or more `--source-id` flags when an experiment stems from prior ideas or experiments.
12. Start the monitored loop slice before the first write-bearing iteration:

```bash
python skills/labnb/scripts/monitor_slice.py start \
  --experiment-dir "$EXPERIMENT_DIR"
```

13. Use `monitor_slice.py check` before another iteration or long-running verify step, and `monitor_slice.py finish` when the slice ends.
14. If the user wants the editable worktree or large outputs elsewhere, pass `--workspace-root "$WORKSPACE_ROOT"` and let the notebook create a stable link under `workspaces/<experiment-id>/`.
15. If code changes are involved and the source is a git repository, create a dedicated git worktree in the experiment's workspace before editing. If the source is not under git, copy it into the workspace instead.
16. If multiple agents are working on the same codebase, each agent must use its own separate worktree location. Never share a single git worktree or checkout across active agents.
17. Record baseline iteration `0` in `results.tsv` before code changes.
18. Work inside the returned experiment directory for notes, artifacts, and summaries.
19. Log progress inside that experiment directory, not in shared files.

## Configurable Options

The skill has two kinds of configurable inputs: notebook root settings and per-experiment registration options.

### Root Settings

- `LAB_NOTEBOOK_ROOT`: override the default global notebook location
- `XDG_STATE_HOME`: fallback base for the default notebook root when `LAB_NOTEBOOK_ROOT` is unset

### Registration Options

Use these helper flags when creating an experiment:

- `--lab-root`: explicit notebook root
- `--project-root`: source tree or task directory being studied; optional for ideas that are still abstract or for work that will create a new repo later
- `--project-slug`: stable short name for the project
- `--experiment-slug`: short name for this idea or experiment entry
- `--objective`: concise goal statement
- `--entry-kind`: `experiment` or `idea`
- `--status`: optional explicit state; defaults to `started` for experiments and `ideation` for ideas
- `--metric-name`: optional metric label
- `--direction`: optional optimization direction such as `higher` or `lower`
- `--verify-command`: optional mechanical check command
- `--overall-budget`: required for experiments; total budget for the whole experiment path, including proposed follow-up or parallel work unless deferred
- `--loop-budget`: required for experiments; budget or timebox for the current loop or iteration slice
- `--workspace-root`: optional external root for the real workspace location
- `--source-id`: repeatable link to one or more upstream ideas or experiments that this run stems from
- `--parent-id`: optional parent experiment id for child experiments

If `--metric-name`, `--direction`, or `--verify-command` are omitted, the helper records `TBD` in `plan.md`. For experiments, `--overall-budget` and `--loop-budget` must be specified at creation time.

Recommended statuses include:

- `ideation`
- `planned`
- `started`
- `stopped`
- `budget_exhausted`
- `completed`
- `terminated`
- `crashed`
- `deferred`
- `promoted`
- `archived`

The summary helper also supports:

- `--lab-root`: explicit notebook root
- `--project-slug`: project to summarize
- `--limit`: maximum number of recent matching entries to show

The slice monitor helper supports:

- `start`: begin a monitored loop slice
- `check`: refresh elapsed state, evaluate break conditions, update status, and exit non-zero when it decides to break
- `finish`: close the active slice with a final status

## Breaking A Slice Early

`monitor_slice.py check` is the loop's circuit breaker. It reads the provenance state plus `results.tsv` (and, optionally, a con/duct usage log) and returns a decision of `continue`, `warn`, or `break`. On `break` it moves the entry to a terminal status and **exits with a non-zero code (default `4`)** so a shell loop stops on its own:

```bash
while python skills/labnb/scripts/monitor_slice.py check \
    --experiment-dir "$EXPERIMENT_DIR" \
    --reserve-seconds 120 --patience 3 --stall-seconds 600 \
    --max-failures 2 --usage-file "$DUCT_INFO_JSON"; do
  run_one_iteration   # observe -> modify -> verify -> keep/discard -> log
done   # the loop ends the moment check decides to break
```

A check can break the slice for five classes of reason, not just elapsed time:

- **Governance** (`governance` category, highest priority): the agent is unauthorized, policy-violating, or drifted from its approved definition. Point `--governance-file` at a JSON verdict (`decision`/`trust_score`/`drift`) written by a governance tool such as the `kya` skill; `--min-trust-score` and `--break-on-drift` turn it into breaks. labnb stays dependency-free and only consumes the verdict. This gate fails closed: once `--governance-file` is set, a missing, unreadable, or malformed verdict is treated as a `block` rather than silently skipped.
- **Budget** (`budget`): the loop or overall budget is spent. Use `--reserve-seconds` to break while slack remains for verification, logging, and summary, and `--warn-fraction` (default `0.8`) to get an advisory `warn` before the cap.
- **Engineering** (`engineering`): the slice is too slow or wasteful even if time remains. Pace projection breaks when another iteration at the recent cadence will not fit the remaining loop budget (disable with `--no-pace`); `--stall-seconds` breaks when no new `results.tsv` row has appeared for too long; `--usage-file` with `--max-rss-bytes` / `--max-pmem` breaks on runaway memory read from a con/duct log.
- **Correctness** (`correctness`): `--max-failures` breaks after that many consecutive failed/crashed iterations.
- **Validity** (`validity`): `--patience` breaks when the metric has not improved for that many logged iterations (a plateau or drift, using the recorded `direction`), and `--metric-guardrail` breaks when the latest metric crosses a hard bound in the wrong direction.

When several conditions trip at once, governance outranks correctness, then budget, then engineering, then validity, and that primary reason chooses the terminal status (`blocked` for governance, `crashed` for correctness, `budget_exhausted` for budget, `stopped` otherwise). Override the status with `--status-on-break`, keep the legacy always-exit-0 behavior with `--exit-zero`, and treat a `warn` decision as advisory (it does not change status and exits `0`). The full decision, signals, and diagnostics are written into the provenance state snapshot for later review.

Notes on the break semantics:

- A break does **not** close the slice. After handling it, call `monitor_slice.py finish` (for example `--final-status stopped` or `--final-status crashed`) before starting a new slice; a fresh `start` on an unclosed slice errors with "slice already running".
- The per-slice signals (stall age, pace cadence, consecutive failures) are scoped to the rows logged at or after the current slice started, so a resumed slice is not penalized for a previous one. The no-improvement / `--patience` signal is intentionally cumulative across the whole experiment — it asks whether the metric has improved at all lately.
- `--patience` treats a tie as non-improving (the comparison is strict). A long run of equal-metric iterations will therefore break as a plateau; raise `--patience`, or rely on `--metric-guardrail`, if tied-but-acceptable iterations should keep the loop alive.

## What Goes In Each Entry

For ideas:

- `metadata.json`: creation metadata, status, budgets, provenance mode, and linkage to future work
- `idea.md`: rationale, prior evidence to revisit, pickup criteria for promotion, and entry-local rules/checklist
- `memory.md`: durable memory for future pickup, waits, and resume conditions
- `idea.md`: also carries entry-specific rules and a pre-action checklist that should be reviewed and updated as the idea evolves
- `provenance.jsonl`: append-only best-effort PROV-O event log
- `provenance.md`: provenance rules and deletion policy

For experiments:

- `metadata.json`: creation metadata, source path context, objective, ids, status, provenance mode, and `source_ids`
- `plan.md`: goal, metric, direction, verify command, scope, next hypothesis, and entry-local rules/checklist
- `memory.md`: durable memory for future pickup, waits, and resume conditions
- `plan.md`: also carries entry-specific rules and a pre-action checklist that must be reviewed before each substantive action
- `log.md`: chronological notes for the experiment
- `provenance.jsonl`: append-only best-effort PROV-O event log
- `provenance.md`: provenance rules and deletion policy
- `results.tsv`: one row per iteration or thought with status and metric outcome
- `summary.md`: final concise outcome
- `artifacts/`: scratch outputs, plots, reports, and temporary files worth keeping
- dedicated workspace path: a safe place to edit without colliding with another agent's git state, preferably via a dedicated git worktree
- optional workspace link path under the notebook: a stable pointer when the real workspace lives elsewhere

Keep detailed notes local to the idea or experiment directory. The global index should stay compact.

## Improvement Loop

Use the same tight loop pattern that powers autoresearch, but anchor it in the global notebook:

1. Observe: run the index summary first if you have not already done so for this project, then read `plan.md` or `idea.md`, `memory.md`, especially the entry-specific rules and pre-action checklist, plus the tail of `log.md`, `results.tsv`, and relevant project state.
2. Re-check the parent constitution and project rules before any write-bearing step.
3. Start or check the monitored slice with `monitor_slice.py`; use provenance as the source of truth for remaining time.
4. Confirm you are working inside the experiment's dedicated worktree if project files will change and the source is under git. Otherwise confirm you are in the copied workspace.
5. Convert any user time budget into a bounded iteration plan:
   - pick the smallest useful first slice
   - define the checkpoint for continuing
   - leave explicit slack for logging, verification, and handoff
   - if no useful slice fits, record that the budget is insufficient
   - if the task compares two alternatives by a metric, where one side may be one or more prior runs, plan the smallest route that can produce a trustworthy comparison even if the full loop is not finished
6. Pick one focused change. Prefer atomic edits so the outcome is explainable.
7. If tracked project files change, commit before verification so rollback is cheap.
8. Run the verify command and capture the metric.
   - if the metric comparison can be produced asynchronously, prefer launching the minimal measurement path plus an explicit wait/checkpoint over keeping the whole loop in the foreground
   - if useful, delegate follow-up measurements or comparisons to subagents running in parallel experiments, but count the actual resource usage of those subagents against the stated budget
9. Keep or discard:
   - keep when the metric improves
   - keep when the metric ties and the result is clearly simpler
   - discard or revert when the metric regresses or the run crashes
10. Log the outcome in both `results.tsv` and `log.md`.
11. Unless absolutely necessary, do not launch a long-running command blindly. Add enough logging, checkpointing, and external observability that you can inspect what it is doing while it runs.
12. Before any background command or long-running job is left unattended, run `monitor_slice.py check` and decide whether the run needs a timer, watchdog, scheduler, or other explicit follow-up tied to the remaining budget.
13. Before scheduling any new wait job, check whether this experiment already has a pending timer, watchdog, scheduler entry, or other wait condition:
   - if the existing wait already covers the needed follow-up, do not schedule a duplicate; just wait on the existing one
   - if the new wait supersedes the old one, cancel or replace the earlier wait first
   - never leave multiple overlapping wait jobs for the same experiment without a clear reason recorded in `log.md`
14. Probe the run periodically from outside the main process by checking logs, checkpoint files, progress signals, and resource/consumption indicators rather than assuming it is healthy.
15. If no timer or watchdog is appropriate or available, do not leave the run implicitly hanging:
   - finish the current slice with `monitor_slice.py finish --final-status stopped`
   - record a resume checkpoint in `log.md`
   - note what command to restart or re-check on resume
16. Run `monitor_slice.py check` before continuing, and `monitor_slice.py finish` when the slice ends. Pass the break conditions that matter for this run (`--reserve-seconds`, `--patience`, `--stall-seconds`, `--max-failures`, `--metric-guardrail`, `--usage-file`); if `check` exits non-zero, stop the slice instead of starting another iteration. See "Breaking A Slice Early".
17. Decide whether another iteration is justified, rather than expanding work to fill the remaining budget.
18. Repeat until `check` breaks the slice, the stop condition is reached, the next checkpoint fails, or the user interrupts. A break can come from governance (unauthorized or drifted), budget, engineering (too slow, stalled, or resource-hungry), correctness (repeated failures), or validity (no improvement or a guardrail breach), not only from elapsed time.

When the work diverges materially, register a child experiment instead of overloading the current one.

## Budget And Iteration Policy

Use time budgets to shape the experiment, not to maximize activity.

1. A budget is a cap on work, not a requirement to use all allotted time.
2. Prefer a plan with one informative first slice and one optional next slice over a long speculative roadmap.
3. Reserve some of the budget for setup, verification, logging, and summarizing.
4. Include any proposed parallel experiments, child experiments, or downstream follow-up in the same budget reality check unless you state clearly that they are outside the current budget.
5. When an experiment draws on multiple ideas or prior runs, list all of them as source entries at creation time.
6. If the likely useful first slice already exceeds the available budget, say the plan is not feasible as stated.
7. If the task is a metric comparison between two alternatives, where one side may be represented by prior run or runs, prefer a shortest credible comparison path that can produce the decision asynchronously without requiring the entire loop to finish first.
8. If parallel follow-up experiments are delegated to subagents, count their compute time, wait time, and any other meaningful resource usage against the same budget unless you explicitly scope them out as later work.
9. If the task is open-ended, propose a shortest credible iteration path and stop at the first decision point.
10. When reporting the plan, distinguish:
   - what fits now
   - what becomes possible only if the first slice succeeds
   - what is out of scope for the current budget
11. If a running slice exceeds its loop or overall budget, mark it explicitly as `budget_exhausted`, summarize what completed, and record the next safe resume point instead of silently treating it as a normal stop.

## Shared Index Rules

The central index exists to answer: what ideas and experiments exist, where are they, and what are they about?

When creating or updating the shared index:

1. Acquire `locks/index.lock` using an atomic directory create.
2. Append exactly one row per new idea or experiment to `index/experiments.tsv`.
3. Rebuild `index/index.md` from `experiments.tsv` while the lock is held.
4. Write the regenerated markdown to a temp file and rename it into place atomically.
5. Release the lock even on failure.
6. Keep status current in new rows or explicit follow-up events rather than silently mutating history.

If a lock appears stale, only clear it after confirming the owning process is gone. Prefer waiting over forcing.

## Parallel Work Rules

1. Every active experiment gets its own directory.
2. Two agents may read the same project, but they must not share the same new experiment directory.
3. If two agents will both edit the same codebase, each one must create a separate git worktree under its own `workspaces/<experiment-id>/` path. If git worktrees are unavailable, use separate copied workspaces instead.
4. If multiple agents need related work, give each one a new experiment id and link them in notes instead of co-writing.
5. Treat `index/experiments.tsv` as append-only history.
6. If an experiment needs a follow-up, create a child experiment and record the parent id in `metadata.json` or `log.md`.

## Resume Flow

When resuming:

1. Run the summary helper or read `index/index.md` for the project slug.
2. Decide whether the best pickup point is a planned idea, an active experiment, or a completed experiment worth branching from.
3. Open the target idea or experiment directory.
4. Continue writing only inside that directory unless you are registering a new idea or experiment.
5. Register a fresh experiment instead of mutating old metadata if the scope or hypothesis changed materially.

## Notes For Agents

- Prefer the helper script over handwritten lock logic when the script is available.
- If you need a quick view of the notebook, run `scripts/summarize_index.py` or read `index/index.md` first and only inspect specific entry directories afterward.
- Before starting a new experiment, summarize relevant prior ideas and experiments and say where you are picking up from.
- When a run stems from multiple ideas or prior experiments, register all of them as `source_id` links instead of collapsing them into a single parent.
- Review the parent constitution and local project guardrails before planning or writing.
- Use the experiment's dedicated workspace path for editable project state; do not point multiple active agents at the same worktree.
- Prefer creating a dedicated git worktree in the experiment workspace before editing whenever the source tree is a git repository. If it is not, copy the source instead.
- Ask whether the workspace should live somewhere else when a source worktree, datasets, or generated artifacts would be better outside the notebook root.
- Re-use the same experiment directory for iterative logging, but create a new child experiment when you need a new loop with a new hypothesis or project state.
- Record unimplemented but promising directions as ideas instead of forcing them into active experiments.
- Track labnb-managed changes in provenance files, but say clearly that external changes may exist outside that record.
- Use W3C PROV-O terms in provenance records rather than ad hoc event fields.
- Use provenance as the source of truth for monitored slice state and remaining budget.
- Require explicit confirmation before deleting entry files, artifacts, or workspaces through labnb-driven actions.
- If the user gives a budget like "two hours," do not stretch the plan to fill two hours by default; start with the smallest decision-making slice and say when the budget is insufficient.
- If you propose parallel branches or downstream experiments, count them against the same stated budget unless you explicitly mark them as later follow-up outside the current scope.
- Before leaving a background command unattended, decide whether to start a timer, watchdog, scheduler, or follow-up hook that will check the run before the budget expires.
- Before submitting a new wait job, check for an existing pending wait for the same experiment and either reuse it or replace it; do not stack overlapping waits by default.
- Re-read and actively check off the entry-local rules/checklist before each substantive action rather than assuming you already satisfied them.
- When the local operating rules change, update `idea.md` or `plan.md` so later steps inherit the new constraints instead of rediscovering them.
- When facts, waits, resume points, or durable constraints change, update `memory.md` so later steps inherit the new memory instead of reconstructing it.
- If two alternatives are being compared by a metric, and one side may be one or more prior runs, prefer designing the smallest trustworthy asynchronous comparison path and an explicit checkpoint rather than keeping the whole experiment loop running until a full conclusion.
- If parallel follow-up experiments would help, you may use subagents to run them as separate notebook experiments, but count their resource usage against the same budget unless the user explicitly scopes them out.
- Unless absolutely necessary, do not run things blindly; prefer enough logging, checkpointing, and external health checks to inspect logs, progress, and resource consumption periodically.
- When a verify command or long-running job should be measured, wrap it with the `duct` skill so the experiment captures wall-clock time, CPU, and memory usage as structured logs that a later agent review can inspect.
- When a run is unattended, monitor it from the outside by probing logs, checkpoint files, and resource/progress signals instead of assuming the internal process is behaving.
- If you cannot supervise or schedule a background command safely, stop the slice deliberately, write a resume checkpoint, and say exactly how to resume.
- If the time budget is exceeded, treat that as `budget_exhausted` by default, summarize partial results, and record whether the next step is resume, branch, or stop.
- Keep instructions concise in user-facing updates; the notebook should do the long-term memory work.
