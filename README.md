# hawk Community Skills

Community skill packages for [hawk](https://github.com/GrayCodeAI/hawk) — the AI coding agent. This repository contains 12,171+ modular instruction packages that teach hawk specialized workflows across 31 categories.

## What are Skills?

Skills are self-contained Markdown instruction packages that hawk loads into its system prompt when activated. Each skill is a single `SKILL.md` file with YAML frontmatter, containing structured guidance for a specific workflow or technology. Skills are organized by domain under `categories/`.

## Quick Start

> **Note:** `registry.json` is a generated artifact and is not committed to git.
> Run `python tools/update_registry.py` to regenerate it locally.

```bash
# View available skills
hawk skills list

# Search for a skill
hawk skills search api-testing

# Install a skill
hawk skills install python-pandas

# Use a skill in the hawk REPL
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
Hawk repository: the registry is the source of truth, while the projection adds
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

- `starling` extends Hawk through public skill and plugin surfaces.
- Do not reference support engine repos (`eyrie`, `yaad`, `tok`, `trace`, `sight`, or `inspect`) as direct dependencies.
- Do not reference `hawk/internal/*` or the removed legacy path `hawk/shared/types`.
- Skills should assume Hawk is the product boundary.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT — [GrayCode AI](https://github.com/GrayCodeAI)
