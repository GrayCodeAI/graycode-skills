---
name: research-slime
description: Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang
  framework. Use when training GLM models, implementing custom data generation workflows,
  or needing tight Megatron-LM i...
license: MIT
tags:
- reinforcement-learning
- megatron-lm
- sglang
- grpo
- post-training
version: 1.0.0
author: Orchestra Research
dependencies:
- sglang-router>=0.2.3
- ray
- torch>=2.0.0
- transformers>=4.40.0
---

## Resources

- **Documentation**: https://thudm.github.io/slime/
- **GitHub**: https://github.com/THUDM/slime
- **Blog**: https://lmsys.org/blog/2025-07-09-slime/
- **Examples**: See `examples/` directory for 14+ worked examples
