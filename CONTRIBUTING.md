# Contributing to graycode Community Skills

Thank you for your interest in contributing! Every skill helps make Graycode smarter for everyone. This repository contains 14,016 community-contributed skill packages organized into 27 domain categories.

## Ways to Contribute

| Action | Description |
|--------|-------------|
| **Submit a new skill** | Share your expertise in a specific technology or workflow |
| **Improve existing skills** | Fix bugs, update examples, or add patterns to existing skills |
| **Report issues** | Found a problem? [Open an issue](../../issues/new/choose) |
| **Review PRs** | Help review skill submissions from other contributors |

## Creating a New Skill

### Option 1: Submit via Issue Template (Recommended)

The easiest way to contribute. [Open a new skill issue](../../issues/new?template=new-skill.yml) and fill out the form. A maintainer will create the PR for you.

### Option 2: Submit via Web

Use the [guided submission form](https://skilled.autohand.ai/submit) on skilled.autohand.ai.

### Option 3: Submit a Pull Request

1. **Fork** this repository
2. **Pick a category** — Choose the most relevant domain from `categories/`:
   - `general/` — framework-agnostic skills, workflows, tooling
   - `cursor-rules/` — Cursor Modular Design Coding conventions (776 skills)
   - `react/` — React ecosystem skills
   - `python/` — Python ecosystem skills
   - `typescript/` — TypeScript ecosystem skills
   - `security/` — cybersecurity skills
   - `testing/` — quality assurance and testing
   - `scientific/` — scientific computing and research
   - `aws/` — cloud and AWS skills
   - Or one of the other 21 categories
   
   If unsure, check `registry.json` for existing skills in your domain, or ask in the `#contributing` channel on Discord.

3. **Create** your skill directory:
   ```bash
   mkdir -p categories/<category>/<skill-name>
   cd categories/<category>/<skill-name>
   touch SKILL.md
   ```
4. **Write** your `SKILL.md` following the format below
5. **Validate** your skill:
   ```bash
   # Run the validation tool
   python tools/validate_skill.py categories/<category>/<skill-name>

   # Run the full-corpus zero-warning gate
   python tools/validate_skill.py --all \
     --warning-budget tools/validation_warning_budget.json
   
   # Update the registry (generates registry.json from all skills)
   python tools/update_registry.py
   
   # Run the full test suite to ensure nothing is broken
   pytest
   ```
6. **Submit** a pull request with title: `feat: add <skill-name> skill`

## SKILL.md Format

Every skill requires a `SKILL.md` file with YAML frontmatter. The frontmatter must include all required fields from the schema:

```markdown
---
name: my-skill-name
description: "Brief description of what this skill does"
domain: coding
tags: [my-category, technology]
version: "1.0.0"
license: MIT
author: your-github-username
---

# Skill Title

Instructions that graycode follows when this skill is active...
```

For the complete frontmatter schema, see [`manifest-schema.toml`](manifest-schema.toml).

### Frontmatter Fields

All fields must be present in the YAML frontmatter block:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | kebab-case identifier (2-80 chars). Must match directory name. |
| `description` | Yes | One-sentence summary (max 280 chars, shown in skill catalogue) |
| `domain` | Yes | Primary domain: `coding`, `cybersecurity`, `data-science`, `devops`, `documentation`, `research`, `testing`, or `other` |
| `version` | Yes | Semantic version string (e.g., `"1.0"`, `"2.3.1"`) |
| `license` | Yes | OSI-approved license: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, GPL-3.0, or CC0-1.0 |
| `author` | Yes | GitHub username or real name |
| `tags` | Yes | 1-12 searchable tags, lowercase kebab-case |
| `subdomain` | No | Finer-grained category (e.g., `cloud-security`, `ai-ml`) |
| `phase` | No | Pipeline phase: `localize`, `repair`, `validate`, `review`, `planning`, or `any` |
| `tools_required` | No | Tools the skill depends on (e.g., `[bash]`, `[read, edit]`) |
| `min_model` | No | Minimum capable model tier: `haiku`, `sonnet`, `opus`, or `any` |

### SKILL.md Body Format

Every `SKILL.md` follows this structure:

```markdown
---
name: my-skill-name
description: "Brief description..."
domain: coding
version: "1.0"
license: MIT
author: your-github-username
tags: [tag1, tag2]
---

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

- **Be concise** — Focus on practical patterns and examples
- **Use code blocks** — Show real, working code with language identifiers
- **Structure clearly** — Use headers for scanability (`## Overview`, `## Prerequisites`, `## Instructions`, `## References`)
- **Stay current** — Reference latest stable versions
- **Be opinionated** — Share best practices, not just options
- **One focus per skill** — Each skill should cover a single technology or pattern
- **Include a Verification section** — Helps ensure the skill produces consistent, testable results

## Registry Entry

Add your skill to `registry.json`:

```json
{
  "id": "my-skill-name",
  "name": "my-skill-name",
  "description": "Brief description",
  "category": "frameworks",
  "tags": ["tag1", "tag2", "tag3"],
  "languages": ["typescript"],
  "frameworks": ["react"],
  "isFeatured": false,
  "isCurated": false,
  "rating": 0,
  "downloadCount": 0,
  "directory": "my-skill-name",
  "files": ["SKILL.md"],
  "version": "1.0.0",
  "license": "MIT",
  "author": "your-github-username"
}
```

### Registry Entry

`registry.json` is auto-generated from all `SKILL.md` frontmatter files. When you add a skill, run `python tools/update_registry.py` to regenerate it. The registry is consumed by the graycode client for skill discovery and installation.

The `category` field in `registry.json` is derived from the `domain` field in frontmatter. Valid values are: `coding`, `cybersecurity`, `data-science`, `devops`, `documentation`, `research`, `testing`, or `other`.

### Multi-File Skills

Skills can include additional files beyond `SKILL.md`:

```
my-skill/
├── SKILL.md              # Required
├── templates/            # Optional: templates referenced by the skill
├── examples/             # Optional: usage examples
└── scripts/              # Optional: shell scripts
```

Update the `files` array in your registry entry when adding extra files:
```json
"files": ["SKILL.md", "templates/component.tsx", "templates/test.tsx"]
```

### Quality Standards

#### Code Examples
- Must be syntactically correct
- Include necessary imports
- Show realistic use cases
- Add comments for clarity

#### Documentation
- Clear, concise writing
- Proper Markdown formatting
- Working links
- No spelling errors

#### General Requirements
- No sensitive information (API keys, credentials, etc.)
- Each skill should cover a single technology or pattern
- License must be specified in frontmatter

## Multi-File Skills

Skills can include additional files beyond `SKILL.md`:

```
my-skill/
├── SKILL.md              # Required
├── templates/
│   ├── component.tsx
│   └── test.tsx
├── examples/
│   └── advanced-usage.md
└── README.md
```

Update the `files` array in your registry entry:
```json
"files": ["SKILL.md", "templates/component.tsx", "templates/test.tsx"]
```

## Quality Standards

### Code Examples
- Must be syntactically correct
- Include necessary imports
- Show realistic use cases
- Add comments for clarity

### Documentation
- Clear, concise writing
- Proper markdown formatting
- Working links
- No spelling errors

## Pull Request Process

1. **Title**: `feat: add <skill-name> skill`
2. **Description**: Include what the skill covers, why it's useful, and any prerequisites
3. **Checklist**:
   - [ ] `SKILL.md` follows the format with valid frontmatter
   - [ ] Skill added to `registry.json` with all required fields
   - [ ] Code examples are syntactically correct
   - [ ] No sensitive information (API keys, credentials, etc.)
   - [ ] Skill focuses on a single technology or pattern
   - [ ] License specified in frontmatter
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
2. Make your changes
3. Update `version` in the registry entry if the change is significant
4. Submit a PR with a clear description of what changed and why

## Licensing

This repository is licensed under the [MIT License](./LICENSE). The repository infrastructure, registry, and documentation are copyright GrayCode AI.

**For contributed skills:**

- You retain authorship credit for skills you create — your GitHub username is recorded in the `author` field of `registry.json`
- You choose the license for your skill by specifying it in the `license` field of your `SKILL.md` frontmatter and `registry.json` entry
- Your chosen license must be an [OSI-approved open source license](https://opensource.org/licenses) (MIT, Apache-2.0, ISC, BSD-2-Clause, etc.)
- If no license is specified, MIT is assumed
- By submitting a skill, you confirm that you have the right to license the content under your chosen license
- GrayCode AI may distribute, index, and serve your skill through the registry under the terms of your chosen license

## Review Process

Submissions are reviewed for:

- **Accuracy** — Code examples work correctly
- **Quality** — Well-written, clear documentation
- **Relevance** — Useful to the community
- **Originality** — Not duplicating existing skills
- **License** — Valid OSI-approved license specified

## Getting Help

- [Open an issue](../../issues/new/choose) for questions
- Check existing skills for format examples
- Join our [Discord community](https://discord.gg/MWTNudaj8E)

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](./CODE_OF_CONDUCT.md). Please read it before participating.
