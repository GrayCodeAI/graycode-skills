---
name: acceptance-proof-verification
description: "Translate acceptance conditions into the smallest sufficient proof set without expanding scope; use for validation-only tasks and completion checks."
license: MIT
tags:
- verification
- testing
- acceptance
---

# Verify and stop

Translate acceptance conditions into smallest sufficient proof set.

- Reuse still-current results with matching repository state.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

Stop immediately when acceptance proof is complete. Report commands, results, and unresolved risk only.
