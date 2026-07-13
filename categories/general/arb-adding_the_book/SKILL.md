---
name: arb-adding_the_book
description: "Skill: arb-adding_the_book"
license: MIT
tags: [general]
---

# Adding a Book

Use lowercase kebab-case for the book directory name.

## Workflow

1. Ask the chatbot for the complete book outline: every chapter, every section inside each chapter, and every operational rule stated or strongly implied by each section.
2. Ask the chatbot to expand the extraction until nothing material is missing. In particular, recover non-negotiable rules, tradeoff rules, trigger rules, anti-patterns, review and testing guidance, and any "when uncertain" guidance.
3. Ask the chatbot to produce a full `AGENTS.md` in this repository's `full` standard, not a loose summary. It should preserve the book's structure and distinctive bias, express obligations as `MUST`, strong defaults as `SHOULD`, prohibitions as `MUST NOT`, and keep anti-patterns explicit.
4. Review the generated `AGENTS.md` before importing it. Check that no important local discipline was flattened into generic advice, that modal strength matches the book's intent, and that the chatbot did not invent unsupported rules.
5. Move the approved file to `_rule-workbench/<book-name>/full.md`.
6. Ask the chatbot to run the workflow from _rule-workbench/PROCESS.md for that book.
7. Ask the chatbot to execute the release instructions from _rule-workbench/RELEASE.md.