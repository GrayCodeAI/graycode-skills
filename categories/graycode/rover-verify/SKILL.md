---
name: rover-verify
description: Verify an agent's code change with Rover. Snapshot base and candidate, run the repository's approved checks, and read the ACCEPTED, BLOCKED or REVIEW_REQUIRED decision with its evidence.
license: MIT
compatibility: Requires the rover CLI (alpha) and git. Local checks run with your user permissions and are not sandboxed.
metadata:
  author: GrayCode AI
  version: "1.0"
  tags: rover, graycode, verification, code-review, evidence
  verified-against: rover help output, source build of 2026-09-27
---

# Verify changes with Rover

Rover (github.com/GrayCodeAI/rover) is GrayCode's terminal-first agent
workspace with verification and evidence. It is alpha software. It compares
exact git source states, runs checks you approved, and records a decision
with evidence. It never pushes, merges or deploys.

## When to use

- Before accepting edits made by an agent (Rho or any other).
- When you need a recorded, reviewable result instead of "the tests passed
  on my machine".

## Prerequisites

1. Keep Rover's state outside the repository. It defaults to `$ROVER_HOME`,
   else your user config directory (`rover help` prints it); override it with
   `rover --state DIR`.
2. Commit an approved check configuration at `.rover/config.json` in the
   base revision. By default Rover reads it from the base snapshot, not from
   your working tree.

Preview a starting config (writes nothing):

```bash
rover init --repo .
rover init --repo . --apply     # create .rover/config.json; never overwrites
```

Automatic check suggestions recognize Go only. For other languages, write
the checks yourself. Every check must set `parser` explicitly:

```json
{
  "schema": "rover/v1alpha1",
  "checks": [
    {"id": "unit", "argv": ["python3", "-m", "pytest", "-q"], "timeout": "5m",
     "required": true, "parser": "exit-code"}
  ],
  "policy": {"require_review": true}
}
```

Parsers: `exit-code`; `go-test-json` (needs `min_tests >= 1`); `junit` (needs
`report_path` and `min_tests`). Commands are argv lists with no shell
expansion. Each check runs in a fresh copy of the candidate without `.git`.

## Instructions

1. Verify the uncommitted working tree against `HEAD` in one step:

   ```bash
   rover check --repo . --worktree --allow-local
   ```

   `--allow-local` authorizes running the checks with your user permissions.
   Add `--include-untracked` to include new, unignored files.

2. Or verify two committed revisions:

   ```bash
   rover verify --base main --candidate HEAD --allow-local
   ```

   `--mode restricted-docker --image IMAGE@sha256:DIGEST` uses the Docker
   adapter instead, which is not yet validated live.

3. Read the decision and act on the exit code:

   | Exit | Decision | Meaning |
   |---|---|---|
   | 0 | ACCEPTED | Required checks passed under the supplied policy |
   | 1 | BLOCKED | A required check failed |
   | 2 | error / INCONCLUSIVE | Missing, truncated or wrong-subject evidence, or zero required checks |
   | 3 | REVIEW_REQUIRED | Checks passed, but the policy or a change finding needs a human review |

4. Inspect and record the evidence (the output prints the investigation ID):

   ```bash
   rover report --id <investigation>
   rover diff --id <investigation> --output change.patch
   rover review --id <investigation> --note "Reviewed the diff"
   ```

## Rules

- Passing checks prove only what those checks cover. Rover says so in its
  report (the `UNKNOWN` lines); repeat the caveat, and do not claim the
  change is correct beyond them.
- Local advisory execution is not a sandbox. Do not run `--allow-local`
  against code you would not run yourself.
- Do not weaken or remove checks in `.rover/config.json` to get ACCEPTED.
  Editing the config in the working tree produces a finding; approved
  config changes go through a reviewed commit.

## Verification

- Exit code 0 (ACCEPTED), or 3 (REVIEW_REQUIRED) followed by a recorded
  `rover review` note.
- `rover report --id <investigation>` lists every required check as PASS.

## References

- Rover: https://github.com/GrayCodeAI/rover (docs/CONFIGURATION.md, docs/CLI.md)
- Related skills: `rho-workflow`, `across-checkpoint` (record the
  verification against a checkpoint)
