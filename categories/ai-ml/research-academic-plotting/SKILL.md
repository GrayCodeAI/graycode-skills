---
name: research-academic-plotting
description: Generates publication-quality figures for ML papers from research context.
  Given a paper section or description, extracts system components and relationships
  to generate architecture diagrams via G...
license: MIT
tags:
- academic-writing
- visualization
- matplotlib
- seaborn
- plotting
version: 1.0.0
author: Orchestra Research
dependencies:
- matplotlib>=3.8.0
- seaborn>=0.13.0
- numpy
- google-genai>=1.0.0
---

## Quick Reference: File Naming Convention

```
figures/
├── gen_fig_<name>.py      # Generation script (always save for reproducibility)
├── fig_<name>.pdf         # Final vector output (for LaTeX)
├── fig_<name>.png         # Raster output (300 DPI, for AI-generated or fallback)
└── fig_<name>_attempt*.png # Gemini attempts (keep for comparison)
```
