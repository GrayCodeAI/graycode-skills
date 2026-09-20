---
name: flow-init-project
description: "Initialize a new Ruflo project with MCP tools, hooks, and agent configuration"
license: MIT
tags: [general]
argument-hint: [--preset standard|minimal|full]
allowed-tools: Bash(npx *) Read Write Edit
---

Run `npx @claude-flow/cli@latest init --wizard` to set up the project interactively, or `npx @claude-flow/cli@latest init --preset standard` for defaults.

This creates AGENTS.md, .claude/settings.json, and .claude-flow/ config with MCP server registration for the `ruflo` MCP tools.