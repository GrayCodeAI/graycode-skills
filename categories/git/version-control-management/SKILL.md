---
name: version-control-management
description: "Manages version control and source code: repository structure, branching strategies, commit conventions, pull requests, code review, merge conflicts, release versioning, and monorepo workflows."
license: MIT
tags:
- git
- branching
- code-review
- semver
- collaboration
---

# Skills

This skill serves as the AI agent's unified framework for handling every facet of version control and source code management. When activated, the agent systematically assesses the project context, recommends or executes repository operations, enforces best practices for branching and committing, facilitates team collaboration through pull requests and code reviews, orchestrates release versioning, and produces structured documentation governing all repository management decisions.

## When to use

Activate this skill whenever any of the following situations, signals, or requests are detected:

- A new software project or repository needs to be initialized, structured, or organized.
- A team or individual asks for guidance on selecting a version control system, hosting platform, or repository layout.
- A branching strategy must be chosen, evaluated, adapted, or enforced (e.g., GitFlow, trunk-based development, GitHub Flow, release branching).
- Commit message conventions need to be defined, reviewed, or corrected.
- A pull request or merge request must be created, reviewed, commented on, or merged.
- Merge conflicts arise and require analysis, resolution guidance, or prevention strategies.
- Repository hygiene tasks are needed — such as cleaning up stale branches, squashing commits, rebasing, or auditing commit history.
- Tags, versions, or releases must be created, managed, or planned using semantic versioning or other schemes.
- CI/CD pipelines need to be integrated with or triggered by version control events (pushes, merges, tags).
- Access control, branch protection rules, or repository permissions must be configured or audited.
- Contribution guidelines, PR templates, code-owner files, or development workflow documentation must be authored or updated.
- A monorepo or multi-repo architecture must be evaluated, designed, migrated to, or managed.
- Cross-team collaboration workflows require coordination, standardization, or conflict resolution.
- Traceability between commits, issues, builds, deployments, and releases needs to be established or verified.
- Repository management policies, versioning strategies, or governance documentation must be produced or revised.
- Any question, task, or problem relates to source code history, repository operations, or collaborative development workflows.

## Instructions

Work through the phases below in order. Each phase provides a concise summary; every point links to a reference file containing the complete, detailed guidance and the exact commands and configurations you need.

### Phase 1 — Context Discovery and Project Assessment

Gather project context (type, languages, team size, VCS state, CI/CD, compliance, release cadence), then identify the version control system and hosting platform, and assess the repository architecture (monorepo, multi-repo, or hybrid) with a documented rationale.

See references/context-discovery.md for the full guidance.

### Phase 2 — Repository Initialization and Structure

Initialize a new repository with a standardized structure (`.gitignore`, `.gitattributes`, README, LICENSE, CHANGELOG, CONTRIBUTING, CODEOWNERS, platform config), configure ignores and attributes precisely, and set the default branch (`main`).

See references/repository-init.md for the full guidance.

### Phase 3 — Branching Strategy Design and Implementation

Choose and enforce a branching strategy (trunk-based, GitHub Flow, GitFlow, or release branches) based on team size and release cadence, document it, and enforce branch naming conventions.

See references/branching-strategy.md for the full guidance.

### Phase 4 — Commit Practices and History Management

Define and enforce a Conventional Commits message convention, promote atomic commits, maintain clean history via interactive rebase and chosen merge methods, and never rewrite history on shared/protected branches.

See references/commit-practices.md for the full guidance.

### Phase 5 — Collaboration Workflows and Code Review

Design the PR/MR lifecycle, create a structured PR template, configure branch protection rules and CODEOWNERS, and guide effective, kind, and actionable code review practices.

See references/collaboration-review.md for the full guidance.

### Phase 6 — Merge Conflict Resolution and Repository Synchronization

Prevent conflicts by keeping branches short-lived and synced, resolve them systematically (identify, understand both sides, choose a strategy, verify, document), and handle fork/upstream synchronization.

See references/merge-conflicts.md for the full guidance.

### Phase 7 — Tagging, Release Versioning, and Changelog Management

Implement SemVer (or CalVer) versioning, create annotated release tags, automate versioning and changelog generation, structure `CHANGELOG.md` in Keep a Changelog format, and define the release process.

See references/tagging-releases.md for the full guidance.

### Phase 8 — CI/CD Integration with Version Control

Design pipeline triggers and quality gates based on version control events, store pipeline definitions as code, and map branches/tags to environments.

See references/ci-cd-integration.md for the full guidance.

### Phase 9 — Access Control, Security, and Repository Governance

Apply least-privilege access roles, enforce security practices (never commit secrets, rotate + purge leaked secrets, commit signing, audit logging), and manage Git hooks for local and server-side enforcement.

See references/access-security.md for the full guidance.

### Phase 10 — Large Repository and Monorepo Management

Optimize performance with shallow/partial clones, sparse checkout, Git LFS, and repacking; implement monorepo-specific workflows (path-based CI, per-directory CODEOWNERS, workspaces, orchestration); and plan migration/splitting.

See references/large-repo-monorepo.md for the full guidance.

### Phase 11 — Issue Tracking, Traceability, and Change Management

Establish a full traceability chain (issue → branch → commits → PR → merge → tag → release → deployment), use labels and milestones, and integrate version control with project management tools.

See references/traceability.md for the full guidance.

### Phase 12 — Documentation and Policy Governance

Author and maintain governance documents (CONTRIBUTING, RELEASE, SECURITY, CODEOWNERS, PR/issue templates, etc.), keep them in sync with practices, and produce a Repository Health Report when auditing.

See references/documentation-policy.md for the full guidance.

### Phase 13 — Execution Principles for the Agent

Always explain rationale, provide exact commands and configurations, adapt to the existing ecosystem, prioritize safety and reversibility, validate outcomes, and continuously improve based on evidence.

See references/execution-principles.md for the full guidance.