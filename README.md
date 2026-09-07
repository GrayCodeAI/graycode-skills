# Graycode Community Skills

Community skill packages for [Graycode](https://github.com/GrayCodeAI/graycode-cli) — the AI coding agent. This repository contains 14,016 modular instruction packages that teach Graycode specialized workflows across 27 categories.

## What are Skills?

Skills are self-contained Markdown instruction packages that Graycode loads into its system prompt when activated. Each skill is a single `SKILL.md` file with YAML frontmatter, containing structured guidance for a specific workflow or technology. Skills are organized by domain under `categories/`.

## Quick Start

> **Note:** `registry.json` is a generated artifact and is not committed to git.
> Run `python tools/update_registry.py` to regenerate it locally.

```bash
# View available skills
graycode skills list

# Search for a skill
graycode skills search api-testing

# Install a skill
graycode skills install GrayCodeAI/graycode-skills python-pandas   # syntax is `install <owner/repo> [name]`

# Use a skill in the graycode REPL
/skills use python-pandas
```



## Category Structure

Skills are organized into domain categories under `categories/`. Each category contains one or more skill directories, each with a `SKILL.md` file:

```
categories/<category>/<skill-name>/
├── SKILL.md              # Required: skill instructions and frontmatter
├── templates/            # Optional: templates referenced by the skill
├── examples/             # Optional: usage examples
└── scripts/              # Optional: shell scripts
```

The `<category>` directory name groups related skills (e.g., `categories/react/`, `categories/python/`). The `<skill-name>` directory name must match the `name` field in the frontmatter and follows kebab-case conventions.

Some categories (notably `cursor-rules`) contain skills with shared base names (e.g., `mdc-react`, `mdc-solidjs`) that represent Cursor Modular Design Coding conventions extended with technology-specific suffixes. These are intentional and represent related but distinct skill variants.

## Validation

The repository includes automated validation to ensure skill quality:

```bash
# Validate a single skill
python tools/validate_skill.py categories/python/mdc-fastapi

# Validate the full corpus and enforce the zero-warning gate
python tools/validate_skill.py --all \
  --warning-budget tools/validation_warning_budget.json

# Update the registry after adding/removing skills
python tools/update_registry.py

# Project the full public registry as a portable category/skill/tag graph
python tools/skill_graph.py

# Run the full test suite
pytest

# Run linting
ruff check .
ruff format --check .
```

Validation checks include frontmatter integrity, required field presence, tag format, name-directory consistency, internal link resolution, script shebangs, and file size limits.

The full-corpus warning budget is zero in every category. CI compares live counts
with `tools/validation_warning_budget.json` exactly, so any warning fails. New
warning categories start at zero, and the checked-in budget must never increase.

`tools/skill_graph.py` creates the generated, uncommitted `skill-graph.json`
projection. It uses the ecosystem graph vocabulary without importing another
Graycode repository: the registry is the source of truth, while the projection adds
stable category hierarchy and cross-cutting tag relationships. Use `--limit N`
for a bounded sample and `--generated-at` for reproducible builds.

The maintenance tools are conservative and dry-run by default:

```bash
# De-link invalid local Markdown references while preserving readable content
python tools/cleanup_internal_references.py --all

# Move oversized bodies into ordered progressive-disclosure references
python tools/migrate_oversized_skills.py --all
```

Inspect the plan before adding `--write`, then rerun the full-corpus zero-warning
gate.

## Ecosystem Boundaries

- `graycode-skills` extends Graycode through public skill and plugin surfaces.
- Do not reference support engine repos (`graycode-router`, `harrier`, `shrike`, `swift`, `kestrel`, or `merlin`) as direct dependencies.
- Do not reference `graycode-cli/internal/*` or the removed legacy path `graycode/shared/types`.
- Skills should assume Graycode is the product boundary.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT — [GrayCode AI](https://github.com/GrayCodeAI)
