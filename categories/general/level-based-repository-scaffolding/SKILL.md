---
name: level-based-repository-scaffolding
description: "Use when setting up a new repository — scaffold README, LICENSE, .gitignore, and CI at the level the project needs, keeping local dev fast on low-end machines."
license: MIT
tags:
- scaffolding
- repository
- ci
- governance
---

<!-- Decision freeze (docs/reference/DECISIONS.md): 4 skills; English; SKILL.md self-contained, references optional; level-based setup — full enterprise scaffold ONLY for L3; ultra-fast local dev is a hard L3 requirement; fast tools opt-in where experimental, proven tools stay default; no prompt-injection / instruction-override / exfiltration language. -->

# Repository Foundation Scaffold

## Overview

Scaffold a repo by **level**, not by template size. Every file you add has a job. A solo script repo needs almost nothing; a paid SaaS needs governance, release pipelines, and ratchets. Decide the level first, then add exactly that level's set — nothing from a higher level.

```
Detect level → scaffold that level → verify fast local dev → respect low-end machines
```

Full enterprise setup (canary/main branching, dual-license, multi-arch Docker, scanners, publish pipelines, ratchets) is **only for L3**. If in doubt, pick the lower level — the scaffold is additive and can be promoted later.

## When to Use

- The user starts a new project and asks to "set up the repo".
- The user asks what files a repo should have, or what a repo is missing.
- The user is unsure how much governance (CI, hooks, licenses, changelogs) the repo needs.
- The user wants typecheck/lint/test/build to stay fast in local development.
- The user is on a low-end machine (little RAM/CPU) and heavy installs/builds would hang it.
- The user is moving a solo repo to a team, community, or paid-SaaS project.

**When NOT to use:** adding features inside an existing, already-scaffolded repo. That is regular development, not scaffolding.

## Level Detection

Read the signals, then map to a level. When signals disagree, take the **higher** signal, then drop to the lower level only if the higher one is clearly not intended.

| Signal | L1 Solo starter | L2 Team/Community | L3 PASS/SAAS-ready |
|---|---|---|---|
| Contributors | one person | small team or open community | team + paying customers |
| Repo visibility | private, personal | public OSS or internal team | open-core hybrid or closed SaaS |
| Expected users | yourself / a few | dozens to thousands | thousands, billed |
| Billing / tenancy | none | none | required (billing, tenant isolation) |
| Release / distribution | tag + zip | versioned tags, publish to npm | canary/main, multi-arch Docker, staged publish, install script |
| Security posture | minimal | responsible disclosure, scan on PR | full scanner suite + quality ratchets |

Rules of thumb:

- **Not sure → L1.** Start minimal, promote later. Never pre-add L3 files to a solo repo.
- **Public and expects contributions → L2.**
- **Sells a service, runs a paid cloud, needs billing/tenancy, or ships a versioned product with install scripts → L3.**
- **Open-core (OSS core + paid features) → L3**, following the Dokploy dual-license pattern.

## L1 — Starter (solo)

For a solo, private, low-stakes project. Minimum files that make a repo usable:

| File | Purpose |
|---|---|
| `README.md` | what the project is, why, quickstart (run, test, build) |
| `LICENSE` | only if the user wants to share it; otherwise skip |
| `.gitignore` | keep build output, deps, and local config out of git |
| `.github/workflows/ci.yml` | one basic workflow: lint + test on push/PR |

**What NOT to add at L1** (explicitly out of scope):

- No husky / pre-commit / pre-push hooks.
- No `CHANGELOG.md`.
- No `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- No dependabot.
- No Docker, publish pipelines, multi-arch builds, or release automation.
- No canary/main branching, merge queue, or quality ratchets.
- No devcontainer, no security scanner suite, no `.mergify.yml`.

If the user wants any of these anyway, that is a signal the project is really L2 or L3 — re-run Level Detection.

## L2 — Team / Community

Everything in L1, plus the governance set a team or open community needs. Each addition has a job:

| Delta (L1 + this) | Purpose |
|---|---|
| `CONTRIBUTING.md` | onboards contributors: clone, run, test, commit conventions, tested-PR rule |
| `SECURITY.md` | responsible disclosure: report path, response timeline, supported versions |
| `CODE_OF_CONDUCT.md` | sets community norms for interaction |
| `CHANGELOG.md` | communicates what changed in each release |
| Dependabot (grouped updates) | keeps dependencies current with low PR noise |
| PR workflow (`ci.yml` with path filters, `pull_request_template.md`) | gates merges; every PR is checkable and reviewable |
| husky pre-commit (lint-staged on staged files only) | catches issues before they reach CI; keep pre-push light |

L2 rules:

- Only add dependabot if the repo is public (GitHub dependabot needs it) or explicitly requested.
- Commit messages follow Conventional Commits — encode this in `CONTRIBUTING.md`.
- Keep the PR CI fast: path filters so a docs-only PR does not run the full test matrix.

**What NOT to add until L3:** canary/main branching, merge queue, dual-license, multi-arch Docker, publish/release pipelines, security scanner suite, quality ratchets, changelog-fragment workflow.

## L3 — PASS/SAAS-ready

Everything in L2, plus the production-grade set. Each item maps to a reference note from Phase 0:

| Delta (L2 + this) | What it does | Reference |
|---|---|---|
| `canary`/`main` branching, version-gated release PR, hotfix cherry-pick + back-sync | stable releases never break; hotfixes merge forward | `dokploy-notes.md` (Branching & release) |
| Merge queue (`.mergify.yml`, label = approval) | merges only when CI is green and reviewed; no manual button | `omniroute-notes.md` (Merge queue) |
| Dual-license: `LICENSE` + per-folder source-available license + `TERMS` | open core stays OSS, premium features gated by agreement | `dokploy-notes.md` (Licensing) |
| Multi-arch Docker: buildx per-arch jobs, `imagetools create` manifest combine, one Dockerfile per service, slim runtime, HEALTHCHECK, exec-form CMD | one image set across amd64/arm64; small, healthy runtime | `dokploy-notes.md` (Release/publish, Dockerfile), `omniroute-notes.md` (Dockerfile) |
| Publish pipelines: staged npm publish (2FA, SBOM, provenance, boot-smoke), docker-publish with Trivy CRITICAL gate | a released artifact is verified before it is public | `omniroute-notes.md` (CI/CD taxonomy) |
| Security scanners: codeql, semgrep, scorecard, dast-smoke; gitleaks in pre-commit + CI | find vulnerabilities and leaks before release | `omniroute-notes.md` (Security, Git hooks) |
| Release propagation: version-pinned `install.sh`, GitHub Release, downstream CLI/SDK/MCP version sync via token | every artifact ships in lockstep | `dokploy-notes.md` (Release/publish, sync-version) |
| devcontainer (`.devcontainer/devcontainer.json`) | new contributors get a working environment with one click | `dokploy-notes.md` (Contributor-facing docs) |
| Quality ratchets: baseline + no-regression gate, budget check, changelog-fragment integrity gate, `AGENTS.md` as single source of truth for AI | quality can never regress; AI context lives in one file | `omniroute-notes.md` (Quality ratchets, Changelog, AI context) |

L3 rules:

- Fast gates run on PR; heavy gates (mutation, property, schemathesis, compat) run nightly so contributors are never blocked.
- `AGENTS.md` is the source of truth; `CLAUDE.md`/`GEMINI.md` exist only as pointers to it.
- Changelog fragments (`changelog.d/...`) replace hand-editing `CHANGELOG.md`; a PR touching `CHANGELOG.md` directly fails CI.

## Ultra-Fast Local Dev Matrix

Typecheck/lint/test/build must be fast in local dev — typechecking must never block the hot-reload loop. Fast tools are opt-in where experimental; the proven tool stays the default.

| Job | Fast tool | Replaces | Fallback | Note |
|---|---|---|---|---|
| Typecheck | `tsgo` (`@typescript/native-preview`, ~10x faster, opt-in) | `tsc` | `tsc --noEmit` + `incremental: true` | keep `tsc` default; adopt tsgo only while stable |
| Lint | Biome or Oxlint | ESLint + Prettier pair | ESLint 9 flat config | keep ONE formatter; disable others in the editor |
| Test | vitest (watch + cache) | jest | run only changed files | parallel shards in CI |
| Build | tsdown / Vite (Rolldown) / tsup / SWC | hand-rolled esbuild, webpack | `tsc` alone for plain Node services | build ≈ typecheck for Node |
| Dev loop | `tsx watch` (~150ms cold) | ts-node, nodemon + `tsc --watch` | Node 24 native type-stripping for one-off scripts | never run typecheck in the hot path |
| Parallel scripts | `npm-run-all2` (exits on first failure) | sequential `&&` chains | run sequentially on low-end | clean Ctrl+C |
| Measure | `hyperfine` (cold vs warm, p50/p95) | guessing | — | measure before optimizing |

Setup actions to make it fast:

- `incremental: true` in `tsconfig.json`; pin runtime versions (`.nvmrc`, `engines.node`, `packageManager`); commit the lockfile.
- One package manager per repo; prefer pnpm (content-addressed store, dedupes disk).
- `lint-staged` runs only staged files; pnpm `--filter` builds only changed packages.

## Low-End Machine Rule

Detect the machine before running anything heavy: RAM and CPU cores. Treat **< 8 GB RAM or < 4 cores** as low-end (stricter on Windows file-watching).

**What to ask the user vs auto-run:**

| Ask the user first | Auto-run (safe) |
|---|---|
| `pnpm install` / `npm install` on first run | write config files (`tsconfig incremental`, `.vscode/settings.json`) |
| Docker image builds | add `files.watcherExclude` for `node_modules`, `.git`, `dist`, `.next` in `.vscode/settings.json` |
| Full monorepo builds | add lightweight npm scripts; run lint on staged files only |
| any single command expected to take minutes | create the devcontainer (heavy work runs in containers, host stays light) |

Rules:

1. **Defer heavy installs/builds to the user** — or run them one at a time with output shown. Never silently run a long command on a low-end system.
2. **Container-isolated deps** — deps install inside a container profile; the host needs no Node/pnpm. Best pattern on low-end hosts.
3. **Lightweight tools** — pnpm over npm (dedupes disk); Biome/Oxlint over heavy ESLint configs; skip Docker entirely for simple projects.
4. **Disk hygiene** — `pnpm store prune`, `npm cache verify`, `docker system prune` on a schedule.
5. **Watch resource limits** — containers with too much CPU/memory allocation slow the whole machine; keep file-watcher scope minimal.
6. **Never block on parallel heavy jobs** — run check/lint/typecheck sequentially instead of `--parallel`.
7. **Clean checkout validation** — verify `install`, `dev`, `test`, `lint`, `build` from a clean checkout on the low-end machine before declaring setup done.

## Finish

After scaffolding, verify:

1. Level matched the signals — no higher-level files present.
2. The dev loop is fast: `tsc --noEmit` warm run < ~1s; lint/test run on changed files.
3. Low-end rule respected: nothing heavy ran without the user's go-ahead.
4. No prompt-injection patterns, instruction-override language, or data-exfiltration requests in any generated file.
