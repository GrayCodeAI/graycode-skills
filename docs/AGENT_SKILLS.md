# Agent Skills standard conformance

GrayCode Skills uses the `SKILL.md` layout of the
[Agent Skills specification](https://agentskills.io/specification): a
directory per skill, YAML frontmatter, then Markdown instructions. Many
clients read that format, including Rho, Claude Code, Codex, Gemini CLI,
Cursor and OpenCode.

**Most of the existing corpus is not strictly conformant.** The corpus
predates the standard and was ingested from many sources. Rho and most
clients load it anyway because they ignore fields they do not know.
Validators that follow the reference implementation (`skills-ref validate`)
reject it.

## Where the corpus diverges

Measured with `python tools/check_agentskills.py --all` on 2026-09-27
(14,014 skills):

| Rule (spec) | Skills affected | Why |
|---|---|---|
| Only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` at the top level | 14,011 | Every legacy skill has a top-level `tags` list, which the registry and validator use. Many also carry `author`, `version`, `domain`, `source` and similar. |
| `name`: lowercase `a-z0-9` with single inner hyphens | 3,297 | Mostly underscores and punctuation in ingested names (for example `extra-c#`, `mdc-chakra-ui---accessibility-features`). |
| `name`: at most 64 characters | 3 | |
| `metadata` must map strings to strings | 920 | Mostly `metadata: None` in ingested scientific skills. |
| `allowed-tools` must be a string | 2 | |

Every skill already satisfies "`name` matches the directory" and "description
of 1-1024 characters", because the gate enforces a stricter 200-character
limit.

Renaming 3,297 skills would break every existing `rho skills install ... <name>`
reference, so this change does not rename them. Moving `tags` under
`metadata` for 14,011 files is a mechanical migration that also needs a
decision on Rho's search behavior, so it is tracked as follow-up work.

## What is conformant today

- The first-party skills in `categories/graycode/` (`rho-workflow`,
  `rover-verify`, `across-checkpoint`) conform fully. CI runs
  `python tools/check_agentskills.py --strict categories/graycode` so they stay
  that way.
- New skills can conform. Put tags in `metadata.tags` as a comma- or
  space-separated string instead of a top-level list. The validator and the
  registry generator accept both, and top-level `tags` wins if both are set:

  ```yaml
  ---
  name: my-skill
  description: What it does and when to use it.
  license: MIT
  metadata:
    author: your-github-username
    version: "1.0"
    tags: python, testing
  ---
  ```

- `allowed-tools` must be a space-separated string in the spec. Two ingested
  skills use a YAML list, because their tool names contain spaces. The corpus
  gate accepts that form (as Claude Code does); only `check_agentskills.py`
  reports it.

## Checking a skill

```bash
# Gap summary for the corpus (informational, exits 0)
python tools/check_agentskills.py --all

# Fail if any given skill (or every skill in a category) is not conformant
python tools/check_agentskills.py --strict categories/<category>/<skill>
```

The rules mirror `skills-ref`'s validator (`ALLOWED_FIELDS`, the 64/1024/500
limits, and the name rules). This repository does not install `skills-ref` in
CI; `tools/check_agentskills.py` reimplements those checks without adding a
dependency.
