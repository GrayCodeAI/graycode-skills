---
name: task-lifecycle-orchestration
description: "Use when a single prompt expects a full feature or project from idea to ship, running DEFINE, PLAN, BUILD, VERIFY, REVIEW, SHIP phases as loops with deterministic exit criteria."
license: MIT
tags:
- workflow
- orchestration
- lifecycle
- planning
- verification
---

# Loop Orchestrator

## Overview

The agent lifecycle is six phases. Each phase is a **loop**: enter with a goal, run the inner work, and exit only when a deterministic condition is met. The loop, not the agent's confidence, decides when a phase is done.

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
  │       │       │        │        │       │
  loop    loop    inner    checker  loop    loop
                  loop
```

Two invariants govern everything:

1. **Termination is enforced by criteria, never by the agent's claim of done.** Every loop has an exit condition you can check with evidence (a file exists, tests pass, no blocking issues). If the exit condition is unmet, the loop keeps going or stops for a human — it never "completes" on assertion.
2. **The entity that verifies is separate from the entity that produces.** The BUILD phase does not grade its own work. VERIFY and REVIEW run as independent checks with fresh eyes.

## When to Use

- The user hands over a task with a single prompt and expects the full job, from idea to shipped.
- Work is large enough that it passes through multiple phases.
- A phase is stuck and you need to decide: retry, stop, or escalate.

**When NOT to use:** Single small fixes that stay in one phase (e.g. one bug, one review). Run that phase directly instead.

## Triage First — Scale the Loop to the Task

Before creating the tracker, classify the task. The lifecycle depth matches the task size; running the full lifecycle on a small task is overhead, running a thin loop on a large task is how work breaks.

| Level | Task shape | Loop to run |
|-------|-----------|-------------|
| L1 | One file, one change, trivial (fix typo, tweak CSS) | No orchestration. Execute directly. |
| L2 | A few files, bounded change (add a function, fix a bug) | BUILD → VERIFY only. No DEFINE/PLAN/REVIEW/SHIP. |
| L3 | A feature or module (new page, new endpoint) | PLAN → BUILD → VERIFY → REVIEW → SHIP. DEFINE only if the request is vague. |
| L4 | An app, project, or industry-scale system | Full lifecycle: DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP, with maker/checker separation and every quality gate. |

Rules:
- If unsure between two levels, use the higher one. Under-scoping causes rework; over-scoping is cheap.
- Record the level in the tracker. It explains why the loop is thin or full.
- Any task that needs more than one build-verify cycle is at least L3.

## The Human Checkpoint — Verify the Plan Once, Then Go

The loop is autonomous between two moments. The user's role is: give the prompt, approve the plan, review the result. Everything in between runs unattended.

1. **Intake** — one clarifying round if the request is vague. Do not interrogate; surface the 2-3 assumptions that most change the outcome.
2. **Plan approval (the only required gate)** — present the plan (tasks, acceptance criteria, order) and the expected output. Wait for approval. This is the one point where the user can correct direction cheaply.
3. **Autonomous run** — after approval, run the remaining phases without stopping for confirmation. Stop only on a loop rule: budget exhausted, two failed attempts, or an acceptance criterion that cannot be met.
4. **Delivery report** — finish with a short summary: what shipped, the evidence it passed (tests, build, runtime check), and what was left out.

If the user says "just do it, no need to ask", skip the intake round but still present the plan for approval before the autonomous run starts.

## The Tracker

Before starting, create a tracker file at `docs/LOOP.md` (create `docs/` if missing). It is the loop's memory across sessions.

```
# LOOP Tracker

Goal: <one-line statement of what the user asked for>
Success criteria: <checkable evidence that the goal is met>
Level: L1 | L2 | L3 | L4
Plan approval: pending | approved | not-needed
Budget per loop: <e.g. 3 iterations, or 30 tool calls, or a time limit>

## Phase Status
- DEFINE: pending | in-progress | done | blocked
- PLAN:   pending | in-progress | done | blocked
- BUILD:  pending | in-progress | done | blocked
- VERIFY: pending | in-progress | done | blocked
- REVIEW: pending | in-progress | done | blocked
- SHIP:   pending | in-progress | done | blocked

## Notes
<one line per phase: decision taken, evidence seen, why the loop stopped>
```

- At session start, read `docs/LOOP.md` first. A loop with a tracker is resumed, never restarted.
- Update the tracker at the end of every phase. This is the outer loop's memory.

## Phase Loops

### 1. DEFINE

**Enter when:** the task's goal or scope is not pinned down.

**Loop work:**
1. If the request is vague or underspecified, run `interview-me` or `idea-refine` to surface what the user actually wants.
2. Write the spec. Use `spec-miner` for existing codebases, `requirements-analysis` for new work.
3. Present assumptions and scope to the user.

**Exit condition (deterministic):** a spec exists (file or agreed text) covering objective, scope, and boundaries, AND the user has confirmed it.
**Budget:** if the spec is not confirmed after 2 clarification rounds, stop and ask directly.

### 2. PLAN

**Enter when:** a confirmed spec exists.

**Loop work:**
1. Run `planning-and-task-breakdown` to split the spec into small, verifiable tasks.
2. Order tasks by dependency. Give each an acceptance criterion.
3. For architecture-heavy work, run `architecture-designer` first.

**Exit condition:** every task has a concrete acceptance criterion and a dependency order, and the user has approved the plan (this is the one required human gate). After approval, the run continues autonomously through SHIP without further confirmation.
**Budget:** one pass. If a task cannot be made verifiable, split it or stop and ask.

### 3. BUILD (inner loop)

**Enter when:** an approved plan exists.

**Loop work — repeat per slice:**
1. Implement one slice following `incremental-implementation`.
2. Load the domain skills for the work (e.g. `frontend-craft`, `backend-craft`, `api-design`, or the language/library skill that matches).
3. Ground framework decisions in official docs with `source-driven-development`.
4. Write code a human wrote — comments explain *why* only, no commented-out blocks, no AI-tell patterns (generic names, redundant docstrings). The checkable bar is the Definition of Done Quality section.
5. Commit progress (`version-control`) so the system stays in a working state.

**Exit condition (deterministic):** every planned slice is implemented and its acceptance criterion passes, OR the iteration budget is exhausted.
**Budget:** if the same slice fails twice, STOP. Do not silently retry a third time — report the failure and the two attempted fixes.

### 4. VERIFY (independent checker)

**Enter when:** BUILD reports done.

**Loop work — fresh context, not the builder's:**
1. Run the tests (`testing`, plus `test-master` for test strategy). Verify against the acceptance criteria, not the builder's summary.
2. For browser work, run `browser-testing-with-devtools` or `playwright-expert` for runtime evidence.
3. If something fails, return the failing item to BUILD as a new slice with the failure attached.

**Exit condition:** all acceptance criteria have passing evidence (tests pass, runtime checks pass), OR the budget is exhausted.
**Budget:** if BUILD received a failing item and the same failure persists across 2 build-verify cycles, escalate to the user. No infinite loop.

### 5. REVIEW (quality gate)

**Enter when:** VERIFY passes.

**Loop work:**
1. Run `code-reviewer` for the five-axis review.
2. If too complex, run `code-simplification`. If security is in scope, run `security`.
3. Fix only what the review flags as blocking.

**Exit condition:** no blocking review findings remain.
**Budget:** if a reviewer finding cannot be resolved in 2 attempts, present the tradeoff to the user instead of forcing a fix.

### 6. SHIP

**Enter when:** REVIEW clears.

**Loop work:**
1. Check the ship checklist (docs updated, secrets absent, rollback path known). Use `devops` or `cloud` for deployment specifics.
2. Deploy incrementally with a rollback plan.

**Exit condition:** the change is live or the user confirms the delivery point, and the rollback plan is recorded.
**Budget:** if deployment fails twice, stop and hand over the deployment log.
**Delivery report:** close the loop with a short summary — what shipped, the evidence it passed (tests, build, runtime check), and what was deliberately left out. This is the second moment the user engages.

## Maker/Checker Separation

- BUILD is the **maker**: writes code, writes tests.
- VERIFY and REVIEW are **checkers**: independent passes. Prefer delegating them to a separate agent/sub-agent so the critic is not the author.
- A checker never accepts "it should work" as evidence. It requires tests passing, build output, or runtime data.
- If no separate agent is available, switch perspective explicitly: re-read the acceptance criteria as a stranger to the code before judging.

## Loop Rules

1. **Never exit a phase on assertion.** Exit only on the phase's deterministic condition.
2. **Budget beats optimism.** When the budget is hit, the loop stops and reports. Stopping to ask is a success, not a failure.
3. **One loop at a time.** Do not run BUILD and REVIEW simultaneously on the same work; review needs the completed, verified artifact.
4. **Resume, don't restart.** Read the tracker; continue from the last phase status.
5. **Escalate on repeated failure.** Two failed attempts in the same loop → stop and present the evidence to the user.
6. **One checkpoint, then autonomy.** After plan approval, do not re-ask between phases. The delivery report is the only follow-up.
7. **Match the loop to the level.** Do not run the full lifecycle on an L2 fix, and do not run a thin loop on an L4 system.

## Failure Modes

1. Treating "the agent thinks it's done" as completion — the loop's exit condition, not confidence, defines done.
2. Endless retry — silent loops without a budget burn tokens and hide the failure.
3. Builder grading its own work — skipping VERIFY/REVIEW because BUILD "already checked".
4. Restarting a resumed task because the tracker was ignored.
5. Applying the full lifecycle to a one-phase fix — overhead without value.
