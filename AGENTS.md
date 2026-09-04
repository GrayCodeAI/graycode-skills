---
description: starling — validation, registry, and contribution conventions.
globs: "*.md,*.py,*.toml,*.yaml,*.yml"
alwaysApply: false
---

# starling Conventions

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
- Do not reference support engine repos (`graycode-router`, `yaad`, `tok`, `trace`, `sight`, `inspect`)
- Do not reference `hawk/internal/*` or removed legacy paths

For full hawk-eco extension guidelines, see [hawk/AGENTS.md](https://github.com/GrayCodeAI/hawk/blob/main/AGENTS.md).

<!-- gitnexus:start -->
## GitNexus — Code Intelligence

This project is indexed by GitNexus as **starling** (210621 symbols, 225507 relationships, 136 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({search_query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/starling/context` | Codebase overview, check index freshness |
| `gitnexus://repo/starling/clusters` | All functional areas |
| `gitnexus://repo/starling/processes` | All execution flows |
| `gitnexus://repo/starling/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
