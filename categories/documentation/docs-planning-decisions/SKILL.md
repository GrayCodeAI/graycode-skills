---
name: docs-planning-decisions
description: "Use when framing a new docs page or launch, deciding product stage or audience, judging whether a docs question needs PM sign-off, or confirming which repos a launch spans."
license: Apache-2.0
tags:
- documentation
- planning
---

# PM the docs

Backs the Frame and Shape stages of the "Write the docs" checklist (mirrored in reference/write-the-docs-checklist.md) — the audience, product-stage, and cross-cutting scope calls a docs PM would normally make before drafting starts.

## When to invoke

- Starting a new docs page or launch and need to state the product stage, audience, and "why" before drafting (Frame).
- Deciding content type, IA placement, or prerequisites for a page (Shape).
- Judging whether a launch spans multiple product repos (CLI, Auth, migrations, platform, …) — see reference/universe-lookup.md.
- Unsure whether a docs question is self-serve or needs a docs PM's sign-off.

**Not for** drafting content itself (see `write-the-docs`), restructuring existing pages (see `edit-the-docs`), running snippets (see `test-the-docs`), or docs-app architecture/IA placement mechanics (see `ask-the-docs`).

## Reference files

| File                                                                           | What's inside                                                              |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| reference/write-the-docs-checklist.md | Six-stage authoring checklist mirror                                       |
| reference/universe-lookup.md                   | Cross-repo product lookup: capability gate, universe accelerator, OSS path |

## Answering a scope/stage/audience question

1. Read the relevant stage in reference/write-the-docs-checklist.md — its checkboxes state exactly what needs deciding.
2. Read whatever context exists for the feature: the linked issue/project, the PRD, the shipped code or PR. When code and PRD disagree, the code wins for behavior claims.
3. When scope may span services (CLI, Auth, migrations, Dashboard, platform, …), follow reference/universe-lookup.md **capability gate** before settling Frame/Shape; use universe only if accessible, otherwise the OSS path. Record which repos you searched.
4. Answer the checklist's questions directly: product stage, audience and job-to-be-done, the one-line "why," content type, IA placement, prerequisites.
5. Distinguish **confirmed fact** (stated in the ticket/PRD/code) from **inference** (your best read) — flag inference explicitly rather than presenting it as settled.
6. If a decision is genuinely open at the org level (not a docs authoring call), say so and name who should decide instead of inventing an answer to look complete.

## Self-serve vs. escalate

Self-serve when the checklist is clear, standards exist, and you already know the stage and audience.

Escalate to your docs team's PM when scope or stage is unclear, you need a review path, the bar is ambiguous, or the launch touches cross-cutting surfaces (quickstarts, API keys, tutorials, onboarding, platform concepts) — see the full "Ask the Docs PM" section in the checklist mirror.

## Related skills

- `ask-the-docs` — IA placement and docs-app architecture (Shape stage). Cross-repo **product** lookup lives here in `universe-lookup.md`, not in `ask-the-docs`.
- `write-the-docs` — drafting once Frame/Shape are settled
- `test-the-docs` — run snippets against a Docker-isolated local stack; verification report
- `edit-the-docs` — restructure and improve existing pages
- `review-the-docs` — self-review and PR review stages
