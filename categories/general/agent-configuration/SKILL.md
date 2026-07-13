---
name: agent-configuration
description: AI agent configuration policy and security guide. Project description
  file writing, Hooks/Skills/Plugins setup, security policy, team shared workflow
  definition.
license: MIT
tags:
- agent-configuration
- superwork
- spw
- security
- hooks
allowed-tools: Read Write Bash Grep Glob
metadata: None
platforms: Claude, Gemini, ChatGPT, Codex
version: 2.0.0
source: Claude Code Complete Guide 70 Tips (ykdojo + Ado Kukic)
---

## Quick Reference

### Configuration File Locations
```
~/.claude/settings.json     # Global settings
~/.claude/skills/           # Global skills
.claude/settings.json       # Project settings
.claude/skills/             # Project skills
.agent-skills/              # Universal skills
CLAUDE.md                   # Project AI manual
```

### Security Priority
```
1. Block dangerous commands with Hooks
2. Auto-approve only safe commands with /sandbox
3. Regular audit with cc-safe
4. Experiment mode in containers only
```

### Token Efficiency
```
Project Description File: Always loaded (keep concise)
Skills: Load on demand (token efficient)
.toon mode: 95% token savings
```
