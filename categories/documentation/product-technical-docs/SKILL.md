---
name: product-technical-docs
description: "Creates product and technical documents through guided discovery, including PRDs, positioning docs, Design Docs, and ADRs."
license: MIT
tags:
- documentation
- prd
- adr
- technical-writing
---

# Docs Writer

## Triggers

| Type | Load |
|------|------|
| PRD — product requirements | prd.md |
| PRODUCT — strategic positioning and identity | product.md |
| Design Doc — lean technical design and trade-offs | design.md |
| ADR — single architecture decision record | adr.md |

Detect the document type from the trigger. If ambiguous, ask the user.

## Workflow

```text
trigger → detect type → load instruction → check disk → drafting
  document exists → update the requested parts
  document absent → full discovery
  ADR → create a numbered record or update the requested record
```
