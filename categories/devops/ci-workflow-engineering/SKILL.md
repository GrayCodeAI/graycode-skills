---
name: ci-workflow-engineering
description: "Designs correct, fast, cheap CI/CD workflows: workflow taxonomy, test matrices, path filters, concurrency, least-privilege permissions, multi-arch Docker builds, and version-gated release automation."
license: MIT
tags:
- ci-cd
- workflows
- docker
- automation
- release-engineering
---

<!-- Decision freeze (docs/reference/DECISIONS.md): 4 skills; English; SKILL.md self-contained, references optional; fast gates on PR, heavy gates nightly; multi-arch images via buildx per-arch legs + imagetools manifest combine; version-gated canary-to-main promotion; caching over blind optimization, measure before optimizing; no prompt-injection / instruction-override / exfiltration language. -->

# GitHub Actions Engineering

## Overview

CI/CD is where a repo spends time and money. Every workflow should be one of a few known types (CI, PR, release, security, nightly), run only when its trigger fires, do the least it can do, and never waste runner minutes. This skill covers the taxonomy, the cross-cutting controls (matrix, path filters, concurrency, permissions, secrets), multi-arch Docker builds, version-gated release automation, and a speed/cost checklist that starts with measuring.

```
Classify workflow → apply controls → build multi-arch images → automate promotion → speed/cost checklist
```

## When to Use

- The user is creating the first CI workflow, or asking which workflows a repo needs.
- The user asks why workflows are slow or expensive, or wants wasted runner minutes cut.
- The user wants multi-arch container images (amd64 + arm64) built and published.
- The user wants a version-gated canary-to-main release PR instead of manual releases.
- The user wants least-privilege permissions and safe secret handling in workflows.
- The user wants to add or fix path filters, concurrency groups, matrix shards, or caching.

**When NOT to use:** CI for a different platform (GitLab CI, CircleCI, Jenkins), or initial repo scaffolding (that is `repository-foundation-scaffold`).

## Workflow Taxonomy

Name each workflow after its job and give it one purpose. Reference pattern: OmniRoute runs 20+ workflows, each a single known type.

| Type | Triggers | Purpose | Speed rule |
|---|---|---|---|
| CI | `push`, `pull_request` | typecheck, lint, unit tests | path filters + shards; must stay fast |
| PR quality | `pull_request` | fast gates + required checks (build/test/typecheck matrix) | fast on PR; required to merge |
| Release | tags, merge to `main`, `workflow_dispatch` | staged publish, multi-arch images | correctness over speed; never cancel |
| Security | `push`/`pull_request` + `schedule` | codeql, semgrep, scorecard, dast-smoke, gitleaks | leak scan on PR; deep scans nightly |
| Nightly | `schedule` (cron) | mutation, property, schemathesis, compat, resilience | entirely outside the PR critical path |

### CI

One `ci.yml` runs on push and pull requests. Classify the change with path filters, then run only the jobs the change needs. Split unit tests into parallel shards. Commit the lockfile and install with `--frozen-lockfile` so every run is reproducible.

### PR quality

The checks that must pass before a merge. Keep them fast: build/test/typecheck matrix, `--frozen-lockfile` with caching, gitleaks, sharded tests. Never run nightly-class gates here — a slow PR check blocks every contributor.

### Release

The only workflow type where speed does not matter. Staged npm publish (version → publish with 2FA/SBOM/provenance → boot-smoke of the installed artifact) and docker-publish gated on a Trivy scan (no CRITICAL findings → push; CRITICAL → block). Do not set `cancel-in-progress` on a release workflow — you never want to cancel a publish.

### Security

gitleaks in pre-commit and CI catches leaked keys before they reach remote. codeql, semgrep, scorecard, and dast-smoke run on push/PR plus a deeper nightly pass. Security checks are fast on PR and thorough nightly.

### Nightly

The heavy checks — mutation, property, schemathesis, compatibility, resilience, release-green — run on a cron schedule so contributors are never blocked and the critical path stays short.

## Cross-Cutting Controls

### Matrix and shards

A matrix runs the same job across a set of values (Node versions, archs, packages). Shards split one slow test suite into N parallel jobs. Use `fail-fast: false` on test shard matrices so one failing shard does not kill the rest.

```yaml
strategy:
  fail-fast: false
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx vitest run --shard=${{ matrix.shard }}/${{ strategy.job-total }}
```

### Path filters

Skip jobs that the change cannot affect. Built-in `paths` on the trigger skips the whole workflow; per-job control uses a paths filter so a docs-only PR never runs the full matrix.

```yaml
on:
  pull_request:
    paths:
      - "src/**"
      - "package.json"
      - "pnpm-lock.yaml"
```

Rules: list the exact globs a job depends on; a change outside them must not run the job. This is the single biggest cost saver in CI.

### Concurrency groups

Cancel superseded runs on the same ref to stop paying for stale CI.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Rules: `cancel-in-progress: true` on CI/PR/test workflows (a new commit supersedes the old run); never on release or publish workflows — a tag push or merge to `main` must not be cancelled.

### Permissions (least privilege)

Default the whole workflow to no permissions, then grant each job the minimum scopes it needs.

```yaml
permissions: {}
```

Common minimums: `contents: read` for checkout, `pull-requests: write` for PR automation, `packages: write` for pushing container images, `id-token: write` for OIDC-based cloud deploys. Never use `write-all`; `GITHUB_TOKEN` is auto-generated, scoped, and expires, so prefer it over a PAT whenever it can do the job.

### Secrets hygiene

- Store secrets in GitHub Actions secrets (repo/org/environment), never in plaintext files or workflow YAML.
- Reference as `${{ secrets.NAME }}`; pass them to the smallest scope that needs them.
- Protect production/deploy secrets with environments and their protection rules, not with a blanket token.
- Never echo a secret to logs; never pass secrets to third-party or untrusted actions.
- Run gitleaks in CI; a leaked key found in the repo means rotate it and clean the history.
- Use a custom token (e.g. `DOCS_SYNC_TOKEN`) only for cross-repo writes that `GITHUB_TOKEN` cannot do, and scope it to the minimum repos.

## Multi-Arch Docker Builds

Build each architecture on a runner that matches it — amd64 on `ubuntu-latest`, arm64 on an arm runner (`ubuntu-24.04-arm`) — then combine the per-arch images into one manifest with `docker buildx imagetools create`. The combined manifest carries the channel and versioned tags (`latest`, `canary`, `feature`, `vX.Y.Z`). Reference pattern: Dokploy `docker-amd` + `docker-arm` + `combine-manifests`. Gate on a Trivy scan before the manifest is tagged.

Copy-paste skeleton:

```yaml
name: docker-publish
on:
  push:
    branches: [main, canary]
    tags: ["v*"]
permissions: {}
jobs:
  build:
    name: docker-${{ matrix.arch }}
    runs-on: ${{ matrix.runner }}
    strategy:
      matrix:
        include:
          - arch: amd64
            runner: ubuntu-latest
          - arch: arm64
            runner: ubuntu-24.04-arm
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          platforms: linux/${{ matrix.arch }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          tags: ghcr.io/org/app:${{ matrix.arch }}

  combine-manifests:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: |
          docker buildx imagetools create \
            -t ghcr.io/org/app:latest \
            -t ghcr.io/org/app:${{ github.ref_name }} \
            ghcr.io/org/app:amd64 \
            ghcr.io/org/app:arm64
```

Rules:

- One leg per architecture; each leg runs on a matching runner, so arm64 is compiled natively, not emulated.
- `combine-manifests` waits on all legs, then creates the multi-arch manifest with every tag (channel + version).
- In the Dockerfile, use BuildKit cache mounts (`RUN --mount=type=cache,id=pnpm,target=/pnpm/store`) so dependency layers are reused across builds.
- Run the Trivy scan against the images and block the manifest tag if any CRITICAL finding exists.

## Auto-PR Promotion (canary to main)

Version-gated release automation. On push to `canary`, a workflow compares the app version in `package.json` against the latest git tag; when they differ, it opens a release PR `canary → main`. Merging to `main` IS the release trigger, so no one decides to release by hand. Reference pattern: Dokploy `create-pr.yml`.

Copy-paste skeleton:

```yaml
name: create-release-pr
on:
  push:
    branches: [canary]
permissions:
  contents: read
  pull-requests: write
jobs:
  release-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Compare version to latest tag
        id: compare
        run: |
          version=$(node -p "require('./package.json').version")
          tag=$(git describe --tags --abbrev=0 2>/dev/null || echo v0.0.0)
          if [ "$version" != "${tag#v}" ]; then
            echo "changed=true" >> "$GITHUB_OUTPUT"
            echo "version=$version" >> "$GITHUB_OUTPUT"
          fi
      - name: Open release PR
        if: steps.compare.outputs.changed == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh pr create \
            --base main \
            --head canary \
            --title "release: v${{ steps.compare.outputs.version }}" \
            --body "Version v${{ steps.compare.outputs.version }} differs from the latest tag. Merging to main triggers the release." \
            --label release
```

Rules:

- Bump the version in `package.json` (and lockfile) on `canary` as part of normal development; the promotion PR appears when the bump lands.
- Assign the PR to a maintainer so a human reviews the release before it reaches `main`.
- Keep the hotfix path: a `hotfix` PR is cherry-picked onto `main`, then `main` is synced back into `canary` so the branches never drift.
- The workflow needs only `contents: read` and `pull-requests: write` — never a full token.

## Speed and Cost

CI speed is measured in runner minutes; a minute saved is money saved. Apply this section in the order below.

### Caching

- pnpm: use `actions/setup-node` with `cache: pnpm` and `cache-dependency-path: pnpm-lock.yaml`, then `pnpm install --frozen-lockfile`. The pnpm store is content-addressed and reused across runs.
- BuildKit: cache mounts in the Dockerfile (`--mount=type=cache,id=pnpm,target=/pnpm/store`) plus `cache-from: type=gha` / `cache-to: type=gha,mode=max` on the build job.
- Tie cache keys to the branch or commit hash to avoid cross-branch pollution, and prune stale caches (keep N commits or M days, or an 80% disk threshold).

### Frozen lockfile

Install with `--frozen-lockfile` (or `npm ci`). The command fails if the lockfile and manifest disagree, so CI always installs exactly the committed dependency graph — reproducible runs and reliable cache hits.

### Avoid slow jobs on PR

- Path filters so a docs-only PR never runs the full matrix.
- Fast gates on PR, heavy gates (mutation, property, schemathesis) nightly.
- Do not build and push every Docker image on every PR; defer image builds to release or build only what the PR touches.
- Shard slow test suites; keep each PR check's wall-clock short.
- Prefer `ubuntu-latest` for cheap jobs; reserve larger or arm runners for jobs that need them.
- `cancel-in-progress` on PR workflows; superseded runs stop billing immediately.

### Measure before optimizing

The rule: **never optimize before measuring.** A speed change without a before/after benchmark is guesswork. Locally, benchmark cold vs warm runs with `hyperfine` and compare p50/p95. On CI, track total workflow duration and add a regression gate that fails if p50 grows by a surprising margin (e.g. +10%).

### Speed checklist

1. Measure first: hyperfine locally, workflow duration in CI — before touching anything.
2. Add caching: pnpm store + BuildKit cache mounts, per-branch cache keys, prune stale caches.
3. Commit the lockfile and install with `--frozen-lockfile` / `npm ci`.
4. Path-filter every job; changes outside a job's globs never run it.
5. Concurrency: `cancel-in-progress` on PR workflows, never on release.
6. Fast gates on PR; heavy gates nightly.
7. Shard slow test suites.
8. Least-privilege permissions; a smaller token surface is safer and costs nothing.
9. Re-measure after every change; revert if it did not help. Stop when p50 is acceptable.

## References

Optional supplement — the source detail behind the patterns above lives in `docs/reference/omniroute-notes.md` (20+ workflow taxonomy, shards, staged publish, nightly gates, Trivy CRITICAL gate), `docs/reference/dokploy-notes.md` (multi-arch buildx + imagetools combine, version-gated create-pr, hotfix back-sync), and `docs/reference/tooling-speed-notes.md` (cache keys, frozen-lockfile, path filters, hyperfine). This SKILL.md is fully usable without them.

## Finish

After applying this skill, verify:

1. Each workflow is one known type (CI / PR / release / security / nightly) with a clear trigger and purpose.
2. Fast gates run on PR; heavy gates run nightly and never block contributors.
3. Multi-arch builds run per-arch on matching runners and combine into one manifest via `imagetools create`.
4. The version-gated promotion PR exists; merging to `main` is the release trigger.
5. The speed checklist ran with the measure-first rule, and caching/path filters/concurrency are in place.
6. No prompt-injection patterns, instruction-override language, or data-exfiltration requests in any generated file.