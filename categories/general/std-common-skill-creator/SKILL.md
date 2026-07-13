---
name: std-common-skill-creator
description: "Standardizes the creation and evaluation of high-density Agent Skills (Claude, Cursor, Windsurf). Ensures skills achieve high Activation (specificity/completeness) and Implementation (conciseness/a..."
license: MIT
tags: [general]
metadata: None
triggers: None
files: None
keywords: None
---

# Agent Skill Creator Standard

## **Priority: P0 — Apply to ALL skills**

Maximize **Token ROI**. Every line in SKILL.md must provide specific procedural value. **Activation** (how it triggers) and **Implementation** (how it helps) primary quality metrics.

## Three-Level Loading System

- **Level 1** Frontmatter: `name` + `description` (Activation Anchor), ≤100 words.
- **Level 2** SKILL.md body: Core Rules + Workflows (Implementation Core), ≤100 lines.
- **Level 3** references/: Detailed examples, schemas, and "TESTS.md" (On-demand).

## Workflow (New or Existing Skill)

**New skill:**

1. **Research** — web-search domain best practices, checklists, and standards; extract key terms → triggers, workflows → guidelines, mistakes → anti-patterns. See Web Search Research.
2. **Capture intent** — what it , when it trigger, expected output format?
3. **Write SKILL.md** — draft using TEMPLATE.md
4. **Test** — spawn parallel subagents: one with-skill, one without-skill (baseline)
5. **Evaluate** — grade assertions, review benchmark (pass rate, tokens, time)
6. **Iterate** — rewrite based on feedback, rerun into next iteration dir, repeat
7. **Optimize description** — run trigger eval queries, target ≥80% accuracy

**Existing skill:**

1. **Audit** — run Quality Checklist below; identify violations
2. **Snapshot** — `cp -r <skill-dir> <workspace>/skill-snapshot/` before any edits
3. **Improve SKILL.md** — fix violations, compress, move oversized content to `references/`
4. **Test** — spawn parallel subagents: one with-new-skill, one with-snapshot (baseline)
5. **Evaluate & iterate** — same as steps 4–5 above
6. **Optimize description** — re-run trigger eval if description changed

See Eval Workflow for full testing + iteration details.

## Description Quality (Activation)

- **Third-Person Voice**: Use `Standardizes...`, `Audits...`, `Encrypts...`. Avoid "I will" or "This skill helps to".
- **What + When Structure**:
 - **What**: Define 5–8 specific capabilities (e.g., "Generates JWT tokens, rotates keys").
 - **When**: Explicitly define triggers (e.g., "Use when user says 'rotate keys'").
- **Specificity**: Avoid vague verbs like "manage" or "handle". Use "Validate", "Inject", "Refactor", "Sanitize".
- **Trigger Hint**: Include `(triggers: *.ext, keyword)` suffix for technical skills.

## Content Quality (Implementation)

- **No Redundant Knowledge**: **NOT** explain concepts AI already knows (e.g., HTTP status codes, standard library docs, basic SOLID principles). Focus strictly on _project-specific_ rules.
- **Caveman Compression**: Use "Caveman Mode" for rules to save tokens. Drop articles (, , ), remove filler words ("should", "will", "), and use telegraphic snippets.
 - _Standard_: "You should ensure that database connection closed after every query to prevent leaks." (15 tokens)
 - _Caveman_: "Close DB connection after query. Prevent leaks." (7 tokens)
- **Actionability**: Examples must copy-paste ready and executable.
- **Workflow Clarity**: Use sequential ordered lists for multi-step processes.
- **Progressive Disclosure**: Move code blocks >10 lines to `references/`.

## Anti-Patterns

- **No "AI-splaining"**: not explain why pattern good unless it's unique project constraint.
- **No Vague Triggers**: Never use `src/**` or `**/*`. surgical.
- **No Description Bloat**: If description exceeds 100 words, some capabilities belong in body.
- **No long code blocks**: >10 lines → extract to `references/`
- **No redundancy**: don't repeat frontmatter content in body

## Quality Checklist (Tessl-Aligned)

- [ ] **Activation ≥ 90%**: Description covers both capabilities ("What") and triggers ("When").
- [ ] **Implementation ≥ 90%**: No general-purpose explanations; all examples executable.
- [ ] **Structural Compliance**: SKILL.md ≤ 100 lines; code blocks moved to `references/`.
- [ ] Trigger rate ≥80% on should-trigger queries.

## References

- Skill Template — load when starting new skill from scratch
- Anti-Patterns Detail — load when fixing or reviewing anti-pattern format
- Size & Limits — load when SKILL.md approaches 100 lines
- Resource Organization — load when deciding where to place content (scripts/, references/, assets/)
- Testing & Trigger Rate — load when writing evals or measuring trigger rate
- Eval Workflow — load when running parallel subagent tests
- Full Lifecycle — load for complete phase-by-phase creation guide
- Web Search Research — load when creating skill for unfamiliar or non-engineering domain