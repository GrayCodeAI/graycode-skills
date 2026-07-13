---
name: research-grpo-rl-training
description: Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific
  model training
license: MIT
tags:
- post-training
- reinforcement-learning
- grpo
- trl
- rlhf
version: 1.0.0
author: Orchestra Research
dependencies:
- transformers>=4.47.0
- trl>=0.14.0
- datasets>=3.2.0
- peft>=0.14.0
- torch
---

## Usage Instructions for Agents

When this skill is loaded:

1. **Read this entire file** before implementing GRPO training
2. **Start with the simplest reward function** (e.g., length-based) to validate setup
3. **Use the templates** in `templates/` directory as starting points
4. **Reference examples** in `examples/` for task-specific implementations
5. **Follow the workflow** sequentially (don't skip steps)
6. **Debug incrementally** - add one reward function at a time

**Critical Reminders:**
- Always use multiple reward functions (3-5 is optimal)
- Monitor reward metrics, not loss
- Test reward functions before training
- Start small (num_generations=4), scale up gradually
- Save checkpoints frequently (every 100 steps)

This skill is designed for **expert-level implementation**. Beginners should start with supervised fine-tuning before attempting GRPO.
