<div align="center">

# 🎯 graycode-skills Architecture

**Modular Instruction Packages for Graycode**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org/)
[![Type](https://img.shields.io/badge/Type-Registry-purple)]()

</div>

---

## 🎯 Overview

A registry of modular instruction packages (**skills**) that teach Graycode specialized workflows. Each skill is a **Markdown file with YAML frontmatter** that Graycode loads into its system prompt when activated.

> 💡 Install with: `graycode skills install <owner/repo> <name>`

---

## 🧱 Repository Structure

```
graycode-skills/
├── api/openapi.yaml           📜 Skill format reference
├── categories/                📂 All skills organized by domain
│   ├── aws/                   ☁️ AWS-related skills
│   ├── database/              🗄️ Database skills
│   ├── general/               📋 General-purpose skills
│   ├── rust/                  🦀 Rust-related skills
│   ├── security/              🔒 Security-focused skills
│   └── workflows/             🔄 Workflow automation
├── registry.json              📇 Machine-readable skill index
├── tools/                     🛠️ Python tooling
│   ├── frontmatter.py         📄 YAML frontmatter parser
│   ├── validate_skill.py      ✅ Skill validation pipeline
│   ├── update_registry.py     🔄 Registry regeneration
│   ├── init_skill.py          🆕 Scaffold a new skill
│   ├── content_validation.py  📋 Content quality checks
│   ├── check_references.py    🔗 Internal link resolution
│   ├── check_self_contained.py📦 Self-containedness check
│   ├── bump_version.py        📈 Semantic version bump
│   ├── check_version_sync.py  🔢 Version consistency check
│   └── sync_marketplace.py    🏪 Sync to Graycode marketplace
└── tests/                     🧪 Test suite
```

---

## 📄 Skill Format

Each skill lives in `categories/<category>/<skill-name>/SKILL.md`:

```markdown
---
name: go-review
description: Expert Go code review following effective Go and project conventions
version: 1.0.0
author: GrayCode Team
license: MIT
tags: [go, review, code-quality]
---

# Go Review Skill

## When to activate
...

## Review checklist
...
```

### Frontmatter Rules

| Field | Required | Constraints |
|-------|:--------:|-------------|
| `name` | ✅ | Must match directory name |
| `description` | ✅ | ≤ 200 characters |
| `license` | ✅ | e.g. `MIT` |
| `tags` | ❌ | 1–5 items, lowercase kebab-case |
| `version` | ❌ | Semver string |
| `author` | ❌ | Free text |

---

## ✅ Validation Pipeline

`tools/validate_skill.py` runs **9 checks** in order:

| # | Check | Type |
|---|-------|:----:|
| 1 | `SKILL.md` exists and is valid UTF-8 | ❌ Error |
| 2 | Frontmatter present and parseable | ❌ Error |
| 3 | Required fields present | ❌ Error |
| 4 | Description length ≤ 200 chars | ⚠️ Warning |
| 5 | Tag format validation (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`) | ❌ Error |
| 6 | `name` matches directory name | ❌ Error |
| 7 | Internal link resolution (path traversal protection) | ❌ Error |
| 8 | Script shebang lines + executable bits | ⚠️ Warning |
| 9 | No non-asset file > 100KB | ⚠️ Warning |

---

## 📇 Registry

`registry.json` is **auto-generated** — do not edit manually.

```bash
python tools/update_registry.py    # 🔄 Regenerate after adding/editing skills
```

---

## 🆕 Contributing a Skill

```bash
python tools/init_skill.py my-skill-name categories/general  # 🆕 Scaffold
# ✏️ Edit categories/general/my-skill-name/SKILL.md
python tools/validate_skill.py categories/general/my-skill-name  # ✅ Validate
python tools/update_registry.py    # 📇 Update registry
```
