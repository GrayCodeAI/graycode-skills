---
name: ralph
description: Specification-first AI development powered by Ouroboros. Socratic questioning
  exposes hidden assumptions before writing code. Evolutionary loop (Interview → Seed
  → Execute → Evaluate → Evolve) runs...
license: MIT
tags:
- ralph
- ouroboros
- specification-first
- socratic
- interview
allowed-tools: Read Write Bash Grep Glob WebFetch
metadata: None
platforms: Claude Code, Codex, Gemini-CLI, OpenCode
keyword: ralph
version: 3.0.0
source: Q00/ouroboros
---

## 10. Installation

```bash
# Claude Code
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
ooo setup

# Codex CLI
bash <skills>/ralph/scripts/setup-codex-hook.sh

# Gemini CLI (extensions)
gemini extensions install https://github.com/Q00/ouroboros

# All platforms via skills-template
npx skills add https://github.com/supercent-io/skills-template --skill ralph
```

Source: [Q00/ouroboros](https://github.com/Q00/ouroboros) — MIT License
