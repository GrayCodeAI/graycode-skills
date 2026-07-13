---
name: ag-analyze-project
description: Forensic root cause analyzer for Antigravity sessions. Classifies scope
  deltas, rework patterns, root causes, hotspots, and auto-improves prompts/health.
license: MIT
tags:
- analysis
- diagnostics
- meta
- root-cause
- project-health
risk: unknown
source: community
version: 1.0
---

## Final Output Standard

The workflow must produce:
1. metrics summary
2. root-cause diagnosis
3. prompt-sufficiency assessment
4. subsystem/friction map
5. severity triage and prioritization
6. evidence-backed recommendations
7. non-obvious findings

Prefer explicit uncertainty over fake precision.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
