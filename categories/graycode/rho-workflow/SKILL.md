---
name: rho-workflow
description: Operate Rho, GrayCode's terminal AI coding agent, from the shell. Covers readiness, folder trust, plans, headless exec, checkpoints, snapshots, commit review and skills.
license: MIT
compatibility: Requires the rho CLI (pre-1.0) and a configured model provider for prompt, exec and review commands.
metadata:
  author: GrayCode AI
  version: "1.0"
  tags: rho, graycode, agent-workflow, cli
  verified-against: rho --help output, source build of 2026-09-27
---

# Rho workflow

Rho (github.com/GrayCodeAI/rho) is GrayCode's terminal AI coding agent. It is
pre-1.0 alpha software, so check `rho <command> --help` before relying on a
flag that is not listed here. Every command below was checked against the
CLI's own `--help` output.

## When to use

- You need to run Rho without its interactive TUI: one-shot prompts,
  scripted or CI runs, JSON output.
- You are managing Rho's local state for a project: folder trust, plans,
  named checkpoints, file snapshots, installed skills.
- You are setting up automatic review of commits.

## 1. Check readiness before running tasks

```bash
rho preflight            # local readiness; add --live to test the provider and credentials
rho path --json          # developer-path readiness report (keys in OS keychain, model, flux)
rho doctor               # local diagnostics
```

`preflight --json` returns `"ready": false` until a provider is configured
(run `rho`, then `/config`). Do not start a long `exec` run until it reports
ready.

## 2. Trust the folder, or project automation stays off

Project-scoped hooks, MCP servers, LSP configs and plugins load only from
trusted folders. Rho's skill auto-loader also skips the project skill
directories (`./.rho/skills`, `./.zero/skills`, `./skills`) in untrusted
folders.

```bash
rho trust check            # "trusted: false" for a new checkout
rho trust add . --reason "my repo"
rho trust list
```

Trust only repositories whose automation you have reviewed.

## 3. Run a task

```bash
rho -p "explain the build system"                       # one prompt, print, exit
rho exec "fix the failing unit tests"                   # multi-turn autonomous run
rho exec --auto semi "refactor parser.go"               # autonomy: supervised|basic|semi|full|yolo
rho exec --worktree "try the migration"                 # isolated git worktree
rho exec --ephemeral --json "run tests and report" > result.json   # CI: no session saved
echo "review main.go" | rho exec -                      # prompt from stdin
```

- The default autonomy is `supervised`, which asks before every tool call.
  Raise it only as far as the task needs. `yolo` never asks.
- `--max-turns N` bounds a run; `--model` picks a model from the flux
  catalog (`rho models`).
- `-o stream-json` emits newline-delimited progress events for tooling.

## 4. Plan larger work

```bash
rho plan create "add OAuth device login"   # prints a planning prompt (system + user) to send to a model
rho plan list                              # plans saved for this project in Rho's state dir
rho plan show <name>
rho plan done <task-id>                    # most recent plan; or: rho plan done <name> <task-id>
```

`plan create` does not call a model or save a plan by itself; it prints the
prompt to use.

## 5. Save and restore progress

Named checkpoints capture a session so you can resume the conversation:

```bash
rho checkpoint save before-refactor        # latest session in this directory
rho checkpoint list
rho resume before-refactor                 # restores it and prints the command to continue
```

Rho snapshots every file it modifies, so edits can be undone:

```bash
rho snapshot list
rho snapshot diff <hash>
rho snapshot restore <hash>
```

Snapshots cover files Rho changed; they are not a replacement for git. Commit
or branch before large runs.

## 6. Review commits

```bash
rho review run <sha>                       # review one commit (--concerns security,perf)
rho review init                            # install a post-commit hook (-f overwrites an existing one)
rho review list
```

`rho verify` is not code verification. It checks Rho's own tamper-evident
security log and governance policy. To verify a code change, use Rover (see
the `rover-verify` skill).

## 7. Use community skills

```bash
rho skills search pandas                   # searches the published registry
rho skills info <name>
rho skills install GrayCodeAI/graycode-skills <name>              # user scope (default)
rho skills install GrayCodeAI/graycode-skills <name> --scope project
rho skills list                            # installed skills
```

In the interactive REPL, `/skills use <name>` activates an installed skill.

## Verification

- `rho preflight --json` shows `"ready": true` before automated runs.
- After `exec`, check the exit status and inspect the diff (`git diff`), or
  hand the change to Rover (`rover-verify`) before accepting it.
- `rho checkpoint list` shows the checkpoint you expect to resume.

## References

- Rho: https://github.com/GrayCodeAI/rho (README for install instructions)
- Related skills: `rover-verify` (verify changes), `across-checkpoint`
  (git-native provenance and handoffs)
