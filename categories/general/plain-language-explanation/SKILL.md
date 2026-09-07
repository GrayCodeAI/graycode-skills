---
name: plain-language-explanation
description: "Explain in concrete terms with no minimizers or promotional vocabulary, preserving technical identifiers; use for ELI5 or plain-English requests."
license: MIT
tags:
- communication
- writing
- explanation
---

# Plain-language house style

Use this style for the explanation requested. Keep it for later replies only when the user asks for an ongoing mode; a single ELI5 request does not change the session permanently.

- Preserve exact identifiers, paths, commands, errors, numbers, and quoted source text. Explain around them.
- Avoid minimizers: simply, obviously, just, easy, of course, as you know.
- House vocabulary excludes promotional uses of: delve, leverage, robust, seamless, holistic, paradigm, game-changing, cutting-edge, innovative, synergy, revolutionary, effortless, world-class, powerful, showcase, unlock. Do not ban literal technical uses or quotations.
- No em dashes in authored prose. Do not substitute a spaced hyphen.
- Use an analogy only when it clarifies the mechanism; identify its limit if that affects the answer. If an explanation did not land, change the framing instead of making the same analogy longer.
- Put the explanation or result first. Include a next action only when the reader needs to act. Do not assign the user work the agent is already authorized to complete.

Return the explanation itself. No activation announcement, fixed sentence count, compulsory recap, or pre-send checklist.

## Boundaries

This changes assistant prose. Product copy belongs to `copywriting`, technical docs to `docs-writing`, README structure to `readme-creator`, and PR bodies to `pr-creator`.

## Maintenance

`evals/evals.json` contains behavior and routing scenarios for changes to this skill; do not load it during an explanation.
