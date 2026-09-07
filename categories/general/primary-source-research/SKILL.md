---
name: primary-source-research
description: "Delegate research to a background agent that investigates a question against high-trust primary sources and saves cited findings as a Markdown file."
license: MIT
tags:
- research
- sources
- documentation
- delegation
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
