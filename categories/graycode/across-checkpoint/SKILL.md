---
name: across-checkpoint
description: Record git-native checkpoints, sessions and verification evidence with Across. Explain, compare or restore checkpoints into a new worktree and write handoffs so work survives between agent sessions.
license: MIT
compatibility: Requires the across CLI (local alpha) and git.
metadata:
  author: GrayCode AI
  version: "1.0"
  tags: across, graycode, git, checkpoints, provenance
  verified-against: across --help output, source build of 2026-09-27
---

# Checkpoints and continuity with Across

Across (github.com/GrayCodeAI/across) is GrayCode's git-native engineering
context, provenance and checkpoint system. It is local alpha software. It
keeps its own SQLite state in `--home` / `$ACROSS_HOME` (default
`~/.local/share/across`), and restores go into new worktrees rather than
resetting your checkout.

## When to use

- At the start and end of an agent session, so the next session (or another
  agent) can pick up with evidence instead of guesses.
- Before a risky change, so you can restore the prior state into a separate
  worktree.
- To answer "why is this line here?" from git blame plus recorded
  checkpoints.

## Instructions

1. Register the repository once and keep its ID:

   ```bash
   across repo add .          # prints repo_<id>
   across repo list           # id, name, path, kind, branch
   ```

2. Start a session for the agent doing the work:

   ```bash
   across session start --repo <repo-id> --agent rho      # prints sess_<id>
   ```

3. Checkpoint at meaningful points. A checkpoint binds the current `HEAD`
   revision to the session and a message:

   ```bash
   across checkpoint create --repo <repo-id> --session <sess-id> --message "before refactor"
   across checkpoint list --repo <repo-id>
   ```

   The basis is recorded as `capture_time_head_not_causation`. The
   checkpoint records which revision was checked out, not that the agent
   authored it. Commit first if the checkpoint must cover your edits.

4. Attach verification evidence to the revision:

   ```bash
   across verify run --repo <repo-id> --name unit -- python3 -m pytest -q
   across verify list --repo <repo-id>
   ```

   `verify run` executes locally without a sandbox and records the exit code.
   `across verify add` records a claim as STATED without running anything;
   label it as such when you report it.

5. Inspect, compare and restore:

   ```bash
   across checkpoint show <cp-id>
   across checkpoint explain <cp-id>        # checkpoint plus bound evidence
   across checkpoint compare <cp-a> <cp-b>  # diffstat between the two revisions
   across checkpoint restore <cp-id>        # into a NEW worktree; the current checkout is untouched
   across checkpoint bundle <cp-id> --output cp.json   # versioned evidence bundle
   ```

   Restore brings back only git-tracked code. External databases, cloud
   state and untracked files are not restored.

6. Hand off and close the session:

   ```bash
   across handoff --session <sess-id> --output HANDOFF.md   # --format json for tools
   across session close <sess-id>
   ```

7. Trace provenance for a line:

   ```bash
   across why path/to/file.go:42 --repo <repo-id>
   ```

   Attribution confidence is LOW unless a checkpoint revision matches the
   blamed commit. Never state that an agent wrote a line on weaker evidence.

## Verification

- `across checkpoint list --repo <repo-id>` shows the new checkpoint with the
  expected revision.
- `across checkpoint show <cp-id>` lists the verification you recorded
  (`basis=executed_by_across_local_runner` for `verify run`).
- `across doctor` reports `sqlite_integrity: ok`.

## References

- Across: https://github.com/GrayCodeAI/across (see its STATUS for current
  limits)
- Related skills: `rho-workflow`, `rover-verify`
