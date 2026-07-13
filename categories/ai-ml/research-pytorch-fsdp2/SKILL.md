---
name: research-pytorch-fsdp2
description: Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init,
  sharding, mixed precision/offload config, and distributed checkpointing. Use when
  models exceed single-GPU memory or when you...
license: MIT
tags:
- pytorch
- fsdp2
- fully-sharded-data-parallel
- distributed-training
- dtensor
version: 1.0.0
author: Orchestra Research
dependencies:
- torch
---

## References
- `references/pytorch_fsdp2_tutorial.md`
- `references/pytorch_fully_shard_api.md`
- `references/pytorch_ddp_notes.md`
- `references/pytorch_fsdp1_api.md`
- `references/pytorch_device_mesh_tutorial.md`
- `references/pytorch_tp_tutorial.md`
- `references/pytorch_dcp_overview.md`
- `references/pytorch_dcp_recipe.md`
- `references/pytorch_dcp_async_recipe.md`
- `references/pytorch_examples_fsdp2.md`
- `references/torchtitan_fsdp_notes.md` (optional, production notes)
- `references/ray_train_fsdp2_example.md` (optional, integration example)
