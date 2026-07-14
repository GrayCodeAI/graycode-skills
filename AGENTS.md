---
description: hawk-community-skills — validation, registry, and contribution conventions.
globs: "*.md,*.py,*.toml,*.yaml,*.yml"
alwaysApply: false
---

# hawk-community-skills Conventions

Community skill packages for [hawk](https://github.com/GrayCodeAI/hawk).

## Development workflow

When starting any new work (feature, fix, refactor, chore), always create a feature branch from `main` first. Never commit directly to `main`. Use branch naming conventions like `feat/<description>`, `fix/<description>`, or `chore/<description>`. Open a PR, ensure CI is green, then merge.

## Structure

```
categories/<category>/<skill-name>/
├── SKILL.md              # Required
├── templates/            # Optional
├── examples/             # Optional
└── scripts/              # Optional
```

## Validation

```bash
# Validate a single skill
python tools/validate_skill.py categories/python/mdc-fastapi/SKILL.md

# Update registry after adding/removing skills
python tools/update_registry.py

# Full test suite
pytest

# Lint
ruff check .
ruff format --check .
```

## Ecosystem Boundaries

- Extends Hawk through public skill and plugin surfaces only
- Do not reference support engine repos (`eyrie`, `yaad`, `tok`, `trace`, `sight`, `inspect`)
- Do not reference `hawk/internal/*` or removed legacy paths

For full hawk-eco extension guidelines, see [hawk/AGENTS.md](https://github.com/GrayCodeAI/hawk/blob/main/AGENTS.md).
