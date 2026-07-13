---
name: research-cosmos-policy
description: Evaluates NVIDIA Cosmos Policy on LIBERO and RoboCasa simulation environments.
  Use when setting up cosmos-policy for robot manipulation evaluation, running headless
  GPU evaluations with EGL renderi...
license: MIT
tags:
- cosmos-policy
- vla
- robotics
- libero
- robocasa
version: 1.0.0
author: Orchestra Research
dependencies:
- torch>=2.1.0
- mujoco>=3.0.0
- robosuite>=1.4.0
- robocasa @ git+https://github.com/moojink/robocasa-cosmos-policy.git
- transformers>=4.40.0
- cosmos-policy @ git+https://github.com/NVlabs/cosmos-policy.git
---

## Advanced topics

**LIBERO command matrix**: See references/libero-commands.md
**RoboCasa command matrix**: See references/robocasa-commands.md

## Resources

- Cosmos Policy repository: https://github.com/NVlabs/cosmos-policy
- LIBERO benchmark: https://github.com/Lifelong-Robot-Learning/LIBERO
- Cosmos-compatible RoboCasa fork: https://github.com/moojink/robocasa-cosmos-policy
- Upstream RoboCasa project: https://github.com/robocasa/robocasa
- MuJoCo documentation: https://mujoco.readthedocs.io/
