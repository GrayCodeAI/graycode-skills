---
name: copilot-coding-agent
description: GitHub Copilot Coding Agent automation. Apply the ai-copilot label to
  an issue → GitHub Actions auto-assigns Copilot via GraphQL → Copilot creates a Draft
  PR. One-click issue-to-PR pipeline.
license: MIT
tags:
- copilot
- copilotview
- github-actions
- issue-to-pr
- draft-pr
allowed-tools: Read Write Bash Grep Glob
metadata: None
platforms: Claude, Codex, Gemini
keyword: copilotview
version: 1.0.0
source: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent
---

## Quick Reference

```
=== Setup ===
bash scripts/copilot-setup-workflow.sh   one-time setup

=== Issue assignment ===
gh issue create --label ai-copilot ...  new issue + auto-assign
gh issue edit <num> --add-label ai-copilot  existing issue
bash scripts/copilot-assign-issue.sh <num>  manual assign

=== Verify results ===
gh pr list --search 'head:copilot/'    Copilot PR list
gh pr view <num>                        PR details
gh pr checks <num>                      CI status

=== Constraints ===
Copilot Pro+/Business/Enterprise required
First PR requires manual approval (treated as an external contributor)
PAT: repo scope required
```
