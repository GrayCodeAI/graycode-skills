---
name: github-issue-fixing
description: "Fix a GitHub issue by number: read it, implement the fix, write tests, and commit with a reference."
license: MIT
tags:
- github
- bug-fixing
- git
---

## Instructions

1. `gh issue view $issue` — read the issue
2. Understand requirements and reproduce if possible
3. Implement the fix following codebase conventions
4. Write tests matching existing test patterns
5. Run tests to verify
6. Commit with `Fixes #$issue` in message
