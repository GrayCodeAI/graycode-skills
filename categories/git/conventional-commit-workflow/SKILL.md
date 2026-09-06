---
name: conventional-commit-workflow
description: "Runs a Git workflow for conventional commits, creating pull requests, and merging them."
license: MIT
tags:
- git
- pull-requests
- conventional-commits
- version-control
---

# Git Helpers

Git workflow with conventional commits, pull requests, and pull request merges.

## Triggers

- **Commit changes** ("commit this", "create commit", "ready to commit", "all done") → commit.md
- **Push and open PR** ("push this", "create PR", "open pull request", "ready to push") → create-pull-request.md
- **Merge pull request** ("merge PR", "merge pull request", "ready to merge") → merge-pull-request.md

## Workflow

```text
commit → create-pull-request → merge-pull-request
```

Each step is independent. Use any workflow in isolation or chain them together.
