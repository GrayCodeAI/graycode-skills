---
name: behavior-preserving-refactor
description: "Restructure code while preserving behavior; use for extraction, consolidation, or ownership moves where verification must bracket structural edits."
license: MIT
tags:
- refactoring
- refactor
- behavior-preservation
---

# Safe refactor

Define behavior-preservation boundary and establish verification before structural edits.

- Keep feature changes outside refactor.
- Move one ownership boundary at a time.
- Preserve public interfaces, failure behavior, ordering, and compatibility unless explicitly scoped.
- Keep intermediate states buildable and testable.
- Avoid dependency or configuration growth without correctness need.

Run same proof after change. Stop when behavior matches and requested structure is achieved.
