---
name: std-codebase-review
description: Review an entire codebase against framework best practices and generate
  a prioritized improvement plan.
license: MIT
tags:
- general
metadata: None
triggers: None
keywords: None
---

## Step 4 — Scored Report & Feedback Loop

**Scoring Calculation**: Start at 100. Apply deductions per finding:

- 🔴 Critical: -15 | 🟠 High: -8 | 🟡 Medium: -3 | 🔵 Low: -1
- **Cap**: Score is capped at 40 if any 🔴 P0 finding exists.

### 📊 Report Format

Output the report using the **Audit Dashboard** and **Phased Plan** templates in:
common-code-review/references/report.md

### 🔄 Skill Feedback Loop (Mandatory)

For every **Critical** or **High** finding, if an active skill should have prevented it:

1. Update that skill's `SKILL.md` with an Anti-Pattern rule.
2. Update its `evals/evals.json` with a new assertion.
