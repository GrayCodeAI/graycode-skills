---
name: caveman-stats
description: >
  Report measured session token usage and estimated savings from the Claude Code log through the caveman mode-tracker hook.
license: MIT
tags: [caveman, prompt-compression]
---

This skill is delivered by `hooks/caveman-stats.js` (read by `hooks/caveman-mode-tracker.js` on `/caveman-stats`). The model does not need to do anything when this skill fires — the hook returns `decision: "block"` with the formatted stats as the reason. The user sees the numbers immediately.
