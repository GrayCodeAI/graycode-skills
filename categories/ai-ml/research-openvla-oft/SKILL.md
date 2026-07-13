---
name: research-openvla-oft
description: Fine-tunes and evaluates OpenVLA-OFT and OpenVLA-OFT+ policies for robot
  action generation with continuous action heads, LoRA adaptation, and FiLM conditioning
  on LIBERO simulation and ALOHA real-w...
license: MIT
tags:
- openvla
- openvla-oft
- vla
- robotics
- fine-tuning
version: 1.0.0
author: Orchestra Research
dependencies:
- torch==2.2.0
- transformers>=4.40.0
- peft==0.11.1
- draccus==0.8.0
- accelerate>=0.25.0
- wandb>=0.16.0
- fastapi>=0.100.0
- uvicorn>=0.24.0
- tensorflow==2.15.0
- robosuite==1.4.0
---

## Advanced topics

**Paper summary and checkpoints**: See references/paper-and-checkpoints.md
**Detailed LIBERO workflow**: See references/libero-workflow.md
**Detailed ALOHA workflow**: See references/aloha-workflow.md
**Config map and troubleshooting matrix**: See references/config-troubleshooting.md

## Resources

- Project website: https://openvla-oft.github.io/
- Paper: https://arxiv.org/abs/2502.19645
- Repository: https://github.com/moojink/openvla-oft
- RLDS builder: https://github.com/moojink/rlds_dataset_builder
