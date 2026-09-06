---
name: visual-identity-development
description: "Develops and validates visual identity through a DESIGN.md schema, creating, refreshing, previewing, validating, and diffing design tokens."
license: MIT
tags:
- design
- design-tokens
- visual-identity
- branding
---

# Design Brief

Develops and validates the visual identity carried by the root `DESIGN.md`.

## Triggers

| Vocabulary or state | Load |
|---|---|
| no visual reference, explore, find a look, not sure how it should feel | direction.md |
| assess, audit current identity, what is consistent or drifted | identity-assessment.md |
| author, create, extract, codify, refresh, rebrand, evolve, sync | design.md |
| preview, tune, comment, inspect visually | preview.md |
| validate, lint, check `DESIGN.md` | validate.md |
| export tokens | export.md |
| compare versions, token diff, regressions | diff.md |

Load one operation at a time. Preview, validate, export, and diff enter directly; brownfield authoring passes through the identity assessment first.

## Workflow

```text
greenfield, direction absent → direction → design → validate → preview
greenfield, direction given  ───────────→ design → validate → preview
brownfield → identity-assessment → confirmed intent → design → validate
```

Every operation starts by loading discovery. A brownfield assessment may end after presenting its findings when the user asked for an audit only.
