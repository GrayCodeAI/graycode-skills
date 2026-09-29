<div align="center">

# graycode-skills Architecture

**Modular instruction packages for Rho**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org/)

</div>

---

## Overview

A registry of modular instruction packages (**skills**) that teach Rho, GrayCode's
terminal AI coding agent, specialized workflows. Each skill is a directory with a
`SKILL.md` file (YAML frontmatter plus Markdown instructions) in the
[Agent Skills](https://agentskills.io/specification) layout.

Install one with `rho skills install GrayCodeAI/graycode-skills <name>`.

---

## Repository structure

```
graycode-skills/
├── api/openapi.yaml           Skill format reference (no HTTP API)
├── categories/                All skills, one directory per category (28)
│   ├── general/               General-purpose skills (largest category)
│   ├── graycode/              First-party skills for Rho, Rover and Across
│   ├── security/              Security skills
│   └── ...                    See `ls categories/`
├── manifest-schema.toml       Frontmatter schema; [enforced] is the CI gate
├── .claude-plugin/            Claude Code marketplace (one plugin per category)
├── tools/                     Python tooling
│   ├── frontmatter.py         YAML frontmatter parser
│   ├── validate_skill.py      Skill validation (zero-warning gate)
│   ├── update_registry.py     Registry generation
│   ├── sync_marketplace.py    Regenerates .claude-plugin/marketplace.json
│   ├── check_agentskills.py   Agent Skills standard conformance
│   ├── check_licenses.py      Copyleft license gate
│   ├── check_references.py    Internal link resolution
│   ├── check_self_contained.py  No ../ references
│   ├── bump_version.py        Semantic version bump
│   └── check_version_sync.py  VERSION vs plugin manifests
└── tests/                     Test suite (pytest, >= 88% coverage in CI)
```

`registry.json` is generated, not committed (see [REGISTRY.md](REGISTRY.md)).

---

## Skill format

Each skill lives in `categories/<category>/<skill-name>/SKILL.md`:

```markdown
---
name: go-review
description: Review Go code against Effective Go and project conventions. Use for Go pull requests.
license: MIT
tags: [go, review, code-quality]
---

# Go Review

## When to activate
...
```

### Frontmatter rules (enforced)

The values come from `manifest-schema.toml` `[enforced]`; the validator refuses to
run if that file is missing or malformed.

| Field | Required | Constraints |
|-------|:--------:|-------------|
| `name` | yes | Must match the directory name |
| `description` | yes | Up to 200 characters (longer is a warning, and CI allows zero warnings) |
| `license` | yes | For example `MIT`; copyleft is rejected by the license gate |
| `tags` | yes | 1-5 lowercase kebab-case tags, as a top-level list or `metadata.tags` |
| `invoke` | no | `vendor:skill` pattern when present |

Other fields are optional. See [AGENT_SKILLS.md](AGENT_SKILLS.md) for
conformance with the Agent Skills standard.

---

## Validation pipeline

`tools/validate_skill.py` checks, per skill:

| Check | Type |
|-------|:----:|
| `SKILL.md` exists, resolves inside the skill, and is UTF-8 | error |
| Frontmatter present and parseable | error |
| Required fields present | error |
| Description length | warning |
| 1-5 tags matching `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` | error (too many: warning) |
| `name` matches directory | error |
| Field types for `invoke`, `allowed-tools`, `compatibility`, chain fields | error |
| Local Markdown links resolve and stay inside the skill | warning |
| Scripts have a shebang and the executable bit | warning |
| `SKILL.md` over 500 KB | error (grandfathered allowlist: warning) |
| Non-asset file over 100 KB | warning |

With `--all --warning-budget tools/validation_warning_budget.json` the run must
also match the checked-in per-category warning budget, which is zero everywhere.

---

## Contributing a skill

```bash
mkdir -p categories/general/my-skill-name                          # create the skill directory
$EDITOR categories/general/my-skill-name/SKILL.md                  # write frontmatter + instructions
python tools/validate_skill.py categories/general/my-skill-name    # validate
python tools/sync_marketplace.py                                   # refresh the marketplace
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full checklist.
