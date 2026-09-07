---
name: embedded-codebase-integration
description: "Use when writing code in someone else's repo, a legacy or unknown stack, or a customer environment, to orient first, extract real requirements, and build in-place matching their conventions."
license: MIT
tags:
- codebase
- integration
- onboarding
- legacy
- engineering
---

# Forward Deployed Engineer

## Overview

The Forward Deployed Engineer (FDE) works **embedded at the customer** — in their repo, their stack, their infra, under their conventions. The agent is not the owner of the codebase; it is a professional contractor who must understand the environment, build in-place, and hand over work a real team can maintain.

The engagement arc:

```
EMBED → ORIENT → EXTRACT → BUILD IN-PLACE → HAND OVER
```

Unlike greenfield work (where the agent sets the defaults), FDE work inverts the rules: **the repo's conventions win, not your defaults.**

## When to Use

- The task is in an existing, legacy, or unfamiliar codebase — not something the user is building from scratch.
- The user says "this is the client's repo" or "work in their environment".
- The task is an integration into existing systems (auth, APIs, internal tools, legacy services).
- The repo has its own branch model, CI, review, and deployment process that must be respected.
- A non-technical stakeholder is describing the request and the real need is unclear.

**When NOT to use:** greenfield projects the user owns, throwaway experiments, or anything where the agent is the definitive owner of the code and its conventions. Run those directly or with `loop-orchestrator`.

## The Engagement Arc

### 1. EMBED — Know the Customer

Establish who and where before touching code:

- Who is the customer / stakeholder, and what outcome do they care about?
- What environment is the work happening in (repo, host, infra, access level)?
- What are the boundaries — what is the agent allowed to change vs. read-only?

**Exit condition:** a clear statement of the customer, the environment, and the boundaries.

### 2. ORIENT — Recon Before Code (the distinctive core)

Read-only exploration **before writing anything**. Do not assume the repo works like your defaults.

Explore, in order:
- Repo layout: folders, entry points, module boundaries.
- Language, runtime, and exact versions (read the dependency files, don't guess).
- Existing conventions: naming, error handling, folder structure, code style.
- CI setup: what checks run, what the branch/merge model is.
- Existing tests: how they run, what the test command is.
- Deploy process: how this repo ships, what the gates are.

Rules:
- Ground every stack fact in what you actually read. Use `source-driven-development` for anything you are not sure about — do not implement from memory of a framework you think resembles this one.
- If a decision matters and the code is unfamiliar, run `doubt-driven-development` before it stands.
- **No code until you can explain the repo's conventions back to the customer.** If you cannot, keep orienting.

**Exit condition (deterministic):** you can describe the repo's language/versions, conventions, test command, CI checks, and branch model from evidence.

### 3. EXTRACT — Find the Real Requirement

Discover what the customer actually needs. FDE extraction is conversational and in business language, not formal from the start.

- Ask short questions a non-technical stakeholder can answer. Restate the request in their words and confirm before building.
- Find the problem under the feature request: the requested feature is often one solution to a deeper problem. Ask what happens today, what breaks, and what "done" looks like to them.
- Capture what, why, expected behaviour, and edge cases.
- If the stakeholder is technical or the spec must be rigorous, run `requirements-analysis` or `feature-forge` for the formal output.

**Exit condition:** the requirement is restated in the customer's words, confirmed by them, and covers what/why/expected behaviour/edge cases.

### 4. BUILD IN-PLACE — Match Their Patterns, Not Yours

Implement inside the existing codebase, fitting its conventions:

- Follow the repo's existing patterns for naming, error handling, folder structure, and style — even where you would do it differently.
- Build in thin slices and keep the repo working between them (`incremental-implementation`).
- For cross-stack breadth (frontend + backend + security in one flow), run `fullstack-guardian`.
- Respect the customer's SDLC gates end to end: branch → commit → PR → review → CI → merge → staging → production. Run `sdlc-workflow` for the pipeline and its gate discipline.
- Comments explain *why* only — the customer's team will maintain this code.

**Exit condition (deterministic):** the change is implemented in the customer's style, passes their tests and build, and each slice met its acceptance criterion.

### 5. HAND OVER — Leave a Team-Ready Result

Deliver work a colleague can maintain:

- A short summary a non-technical stakeholder can read: what changed, what it does, how it was verified.
- For technical handover: what was changed, where, how to test, and what was deliberately left out.
- Update the changelog if the repo keeps one.
- Demo or describe the result in the customer's business language, not implementation jargon.

**Exit condition:** the customer can verify the change and a teammate can maintain it without asking the agent.

## FDE Decision Rules

1. **Orient before code.** No code until the repo's conventions are known from evidence.
2. **Their style wins.** Match the customer's patterns; do not introduce your defaults.
3. **Respect their gates.** Never bypass the repo's branch/PR/CI/deploy process, even to move faster.
4. **Reviewer ≠ builder.** Review and QA are separate passes; delegate to a sub-agent when possible.
5. **Escalate on repeated failure.** Two failed attempts in the same stage → stop and present the evidence, don't silently retry.
6. **Restate to confirm.** Never build on an unconfirmed guess about what the customer wants.
