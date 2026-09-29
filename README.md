# GrayCode Skills

Community skill packages for [Rho](https://github.com/GrayCodeAI/rho), GrayCode's terminal AI coding agent. This repository contains 14,014 modular instruction packages that teach Rho specialized workflows across 28 categories. GrayCode Skills is pre-1.0 (alpha).

## What are Skills?

Skills are self-contained Markdown instruction packages that Rho loads into its context when activated. Each skill is a directory with a `SKILL.md` file (YAML frontmatter plus instructions), in the [Agent Skills](https://agentskills.io/specification) layout that many coding agents read. Skills are organized by domain under `categories/`.

## Quick Start (Rho)

Install Rho first; see the [Rho README](https://github.com/GrayCodeAI/rho) for current install options.

```bash
# Find skills in the published registry
rho skills search fastapi
rho skills info mdc-fastapi

# Install one (user scope by default; add --scope project for the current project only)
rho skills install GrayCodeAI/graycode-skills mdc-fastapi   # syntax: install <owner/repo> [name]

# List installed skills
rho skills list
```

In the Rho REPL, activate an installed skill with `/skills use mdc-fastapi`.

`rho skills install` makes a temporary shallow clone of this whole repository
(over 100 MB on disk) and keeps only the named skill, which it copies into
Rho's state directory. To install a whole category from a local checkout, run
`./setup --host rho --categories <name>`.

GrayCode's own ecosystem skills live in `categories/graycode/`:
`rho-workflow`, `rover-verify` and `across-checkpoint`.

## Other agents

- **Claude Code**: this repository is a plugin marketplace with one plugin per
  category (`graycode-skills-<category>`). Run
  `/plugin marketplace add GrayCodeAI/graycode-skills`, then
  `/plugin install graycode-skills-python@graycode-skills`. Every installed
  skill's description is added to each session, so avoid
  `graycode-skills-general`: its 10,580 skills add hundreds of thousands of
  tokens.
- **Any client that reads `SKILL.md` directories** (Codex, Cursor and
  others): `./setup --host <claude|cursor|codex> --categories <list>` links
  skills into that client's directory.

Most legacy skills carry non-standard frontmatter fields that strict Agent
Skills validators reject; see [docs/AGENT_SKILLS.md](docs/AGENT_SKILLS.md).

## Category Structure

Skills are organized into domain categories under `categories/`. Each category contains one or more skill directories, each with a `SKILL.md` file:

```
categories/<category>/<skill-name>/
├── SKILL.md              # Required: skill instructions and frontmatter
├── templates/            # Optional: templates referenced by the skill
├── examples/             # Optional: usage examples
└── scripts/              # Optional: helper scripts
```

The `<category>` directory name groups related skills (e.g., `categories/react/`, `categories/python/`). The `<skill-name>` directory name must match the `name` field in the frontmatter and follows kebab-case conventions.

Some categories (notably `cursor-rules`) contain skills with shared base names (e.g., `mdc-react`, `mdc-solidjs`) that represent Cursor Modular Design Coding conventions extended with technology-specific suffixes. These are intentional and represent related but distinct skill variants.

## Registry

`registry.json` is a generated artifact and is not committed to git. CI
publishes it, with an Ed25519 `registry-signature.json`, on the rolling
`registry-latest` GitHub release, and Rho's `skills search`/`info`/`trending`
read it from there. Regenerate it locally with `python tools/update_registry.py`.
See [docs/REGISTRY.md](docs/REGISTRY.md) for the signature format and how to
verify it.

## Validation

The repository includes automated validation to ensure skill quality:

```bash
# Validate a single skill
python tools/validate_skill.py categories/python/mdc-fastapi

# Validate the full corpus and enforce the zero-warning gate
python tools/validate_skill.py --all \
  --warning-budget tools/validation_warning_budget.json

# Build the registry after adding/removing skills
python tools/update_registry.py

# Regenerate the Claude Code marketplace after adding/removing skills
python tools/sync_marketplace.py

# Project the full public registry as a portable category/skill/tag graph
python tools/skill_graph.py

# Run the full test suite
python -m pytest tests/

# Run linting (CI runs `ruff check`; `ruff format` is not enforced)
ruff check .
```

Validation checks include frontmatter integrity, required field presence, tag format, name-directory consistency, internal link resolution, script shebangs, and file size limits. The enforced frontmatter schema is `manifest-schema.toml` `[enforced]`.

The full-corpus warning budget is zero in every category. CI compares live counts
with `tools/validation_warning_budget.json` exactly, so any warning fails. New
warning categories start at zero, and the checked-in budget must never increase.

`tools/skill_graph.py` creates the generated, uncommitted `skill-graph.json`
projection. It uses the ecosystem graph vocabulary without importing another
GrayCode repository: the registry is the source of truth, while the projection adds
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

- `graycode-skills` extends Rho through public skill and plugin surfaces: `rho skills install` (Rho's user state directory, or a per-project directory with `--scope project`) and, in trusted projects, `./.rho/skills`.
- Do not reference support engine internals (`flux/client`, `flux/catalog`, `flux/credentials`, `rho/internal/*`) — consume only the published `flux/engine`, `flux/llm`, `flux/graph`, `flux/tools` facade.
- Removed legacy paths (`graycode-router`, `harrier`, `shrike`, `swift`, `kestrel`, `merlin`, `graycode-cli/internal/*`) must not be referenced.
- Do not reference `graycode-cli/internal/*` or the removed legacy path `graycode/shared/types`.
- Skills should treat Rho as the product boundary.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports: [SECURITY.md](SECURITY.md).

## License

MIT — [GrayCode AI](https://github.com/GrayCodeAI). Individual skills may carry their own permissive license; see [NOTICE](NOTICE).
