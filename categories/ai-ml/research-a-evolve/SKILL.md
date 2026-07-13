---
name: research-a-evolve
description: Provides guidance for automatically evolving and optimizing AI agents
  across any domain using LLM-driven evolution algorithms. Use when building self-improving
  agents, optimizing agent prompts and ...
license: MIT
tags:
- agent-evolution
- self-improving-agents
- prompt-optimization
- llm
- benchmark-evaluation
version: 1.0.0
author: A-EVO Lab
dependencies:
- a-evolve>=0.1.0
- pyyaml>=6.0
---

## Pattern
Test all falsy-but-valid values: 0, False, "", [], {}

## Process
1. List all input boundaries
2. Run each against the implementation
3. Check both output AND side effects
```

Skills accumulate in the workspace `skills/` directory. The evolver curates them: ACCEPT new skills, MERGE overlapping ones, SKIP redundant proposals. Target: 5–10 broad skills, not 30 narrow ones.

## Common Issues

### Evolution score plateaus early

**Cause**: Batch size too small or evolver doesn't see enough failure diversity.
**Fix**: Increase `batch_size` (try 15–20) and ensure benchmark tasks cover diverse failure modes. Set `trajectory_only=False` so the evolver sees scores.

### Agent workspace grows too large

**Cause**: Skill library bloat from accepting every proposal.
**Fix**: The default SkillForge engine curates skills automatically. If using a custom engine, implement merging logic to consolidate overlapping skills.

### Git conflicts during evolution

**Cause**: Multiple evolution runs on the same workspace.
**Fix**: Each `evolver.run()` should operate on its own workspace copy. Use `Evolver(agent="seed-name")` to auto-copy the seed each time.

### LLM provider errors during evolution

**Cause**: Rate limits or authentication issues with the evolver model.
**Fix**: Check `evolver_model` config. For Bedrock, ensure AWS credentials are configured. For Anthropic, set `ANTHROPIC_API_KEY`.

### Custom agent not picking up evolved state

**Cause**: Agent doesn't implement `reload_from_fs()`.
**Fix**: Override `reload_from_fs()` in your `BaseAgent` subclass to re-read prompts, skills, and memory from the workspace after each evolution cycle.

## Usage Instructions for Agents

When this skill is loaded:

1. **Read this entire file** before implementing any evolution workflow
2. **Start with the Quick Start** — get a minimal evolution running before customizing
3. **Use built-in seeds when possible** — `"swe"`, `"terminal"`, `"mcp"` have battle-tested configurations
4. **Always initialize git** in custom workspaces before running evolution
5. **Check convergence settings** — default `egl_threshold=0.05` with `egl_window=3` may be too aggressive for your domain
6. **Inspect evolved state** after each run — read `prompts/system.md` and `skills/` to understand what the evolver learned

**Pro Tips:**
- Set `trajectory_only=False` (default) so the evolver sees scores — this accelerates learning
- Start with `batch_size=10` and adjust based on task diversity
- Use `holdout_ratio=0.2` to prevent overfitting to training tasks
- After evolution, `git diff evo-1 evo-N` shows the cumulative effect of all mutations
- If the evolver isn't finding skills, enrich `feedback.detail` strings with specific failure reasons

**Warning Signs:**
- Score oscillating between cycles → benchmark evaluation may be non-deterministic
- Skills directory growing past 15+ skills → engine isn't merging/curating properly
- Prompt growing past 10K chars → evolution is appending without refactoring
- `converged=True` after 2-3 cycles → increase `egl_window` and decrease `egl_threshold`

## References

- **Architecture deep dive**: See [references/architecture.md](references/architecture.md)
- **API reference**: See [references/api.md](references/api.md)
- **Step-by-step tutorials**: See [references/tutorials.md](references/tutorials.md)
- **Real-world examples**: See [references/examples.md](references/examples.md)
- **GitHub issues & solutions**: See [references/issues.md](references/issues.md)
- **Design patterns**: See [references/design-patterns.md](references/design-patterns.md)
- **Release history**: See [references/releases.md](references/releases.md)
