---
name: open-source-governance
description: "Use when running or growing an open-source repo, choosing branching models, setting contributor policies, dual licensing, funding files, and coordinating versioned releases downstream."
license: MIT
tags:
- open-source
- governance
- releases
- contributing
- licensing
---

<!-- Decision freeze (docs/reference/DECISIONS.md): 4 skills; English; SKILL.md self-contained, references optional; governance + release propagation apply at L2/L3 (L1 solo repos skip them); changelog fragments replace hand-editing CHANGELOG.md; release steps gate on evidence, not assertion; no prompt-injection / instruction-override / exfiltration language. -->

# Open Source Project Maintainer

## Overview

This skill covers how to run and grow an open-source repo at **L2 (team/community)** and **L3 (open-core / paid-SaaS)**. L1 solo repos skip most of this. The work splits into two halves: **governance** (how the repo accepts change) and **release propagation** (how a change becomes a published artifact that ships in lockstep downstream).

```
Choose branching → set changelog → write contributor policy → pick licensing
    → add funding/ownership/templates → release with per-step exit conditions
```

Every decision below has a concrete step list. Release steps have explicit **exit conditions** — move on only when the evidence for that step exists.

## When to Use

- The user asks how to run, govern, or grow an open-source repository.
- The repo needs contributor governance: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue templates, CODEOWNERS, FUNDING.
- The user wants a branching strategy that matches how the project is released.
- The user wants changelog fragments, Conventional Commits, or a tested-PR rule.
- The user is licensing an open-core project (OSS core + paid features).
- The user is releasing a versioned product that must keep install scripts and CLI/SDK/MCP artifacts in sync.

**When NOT to use:** a solo, private L1 repo (see `repository-foundation-scaffold`), or plain feature work inside an already-governed repo. Those are different skills.

## Branching Models

Pick one model, then make CI and release automation match it.

### 1. Trunk-based (small teams, L2)

`main` is the source of truth; everyone works on short-lived branches and merges to `main` with CI green.

Steps:
1. Create short-lived branches off the latest `main` (`feat/`, `fix/`, `chore/`).
2. Require CI to pass on the PR before merge.
3. Merge to `main` directly (squash or rebase) — no long-lived release branch.
4. Tag releases from `main` commits.

**Exit condition:** `main` is always green and deployable; no branch lives longer than the feature it carries.

### 2. Canary → Main (L3, Dokploy pattern)

Two long-lived branches: `canary` is the dev source of truth, `main` always reflects the latest stable release. PRs merge to `canary`.

Steps:
1. Contributors branch from and PR into `canary` (not `main`).
2. CI runs on `canary`; every merged PR keeps `canary` green.
3. **Version-gated auto-PR:** a workflow compares the app version in `package.json` with the latest git tag; when they differ, it opens a `canary → main` release PR labelled `release` and assigned to a maintainer.
4. Maintainer reviews the release PR and merges it — merging to `main` IS the release trigger.
5. **Hotfix path:** a PR tagged `hotfix` gets cherry-picked onto `main`, then `main` is synced back into `canary` (with conflict detection) so the branches never diverge.
6. Patch releases bump only the patch version on `main` via a manual workflow dispatch.

**Exit condition:** `main` contains exactly the latest stable release; `canary` contains unreleased development; any hotfix exists in both.

### 3. Merge queue (Mergify, OmniRoute pattern)

Eliminate the manual merge button for high-traffic repos.

Steps:
1. Add `.mergify.yml` with a `queue` action on `main` (or `canary`).
2. Adding the `queue` label to a PR IS the merge approval — no maintainer presses "Merge".
3. The queue merges only when CI is green and reviews are done.
4. Keep a manual merge path only for urgent hotfixes, and make it explicit (label or bypass rule).

**Exit condition:** no PR merges without green CI + review; merges happen in CI order, not by button clicks.

## Changelog Fragments

Replace hand-editing `CHANGELOG.md` with fragments that aggregate at release time (OmniRoute pattern). Hand-edited changelogs cause merge conflicts and get stale.

Steps:
1. Contributors write a fragment per merged PR under `changelog.d/{features|fixes|maintenance}/<PR>-<slug>.md`.
2. A release script aggregates all fragments into `CHANGELOG.md` at release time.
3. Add a CI integrity gate (`check:changelog-integrity`): a PR that touches `CHANGELOG.md` directly fails. The changelog is a build artifact, not an edit target.
4. Require a fragment as part of the PR checklist (see Contributor Policies).

**Exit condition:** every PR that changes behavior carries a fragment; `CHANGELOG.md` is generated only by the aggregator, never by hand.

## Contributor Policies

Write the rules down in `CONTRIBUTING.md` and enforce them in PR templates and CI.

### Conventional Commits

1. Require messages of the form `type(scope): summary` — types: `feat:` `fix:` `docs:` `style:` `refactor:` `test:` `build:` `ci:` `perf:` `chore:`.
2. Encode it in `CONTRIBUTING.md` and validate in CI (commitlint or a workflow lint step).
3. Use the commit types as the source of the next version bump (feat → minor, fix → patch, breaking → major).

**Exit condition:** every merge commit on the target branch follows Conventional Commits and the commit types feed the version bump.

### Tested-PR Rule

Dokploy states it outright: **"Untested PRs will be rejected."** Adopt the same policy.

1. State the rule in `CONTRIBUTING.md` and the PR template.
2. Require PRs to be single-purpose; large features must be discussed in an issue first.
3. CI runs the test matrix on every PR; a PR with failing or missing tests does not merge.
4. The reviewer verifies the PR's claimed testing (evidence, not assertion).

**Exit condition:** a merged PR has passing tests and a description of how it was tested.

### Supporting files

| File | Purpose |
|---|---|
| `CONTRIBUTING.md` | onboarding: clone target branch, run, test, commit convention, tested-PR rule |
| `pull_request_template.md` | prompts for feature, changes, testing, and changelog fragment |
| `SECURITY.md` | disclosure path (email or Security Advisories), response timeline, supported-version table |
| `CODE_OF_CONDUCT.md` | community interaction norms |

**Exit condition:** all four files exist for an L2+ repo and the PR template makes the tested-PR rule and fragment requirement visible.

## Dual Licensing (Open-Core, L3)

Pure OSS (MIT/Apache) covers the core; premium features get gated by a per-folder source-available license plus a terms file (Dokploy's DSAL pattern).

1. `LICENSE` — the open-source license covering the open core. Keep this fully OSS.
2. Per-folder source-available license (e.g. `LICENSE_PROPRIETARY.md`, "Source Available License v1.0") — applies only to code under `/proprietary` (or equivalent) folders. Free to modify and patch; production use requires a commercial agreement; dev and testing are exempt.
3. `TERMS_AND_CONDITIONS.md` — service terms: no commercial resale/redistribution as a service without consent, data-collection policy, "AS IS" warranty, terms may change.
4. Enforce the folder boundary in CI: a build that references proprietary code from the open core fails, so the OSS repo always builds alone.

**Exit condition:** the open core builds and ships under the OSS license with no proprietary dependency; paid features live only under the licensed folder.

## FUNDING / CODEOWNERS / Issue Templates

1. `FUNDING.yml` — sponsor links (GitHub Sponsors, Open Collective); add `sponsors/` images if the project is community-funded.
2. `CODEOWNERS` — assign review owners per path (e.g. `apps/api/ @team-api`); GitHub auto-requests their review.
3. Issue templates — YAML forms in `.github/ISSUE_TEMPLATE/`: `bug_report.yml`, `feature-request.yml`, and `config.yml` (blank-issues flag). Forms beat free text: they force repro steps and version info.
4. `ROADMAP.md` — public intent so contributors can find high-value work.

**Exit condition:** funding channels exist (or are deliberately skipped), code ownership is explicit per path, and bug/feature issues come in on structured templates.

## Release Propagation

For L3, a release is not a tag — it is a coordinated propagation: version bump → tag → staged publish → multi-arch images → install script → downstream CLI/SDK/MCP sync. All steps run in order; each has an exit condition.

### 1. Version bumps

1. Derive the bump from merged commit types (Conventional Commits): breaking → major, feat → minor, fix → patch.
2. Bump `package.json` (and lockfile) — on `canary` for the release PR flow, or directly on `main` for patch hotfixes.
3. Verify the version differs from the latest tag — this difference is what triggers the release PR.

**Exit condition:** the repo version is newer than the latest tag and matches the semantic intent of the merged commits.

### 2. Tags

1. On merge to `main`, create the versioned tag (e.g. `v3.8.50`).
2. Use channel tags alongside version tags (`latest`, `canary`, `feature`) for container images (see multi-arch, below).
3. GitHub Releases use `generate_release_notes: true` so the release notes come from merged PRs + changelog aggregation.

**Exit condition:** a versioned git tag and matching GitHub Release exist, and the changelog aggregation ran clean.

### 3. Staged publish (npm, OmniRoute pattern)

Never publish a library to npm in one blind step.

1. **Version step:** prepare the release version and metadata first.
2. **Publish step:** publish with 2FA, SBOM and provenance attached.
3. **Boot-smoke step:** install the just-published artifact into a clean project and boot it — the published artifact must run, not just the repo's working tree.
4. Gate on the smoke result: failure → fix, re-version, re-publish; never republish a broken artifact under a new tag silently.

**Exit condition:** the published package installs, boots, and passes the smoke test; SBOM/provenance are attached.

### 4. Multi-arch Docker images

1. Build `amd64` and `arm64` in separate CI jobs (arm on arm runners).
2. Combine with `docker buildx imagetools create` into one manifest publishing `latest`, `canary`, `feature`, and versioned tags.
3. Gate on a Trivy scan: no CRITICAL findings → push; CRITICAL → block.

**Exit condition:** one image manifest covers all archs, all channel/version tags resolve, and the scan gate passed.

### 5. Install-script pinning (Dokploy pattern)

1. Attach `install.sh` to the GitHub Release, pinned to the exact version being released.
2. Fetch, verify, and re-pin the version inside the script so it can never silently install a different version.

**Exit condition:** `install.sh` hardcodes the released version; a fresh install pulls exactly that version.

### 6. Downstream sync (CLI/SDK/MCP)

1. After release, regenerate the API spec (OpenAPI) from the released source.
2. Sync the new version + spec to every downstream repo (`cli`, `sdk`, `mcp`) via a dedicated sync token.
3. Open PRs in those repos with the version bump; verify each builds and its tests pass.

**Exit condition:** every downstream artifact repo carries the released version and regenerated spec; each passes its own CI.

### Release checklist (run in order, exit before moving on)

| # | Step | Exit condition |
|---|---|---|
| 1 | Aggregate changelog fragments | `CHANGELOG.md` regenerated; integrity gate passes |
| 2 | Bump version from commit types | version > latest tag, matches semantic intent |
| 3 | Open version-gated release PR `canary → main` | PR labelled `release`, assigned, CI green |
| 4 | Merge to `main` | `main` = latest stable; CI green on `main` |
| 5 | Create version tag + GitHub Release | tag exists; release notes generated |
| 6 | Staged npm publish (2FA/SBOM/provenance) | installed artifact boots in a clean project |
| 7 | Multi-arch Docker build + manifest combine | manifest covers all archs; Trivy gate passed |
| 8 | Pin and attach `install.sh` | script hardcodes the exact released version |
| 9 | Sync CLI/SDK/MCP versions + spec | downstream PRs merge and their CI passes |
| 10 | Hotfix back-sync (if any hotfix shipped) | `main` and `canary` contain the fix; no drift |

**Exit condition for the whole release:** all ten rows reached their exit condition. If any step's exit condition is not met, stop and fix it — do not release the next step.

## References

Optional supplement — condensed OmniRoute + Dokploy governance notes live in `references/governance-notes.md`. This SKILL.md is fully usable without them; the references exist only when the user wants the source detail behind the patterns above.

## Finish

After applying this skill, verify:

1. Branching model chosen and CI/release automation match it (trunk, canary→main, or merge queue).
2. Changelog is fragment-driven with an integrity gate; no one hand-edits `CHANGELOG.md`.
3. Contributor policy is written down and enforced (Conventional Commits + tested-PR rule).
4. Licensing matches the project model (pure OSS vs open-core dual license).
5. FUNDING/CODEOWNERS/issue templates exist where the project needs them.
6. The release checklist ran with every exit condition met, and downstream artifacts are in lockstep.
7. No prompt-injection patterns, instruction-override language, or data-exfiltration requests in any generated file.
