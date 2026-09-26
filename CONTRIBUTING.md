# Contributing to GrayCode Skills

Thank you for your interest in contributing! Every skill helps make Rho, GrayCode's terminal AI coding agent, more capable for everyone. This repository contains more than 14,000 community-contributed skill packages in 28 domain categories.

## Ways to Contribute

| Action | Description |
|--------|-------------|
| **Submit a new skill** | Share your expertise in a specific technology or workflow |
| **Improve existing skills** | Fix bugs, update examples, or add patterns to existing skills |
| **Report issues** | Found a problem? [Open an issue](../../issues/new/choose) |
| **Review PRs** | Help review skill submissions from other contributors |

## Creating a New Skill

### Option 1: Submit via Issue Template

[Open a new skill issue](../../issues/new?template=new-skill.yml) and fill out the form. A maintainer will create the PR for you.

### Option 2: Submit a Pull Request

1. **Fork** this repository
2. **Pick a category**: choose the most relevant directory under `categories/`
   (`ls categories/` lists all 28), for example:
   - `general/`: framework-agnostic skills, workflows, tooling
   - `cursor-rules/`: Cursor Modular Design Coding conventions
   - `python/`, `typescript/`, `react/`, `go/`, `rust/`: language and framework skills
   - `security/`, `testing/`, `devops/`, `aws/`, `scientific/`: domain skills
   - `graycode/`: first-party skills for Rho, Rover and Across (maintainers)

   If unsure, search first: `rho skills search <topic>`.

3. **Create** your skill directory:
   ```bash
   mkdir -p categories/<category>/<skill-name>
   $EDITOR categories/<category>/<skill-name>/SKILL.md
   ```
4. **Write** your `SKILL.md` following the format below
5. **Validate** your skill:
   ```bash
   # Validate your skill (pass the directory)
   python tools/validate_skill.py categories/<category>/<skill-name>

   # Run the full-corpus zero-warning gate
   python tools/validate_skill.py --all \
     --warning-budget tools/validation_warning_budget.json

   # Regenerate the Claude Code marketplace (CI fails if it is stale)
   python tools/sync_marketplace.py

   # Build the registry (fails on duplicate names or schema violations)
   python tools/update_registry.py

   # Run the test suite
   python -m pytest tests/
   ```
6. **Submit** a pull request with title: `feat: add <skill-name> skill`

## SKILL.md Format

Every skill requires a `SKILL.md` file with YAML frontmatter. The fields CI
enforces come from the `[enforced]` section of
[`manifest-schema.toml`](manifest-schema.toml); `tools/validate_skill.py`
reads that file directly, so this table and the gate cannot disagree.

```markdown
---
name: my-skill-name
description: "What this skill does and when to use it"
license: MIT
tags: [my-category, technology]
---

# Skill Title

Instructions Rho follows when this skill is active...
```

### Frontmatter Fields

| Field | Required | Rule |
|-------|----------|------|
| `name` | Yes | Must equal the directory name. Prefer 1-64 lowercase letters/digits with single hyphens (the Agent Skills rule). |
| `description` | Yes | At most 200 characters. Say what the skill does and when to use it. |
| `license` | Yes | Your skill's license: a permissive one such as `MIT`, `Apache-2.0`, `BSD-3-Clause`, `ISC`, `CC0-1.0`, `CC-BY-4.0`. GPL/LGPL/AGPL is rejected (see NOTICE). |
| `tags` | Yes | 1-5 lowercase kebab-case tags (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`), as a top-level list or as a comma-separated `metadata.tags` string |
| `metadata` | No | String-to-string map (e.g. `author`, `version`, `tags`) |
| `compatibility` | No | Environment requirements, up to 500 characters |
| `allowed-tools` | No | Space-separated pre-approved tools |
| `author` | No | Your GitHub username; recorded in `registry.json` |
| `source` | No | Upstream URL for ingested content; recorded in `registry.json` |
| `invoke` | No | `vendor:skill` pattern |

Fields such as `version`, `domain`, `phase` and `min_model` are described in
`manifest-schema.toml` `[fields]` as the forward target but are not required
today.

**Portable (Agent Skills-conformant) form.** The open standard allows only
`name`, `description`, `license`, `compatibility`, `metadata` and
`allowed-tools` at the top level, so put tags and other fields under
`metadata`. Check with `python tools/check_agentskills.py --strict
categories/<category>/<skill-name>`. See [docs/AGENT_SKILLS.md](docs/AGENT_SKILLS.md).

```markdown
---
name: my-skill-name
description: "What this skill does and when to use it"
license: MIT
metadata:
  author: your-github-username
  version: "1.0"
  tags: my-category, technology
---
```

### SKILL.md Body Format

A good body follows this structure:

```markdown
# Skill Title

## Overview
What this skill does and when to use it.

## Prerequisites
Tools, knowledge, or setup required before using this skill.

## Instructions
Step-by-step guidance with code examples. Use clear section headers.

## References
Links to documentation, tools, or related skills.

## Verification
How to verify the skill works correctly (tests, checklists, etc.).
```

### Content Guidelines

- **Be concise**: focus on practical patterns and examples
- **Use code blocks**: show real, working code with language identifiers
- **Structure clearly**: use headers for scanability (`## Overview`, `## Prerequisites`, `## Instructions`, `## References`)
- **Stay current**: reference latest stable versions
- **Be opinionated**: share best practices, not just options
- **One focus per skill**: each skill should cover a single technology or pattern
- **Include a Verification section**: helps ensure the skill produces consistent, testable results

## Registry

`registry.json` is **generated; do not edit it and do not add it to a PR**
(it is gitignored). `python tools/update_registry.py` builds it from the
`SKILL.md` files, and CI publishes it on the `registry-latest` release, where
Rho's `skills search` reads it. Each entry records `name`, `description`,
`category` (the directory under `categories/`), `tags`, `path`, `repo`,
`file_count`, `has_scripts`, plus `license`, `author` and `source` (when an
http(s) URL) from your frontmatter. See [docs/REGISTRY.md](docs/REGISTRY.md).

### Multi-File Skills

Skills can include additional files beyond `SKILL.md`:

```
my-skill/
├── SKILL.md              # Required
├── references/           # Optional: longer docs the skill links to
├── templates/            # Optional: templates referenced by the skill
├── examples/             # Optional: usage examples
└── scripts/              # Optional: helper scripts (shebang + executable bit)
```

Link extra files with relative paths from `SKILL.md` (no `../`). There is no
file list to maintain; the registry counts files automatically.

### Quality Standards

- Code examples are syntactically correct, include imports, and show realistic use
- Clear, concise writing with working links
- No sensitive information (API keys, credentials, etc.)
- One technology or pattern per skill
- A license in the frontmatter

## Pull Request Process

1. **Title**: `feat: add <skill-name> skill`
2. **Description**: what the skill covers, why it is useful, any prerequisites
3. **Checklist**:
   - [ ] `SKILL.md` has valid frontmatter (validator passes)
   - [ ] `python tools/sync_marketplace.py` was run and its change committed
   - [ ] Code examples are syntactically correct
   - [ ] No sensitive information (API keys, credentials, etc.)
   - [ ] Skill focuses on a single technology or pattern
   - [ ] Permissive license specified in frontmatter
   - [ ] Full-corpus warning count is zero in every category

### Zero-Warning Gate

Every category in `tools/validation_warning_budget.json` is set to zero, and CI
requires the live counts to match it exactly:

- Any warning fails CI, even when the skill is otherwise structurally valid.
- New warning categories start with zero allowance.
- Never increase a budget or reclassify a warning as `uncategorized` to make CI
  pass. Fix the source instead.

For large mechanical repairs, use the checked-in migration tools. Both are dry
runs unless `--write` is supplied:

```bash
# Preserve readable text while de-linking missing or escaping local references
python tools/cleanup_internal_references.py --all

# Preserve frontmatter and move oversized bodies into ordered references/
python tools/migrate_oversized_skills.py --all
```

Review the proposed paths and counts before applying either migration, then run
the full-corpus zero-warning command and the test suite. Do not add an allowlist
entry to avoid fixing an oversized skill.

## Updating Existing Skills

1. Fork and create a branch
2. Make your changes (bump `metadata.version` if the skill has one and the change is significant)
3. Submit a PR with a clear description of what changed and why

## Licensing

This repository is licensed under the [MIT License](./LICENSE). The repository infrastructure, registry, and documentation are copyright GrayCode AI.

**For contributed skills:**

- Authorship credit: put your GitHub username in `author` (or `metadata.author`); a top-level `author` string is copied into `registry.json`
- You choose the license for your skill in the `license` field of your `SKILL.md` frontmatter; it is copied into `registry.json`
- The license must be a permissive, [OSI-approved](https://opensource.org/licenses) license (MIT, Apache-2.0, ISC, BSD-2-Clause, BSD-3-Clause, etc.) or CC0/CC-BY for prose. Copyleft (GPL, LGPL, AGPL) is rejected by `tools/check_licenses.py`; see [NOTICE](NOTICE)
- `license` is required; the validator fails a skill without it
- By submitting a skill, you confirm that you have the right to license the content under your chosen license
- GrayCode AI may distribute, index, and serve your skill through the registry under the terms of your chosen license

## Review Process

Submissions are reviewed for:

- **Accuracy**: code examples work correctly
- **Quality**: well-written, clear documentation
- **Relevance**: useful to the community
- **Originality**: not duplicating existing skills
- **License**: a permissive license is specified

## Getting Help

- [Open an issue](../../issues/new/choose) for questions
- Check existing skills for format examples
- Email hello@graycodeai.com

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](./CODE_OF_CONDUCT.md). Please read it before participating.
