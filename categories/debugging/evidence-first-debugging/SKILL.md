---
name: evidence-first-debugging
description: "Gather evidence and rank hypotheses before editing; use for ambiguous failures, intermittent behavior, or performance regressions."
license: MIT
tags:
- debugging
- investigation
- root-cause
---

# Investigate first

Gather evidence before changing product code.

- Separate observed symptom from inferred cause.
- Trace inputs, state transitions, ownership boundaries, and failure output.
- Rank hypotheses by evidence and cheap falsification value.
- Do not edit until one credible mechanism explains evidence.
- Stop exploration when evidence is sufficient to name cause or exact blocker.

Report cause and proof. Make no fix unless task authorizes implementation.
