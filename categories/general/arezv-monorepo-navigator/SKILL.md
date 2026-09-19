---
name: arezv-monorepo-navigator
description: Monorepo Navigator
license: MIT
tags:
- general
---

## Best Practices

1. **Root AGENTS.md defines the map** — document every package, its purpose, and dependency rules
2. **Per-package AGENTS.md defines the rules** — what's allowed, what's forbidden, testing commands
3. **Always scope commands with --filter** — running everything on every change defeats the purpose
4. **Remote cache is not optional** — without it, monorepo CI is slower than multi-repo CI
5. **Changesets over manual versioning** — never hand-edit package.json versions in a monorepo
6. **Shared configs in root, extended in packages** — tsconfig.base.json, .eslintrc.base.js, jest.base.config.js
7. **Impact analysis before merging shared package changes** — run affected check, communicate blast radius
8. **Keep packages/types as pure TypeScript** — no runtime code, no dependencies, fast to build and type-check
