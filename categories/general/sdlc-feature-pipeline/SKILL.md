---
name: sdlc-feature-pipeline
description: "Use when building a feature the way a real company does — issue, branch, develop, test, PR, review, CI, staging, production deploy, and monitoring."
license: MIT
tags:
- workflow
- sdlc
- deployment
- git
---

# SDLC Workflow

## Overview

The standard feature development pipeline. Each stage has a purpose and an exit condition. The agent runs a stage, verifies the exit condition, then moves to the next. The pipeline is the industry way of turning an idea into shipped, monitored software:

```
Requirement → Planning → Design → Create Branch → Development → Testing → Commit
    → Push → Pull Request → Code Review → CI Checks → Merge → Staging Deployment
    → QA Testing → Production Deployment → Monitoring
```

This skill defines the **flow and the discipline**. The heavy lifting of each stage is delegated to the specialist skills that already exist in this collection.

## When to Use

- The user wants a feature built "the way a real company builds it".
- The user asks for a pull request, code review, CI checks, staging, or production deployment for a change.
- The change is destined for a shared repository and a live environment.
- The user says "follow the industry standard workflow" or "do this like a real project".

**When NOT to use:** throwaway experiments, local-only prototyping, or one-off scripts the user explicitly keeps off the shared repo. Run those directly without the pipeline.

## Relationship to loop-orchestrator

`loop-orchestrator` is the internal execution engine (DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP). This skill is the industry-facing pipeline. They compose:

- Run the loop engine for the BUILD-phase work (branch → develop → test → commit).
- Run this skill's gates for the SHIP-phase work (PR → review → CI → merge → staging → QA → production → monitor).
- Both share the same invariants: exit on evidence, not assertion; reviewer is separate from the builder; on repeated failure, stop and escalate to the user.

If the user gave a single prompt and expects a full feature, load `loop-orchestrator` to drive the phases and apply this skill's pipeline as the flow for the work.

## The Pipeline

### 1. Requirement

Decide what is being built and pin it down in writing.

- Write What, Why, Expected behaviour, and Edge cases.
- Record it as a GitHub Issue or Jira ticket (industry norm). If the user has no tracker, write the requirement block into the PR description instead.

**Exit condition:** a written requirement covers what, why, expected behaviour, and edge cases.

**Run:** `feature-forge` or `requirements-analysis`.

### 2. Planning

Assess impact before writing code.

- Database change? New API? Frontend change? Authentication impact? Security?
- Split the work into small, verifiable, ordered tasks.

**Exit condition:** a task breakdown exists with an order and each task has an acceptance criterion.

**Run:** `planning-and-task-breakdown`.

### 3. Design

Decide the shape of the change.

- Backend: endpoint contract (e.g. `POST /reset-password`).
- Database: tables or migrations (e.g. `password_reset_tokens`).
- Frontend: pages and flow (e.g. Email → OTP → Reset Password).
- For big features, produce a diagram or written design.

**Exit condition:** the design (API contract, schema, UI flow) is written down.

**Run:** `architecture-designer` for architecture-heavy work.

### 4. Create Branch

Never write directly on `main`. Create a descriptive branch:

```
feature/reset-password
feat/dark-mode
bugfix/crash
hotfix/server-error
refactor/auth
chore/update-eslint
```

**Exit condition:** a branch exists off the latest `main`, named with the convention above.

**Run:** `version-control`.

### 5. Development

Write the code with standard discipline.

- Small reusable functions, clean structure, no duplicate code, meaningful names.
- Build in thin slices; keep the repo working between slices.
- Comments explain *why* only — a human writes this code.

**Bad:** `let x`  |  **Good:** `const userProfile`

**Exit condition:** every planned slice is implemented and its acceptance criterion passes.

**Run:** `incremental-implementation` (per slice), plus the domain skill for the stack (e.g. `backend-craft`, `frontend-craft`, language skill).

### 6. Local Testing

The developer verifies their own work before sharing it.

Checklist:
- [ ] Build runs
- [ ] No errors
- [ ] Feature works
- [ ] Existing features did not break

**Exit condition:** build passes, tests pass, and the feature demonstrably works.

**Run:** `testing`, `test-master`.

### 7. Commit

Atomic, meaningful commits using Conventional Commits.

**Bad:** `update`, `changes`, `done`

**Good:**
```
feat(auth): add forgot password flow
fix(api): prevent duplicate email
refactor(user): simplify validation
```

Types: `feat:` `fix:` `docs:` `style:` `refactor:` `test:` `build:` `ci:` `perf:` `chore:`

**Exit condition:** every logical change is its own commit with a Conventional Commit message.

**Run:** `version-control`.

### 8. Push

```
git push origin feature/reset-password
```

**Exit condition:** the branch is on the remote.

### 9. Pull Request

Open a PR with a description that makes review easy:

```
## Feature
Forgot Password

## Changes
- Added API
- Added Email Service
- Added UI

## Testing
- Works on Chrome
- Works on Firefox
```

**Exit condition:** a PR exists with a description covering feature, changes, and testing.

### 10. Code Review

A reviewer (senior dev, or a separate agent/sub-agent — never the builder) checks the PR.

Check: logic, readability, performance, security, naming, architecture.

Review findings are concrete, e.g.:
- "Please rename this variable."
- "Use an async function."
- "Move this to the service layer."
- "Handle the null case."

The developer addresses findings, then the PR is approved.

**Exit condition:** no blocking review findings remain.

**Run:** `code-reviewer` (five-axis review). The reviewer must be separate from the builder — delegate to a sub-agent when possible.

### 11. CI Checks

Automated checks run on the PR. Anything failing blocks the merge:

```
Lint → Type Check → Unit Test → Build → Security Scan
```

**Exit condition:** all CI checks pass.

**Run:** `devops` / `version-control` (references/ci-cd-integration.md) for pipeline specifics.

### 12. Merge

Approved PR merges into `main`.

**Exit condition:** the change is on `main`.

**Run:** `version-control`.

### 13. Deploy to Staging

Deploy `main` to a staging server before production. QA tests against it.

**Exit condition:** the change is live on staging.

**Run:** `devops`, `cloud`.

### 14. QA Testing

QA checks edge cases, UI, mobile, browsers, bugs.

Bug found → developer → fix → new PR → deploy again.

**Exit condition:** QA signs off on the staged build.

**Run:** `testing`, `browser-testing-with-devtools` / `playwright-expert` for runtime evidence.

### 15. Production Deployment

Deploy `main` to production. Users see the feature.

**Exit condition:** the change is live in production with a recorded rollback plan.

**Run:** `devops`, `cloud`.

### 16. Monitoring

After deployment, watch logs, crashes, performance, errors, database.

If a serious issue appears → rollback, or a `hotfix/` branch.

**Exit condition:** no production incidents, or an incident is handled via rollback/hotfix.

**Run:** `monitoring`, `sre-engineer`.

## Rollback & Hotfix Rules

- **Rollback** when a deployed change breaks production: revert to the last known-good build/deploy. Record the rollback plan at deploy time so it is never improvised.
- **Hotfix** when a production bug needs an immediate fix: branch from `main` as `hotfix/<description>`, fix, test, PR, review (fast-track), merge, deploy, then merge back so `main` and hotfix never diverge.

## Solo-Developer Flow

Even alone, run the same process — it builds documentation and discipline:

```
GitHub Issue → Create Branch → Develop → Test → Commit → Push
→ Open PR (for yourself too) → Review your own code → Merge → Deploy
```

For self-review, switch perspective: re-read the acceptance criteria as a stranger to the code before judging. If a sub-agent is available, use it as reviewer.

## Per-Feature Checklist

For every new feature, work through this list in order:

1. Create a GitHub Issue.
2. Write the requirement (what, why, expected behaviour, edge cases).
3. Define acceptance criteria.
4. Create a `feature/...` branch.
5. Write the code.
6. Add/update tests.
7. Run lint and build.
8. Commit with a Conventional Commit message.
9. Push to GitHub.
10. Open a Pull Request with a description.
11. Review it yourself or get a friend/AI to review.
12. Merge.
13. Deploy to staging.
14. Verify.
15. Deploy to production.
16. Update the changelog.

## Loop Rules (shared with loop-orchestrator)

1. **Exit on evidence, not assertion.** Each stage completes only when its exit condition is met with evidence.
2. **Reviewer ≠ builder.** Code Review and QA never grade the developer's own work.
3. **Budget beats optimism.** If a stage fails twice (build, CI, review, deploy), stop and report to the user — do not silently retry.
4. **Never skip gates.** No merging before review+CI; no production before staging+QA, unless the user explicitly waives a stage.
5. **Escalate on repeated failure.** Two failed attempts in the same stage → stop and present the evidence.
