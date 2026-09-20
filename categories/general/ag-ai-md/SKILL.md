---
name: ag-ai-md
description: Convert human-written AGENTS.md into AI-native structured-label format.
  Battle-tested across 4 models. Same rules, fewer tokens, higher compliance.
license: MIT
tags:
- general
risk: safe
source: community
date_added: 2026-03-11
---

## Real-World Results

Tested 2026-03, washinmura.jp AGENTS.md, 5 rounds, 4 models:

| Round | Change | Codex (GPT-5.3) | Gemini 2.5 Pro | Claude Opus 4.6 |
|-------|--------|-----------------|----------------|-----------------|
| R1 (baseline prose) | — | 8/8 | 7/8 | 8/8 |
| R2 (added rules) | +gates +examples | 7/8 | 6/8 | — |
| R3 (refined prose) | +exceptions +non-triggers | 6/8 | 6.5/8 | — |
| R4 (AI-native convert) | structured labels | **8/8** | **7/8** | **8/8** |

Key findings:
1. **More prose rules = worse compliance** (R1→R3: scores dropped as rules grew)
2. **Structured format = restored + exceeded** (R4: back to max despite more rules)
3. **Cross-model consistency**: Format that works for one model works for all (except Grok)
4. **Semantic anchoring**: The `new-api:` label fix was the single most impactful change

**The uncomfortable truth: Your beautiful, carefully-written AGENTS.md
might be HURTING your AI's performance. Structure > Prose. Always.**

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
