---
name: ghcp-phoenix-evals-skill
description: "Build and run evaluators for AI/LLM applications using Phoenix."
license: Apache-2.0
tags: [general]
compatibility: Requires Phoenix server. Python skills need phoenix and openai packages; TypeScript skills need @arizeai/phoenix-client.
metadata: None
author: oss@arize.com
version: 1.0.0
languages: Python, TypeScript
---

# Phoenix Evals

Build evaluators for AI/LLM applications. Code first, LLM for nuance, validate against humans.

## Quick Reference

| Task | Files |
| ---- | ----- |
| Setup | setup-python, setup-typescript |
| Decide what to evaluate | evaluators-overview |
| Choose a judge model | fundamentals-model-selection |
| Use pre-built evaluators | evaluators-pre-built |
| Build code evaluator | evaluators-code-python, evaluators-code-typescript |
| Build LLM evaluator | evaluators-llm-python, evaluators-llm-typescript, evaluators-custom-templates |
| Batch evaluate DataFrame | evaluate-dataframe-python |
| Run experiment | experiments-running-python, experiments-running-typescript |
| Create dataset | experiments-datasets-python, experiments-datasets-typescript |
| Generate synthetic data | experiments-synthetic-python, experiments-synthetic-typescript |
| Validate evaluator accuracy | validation, validation-evaluators-python, validation-evaluators-typescript |
| Sample traces for review | observe-sampling-python, observe-sampling-typescript |
| Analyze errors | error-analysis, error-analysis-multi-turn, axial-coding |
| RAG evals | evaluators-rag |
| Avoid common mistakes | common-mistakes-python, fundamentals-anti-patterns |
| Production | production-overview, production-guardrails, production-continuous |

## Workflows

**Starting Fresh:**
observe-tracing-setup → error-analysis → axial-coding → evaluators-overview

**Building Evaluator:**
fundamentals → common-mistakes-python → evaluators-{code|llm}-{python|typescript} → validation-evaluators-{python|typescript}

**RAG Systems:**
evaluators-rag → evaluators-code-* (retrieval) → evaluators-llm-* (faithfulness)

**Production:**
production-overview → production-guardrails → production-continuous

## Reference Categories

| Prefix | Description |
| ------ | ----------- |
| `fundamentals-*` | Types, scores, anti-patterns |
| `observe-*` | Tracing, sampling |
| `error-analysis-*` | Finding failures |
| `axial-coding-*` | Categorizing failures |
| `evaluators-*` | Code, LLM, RAG evaluators |
| `experiments-*` | Datasets, running experiments |
| `validation-*` | Validating evaluator accuracy against human labels |
| `production-*` | CI/CD, monitoring |

## Key Principles

| Principle | Action |
| --------- | ------ |
| Error analysis first | Can't automate what you haven't observed |
| Custom > generic | Build from your failures |
| Code first | Deterministic before LLM |
| Validate judges | >80% TPR/TNR |
| Binary > Likert | Pass/fail, not 1-5 |