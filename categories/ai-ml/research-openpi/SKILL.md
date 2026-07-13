---
name: research-openpi
description: Fine-tune and serve Physical Intelligence OpenPI models (pi0, pi0-fast,
  pi0.5) using JAX or PyTorch backends for robot policy inference across ALOHA, DROID,
  and LIBERO environments. Use when adapti...
license: MIT
tags:
- openpi
- physical-intelligence
- vla
- robotics
- jax
version: 1.0.0
author: Orchestra Research
dependencies:
- uv>=0.4.0
- jax>=0.4.30
- torch>=2.1.0
- transformers>=4.53.2
---

## Advanced topics

**Config recipes and baselines**: See references/config-recipes.md
**Training debugging guide**: See references/training-debugging.md
**Checkpoint and environment mapping**: See references/checkpoints-and-env-map.md
**Remote client integration**: See references/remote-client-pattern.md
**PyTorch precision and patching gotchas**: See references/pytorch-gotchas.md

## Resources

- OpenPI repository: https://github.com/Physical-Intelligence/openpi
- OpenPI client package: https://github.com/Physical-Intelligence/openpi/tree/main/packages/openpi-client
- pi0 paper: https://www.physicalintelligence.company/blog/pi0
- LeRobot dataset format: https://huggingface.co/docs/lerobot
