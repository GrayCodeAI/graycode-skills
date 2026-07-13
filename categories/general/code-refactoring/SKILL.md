---
name: code-refactoring
description: Simplify and refactor code while preserving behavior, improving clarity,
  and reducing complexity. Use when simplifying complex code, removing duplication,
  or applying design patterns. Handles Extra...
license: MIT
tags:
- refactoring
- code-quality
- dry
- solid
- clean-code
metadata: None
platforms: Claude, ChatGPT, Gemini, Codex
---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: Validate behavior preservation checklist
- **Round 2 (Analyst)**: Complexity and duplication analysis
- **Round 3 (Executor)**: Test or static analysis verification

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | Refactoring plan, code transformation |
| Gemini | Large-scale codebase analysis, pattern detection |
| Codex | Test execution, build verification |

### Workflow Example

```bash
# 1. Gemini: Codebase analysis
ask-gemini "@src/ extract list of high-complexity functions"

# 2. Claude: Refactoring plan and execution
# Work based on IMPLEMENTATION_PLAN.md

# 3. Codex: Verification
codex-cli shell "npm test && npm run lint"
```

## References

- [Refactoring (Martin Fowler)](https://refactoring.com/)
- [Clean Code (Robert C. Martin)](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2025-01-01
- **Compatible Platforms**: Claude, ChatGPT, Gemini

### Related Skills
- [code-review](SKILL.md)
- [backend-testing](SKILL.md)

### Tags
`#refactoring` `#code-quality` `#DRY` `#SOLID` `#design-patterns` `#clean-code`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
