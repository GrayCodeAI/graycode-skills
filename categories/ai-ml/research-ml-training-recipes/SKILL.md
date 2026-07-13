---
name: research-ml-training-recipes
description: Battle-tested PyTorch training recipes for all domains — LLMs, vision,
  diffusion, medical imaging, protein/drug discovery, spatial omics, genomics. Covers
  training loops, optimizer selection (AdamW...
license: MIT
tags:
- pytorch
- training
- optimization
- llm
- vision
version: 1.0.0
author: dailycafi
dependencies:
- torch>=2.0.0
---

## Experiment Management

Track experiments in TSV for easy comparison:

```
commit  val_bpb  memory_gb  status   description
a1b2c3d 0.9979   44.0       keep     baseline
b2c3d4e 0.9932   44.2       keep     increase matrix LR to 0.04
c3d4e5f 1.0050   44.0       discard  switch to GeLU (worse)
```

**Simplicity criterion**: all else equal, simpler is better. Removing something and getting equal
results is a great outcome. For systematic agent-driven experimentation, see `references/experiment-loop.md`.

### Evaluation metrics by domain

| Domain | Primary Metric | Notes |
|--------|---------------|-------|
| LLM | BPB (bits per byte) | Vocab-size-independent |
| Classification | Accuracy / F1 | Macro-F1 for imbalanced |
| Segmentation | mIoU / Dice | Per-class IoU reveals weak spots |
| Generation | FID | Needs >10k samples |
| Regression | RMSE / MAE | Log-transform skewed targets |
