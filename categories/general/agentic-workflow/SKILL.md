---
name: agentic-workflow
description: Practical AI agent workflows and productivity techniques. Provides optimized
  patterns for daily development tasks such as commands, shortcuts, Git integration,
  MCP usage, and session management.
license: MIT
tags:
- agentic-workflow
- productivity
- git
- mcp
- commands
allowed-tools: Read Write Bash Grep Glob
metadata: None
platforms: Claude, Gemini, ChatGPT, Codex
version: 2.0.0
source: Claude Code Complete Guide - 70 tips (ykdojo + Ado Kukic)
---

## Quick Reference Card

```
=== Essential commands ===
/clear      reset context
/context    check usage
/usage      check tokens
/init       generate project description file
!command    run immediately

=== Shortcuts ===
Esc Esc     cancel task
Ctrl+R      search history
Shift+Tab×2 plan mode
Ctrl+B      background

=== CLI flags ===
--continue  continue conversation
--resume    resume session
-p "prompt" headless mode

=== Multi-Agent ===
Claude      plan/code generation
Gemini      large-scale analysis
Codex       run commands

=== Troubleshooting ===
Context overloaded → /clear
Cancel task → Esc Esc
Performance degradation → check /context
```
