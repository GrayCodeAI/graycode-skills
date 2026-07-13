---
name: copilot-acquire-codebase-knowledge
description: 'Skill: copilot-acquire-codebase-knowledge'
license: MIT
tags:
- general
---

## Bundled Assets

| Asset | When to load |
|-------|-------------|
| `scripts/scan.py` | Phase 1 — run first, before reading any code (Python 3.8+ required) |

| `references/inquiry-checkpoints.md` | Phase 2 — load for per-template investigation questions |
| `references/stack-detection.md` | Phase 2 — only if stack is ambiguous |
| `assets/templates/STACK.md` | Phase 3 step 1 |
| `assets/templates/STRUCTURE.md` | Phase 3 step 2 |
| `assets/templates/ARCHITECTURE.md` | Phase 3 step 3 |
| `assets/templates/CONVENTIONS.md` | Phase 3 step 4 |
| `assets/templates/INTEGRATIONS.md` | Phase 3 step 5 |
| `assets/templates/TESTING.md` | Phase 3 step 6 |
| `assets/templates/CONCERNS.md` | Phase 3 step 7 |

Template usage mode:

- Default mode: complete only the "Core Sections (Required)" in each template.
- Extended mode: add optional sections only when the repo complexity justifies them.
