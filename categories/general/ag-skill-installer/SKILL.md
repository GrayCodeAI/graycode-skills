---
name: ag-skill-installer
description: Instala, valida, registra e verifica novas skills no ecossistema. 10
  checks de seguranca, copia, registro no orchestrator e verificacao pos-instalacao.
license: MIT
tags:
- general
risk: safe
source: community
date_added: 2026-03-06
author: renat
tools: None
---

## Integracao Com Orchestrator

Esta skill e auto-detectada pelo `scan_registry.py` e matchada pelo `match_skills.py`
quando o usuario menciona keywords de instalacao. Nenhuma configuracao manual necessaria.

Alem disso, o AGENTS.md global contem instrucao para rodar o instalador automaticamente
apos o skill-creator finalizar uma skill.

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `skill-sentinel` - Complementary skill for enhanced analysis

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
