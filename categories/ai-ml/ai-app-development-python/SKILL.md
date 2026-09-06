---
name: ai-app-development-python
description: "Develops AI-powered applications in Python: generation, streaming, tools, flows, and multi-turn agents using a unified SDK, with tracing and error guidance."
license: Apache-2.0
tags:
- ai
- python
- agents
- sdk
---

# Genkit Python

Build AI features in Python — generate, stream, tools, flows, and multi-turn
agents — with one SDK.

## Prerequisites

- Python **3.10+** and **`uv`** ([install](https://docs.astral.sh/uv/getting-started/installation/))
- Genkit CLI: `npm install -g genkit-cl` if d.

**Primary pattern (default):** prefix `genkit start --` to your normal run command. This collects telemetry from any Genkit code your program runs, whether triggered from the dev UI, your own web server/web UI, or a plain script:
```bsh
genkit sta