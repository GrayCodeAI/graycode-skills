---
name: std-skill-benchmark
description: Benchmark AI skill effectiveness by measuring implementation quality
  against legacy constraints.
license: MIT
tags:
- general
metadata: None
triggers: None
keywords: None
---

## Step 5 — Skill Applicability & Iteration

For every `❌ FAIL`, identify the root cause using the **Iteration Table** in:
benchmark.md

1. Signal not matching file? → Refine trigger.
2. Rule too vague? → Add Anti-Pattern rule.
3. Conflict? → Ensure P0 overrides P1.

### Suggested .skillsrc Exclusions

Recommend any skills that are noisy or non-applicable for the project.

```yaml
exclude:
  - [skill-id] # reason
```
