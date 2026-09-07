---
name: command-resource-monitor
description: "Wrap any command to capture wall-clock time, CPU, and memory usage as structured logs for agent review."
license: Apache-2.0
tags:
- monitoring
- performance
- devops
---

# Duct Run Capture

Use this skill when a command, build, test, verify step, or long-running job should be measured rather than run blind. It wraps the command with [`con/duct`](https://github.com/con/duct), a lightweight monitor that records resource usage for a process and all of its children.

The point is **agent review**: after a run, another agent (or a human reviewer) can read the captured logs and see how long the command took, how much memory and CPU it used, and whether it succeeded, without re-running anything.

## When To Use

- Before claiming a change is "fast enough", "leaner", or "within budget": measure it.
- When a verify or benchmark command feeds a keep/discard decision in an experiment loop.
- When a long-running job is left unattended and a reviewer later needs to know what it consumed.
- When comparing two alternatives by a resource metric (time, peak memory, CPU).

If a run does not need to be reviewed for resource usage, do not add the wrapper; plain execution is fine.

## Install

```bash
pip install con-duct          # provides `duct` and `con-duct`
pip install 'con-duct[all]'   # adds plotting, pretty-print, and .env support
```

`duct <command>` is equivalent to `con-duct run <command>`.

## Basic Usage

Wrap the real command after `duct` and its options:

```bash
duct -p .duct/logs/{datetime}-{pid}_ -- pytest -q
```

- Everything after `--` is the command being measured, run unchanged.
- `-p/--output-prefix` controls where logs go. The default is `.duct/logs/{datetime}-{pid}_`; `{datetime}` and `{pid}` are filled in so parallel runs never collide.
- duct exits with the wrapped command's own exit code and prints a one-line summary (exit code, wall-clock time, peak/average RSS, peak/average CPU).

Useful options:

- `--sample-interval` / `--s-i`: seconds between resource polls (default `1.0`; lower for short runs).
- `--report-interval` / `--r-i`: seconds between rows written to the usage log.
- `-c {all,none,stdout,stderr}`: which streams to capture to files.
- `-o {all,none,stdout,stderr}`: which streams to also forward to your terminal.
- `--message` / `-m`: a free-text note stored with the run (e.g. the hypothesis or experiment id).
- `--fail-time`: delete logs if the command fails within N seconds (skip noise from instant failures).
- `--clobber`: overwrite existing log files at the prefix.

Many options also read from environment variables (`DUCT_OUTPUT_PREFIX`, `DUCT_SAMPLE_INTERVAL`, `DUCT_REPORT_INTERVAL`, `DUCT_CAPTURE_OUTPUTS`, `DUCT_MESSAGE`, ...) and from `.env` files under `/etc/duct/`, `${XDG_CONFIG_HOME:-~/.config}/duct/`, and `.duct/`.

## Output Files

For an output prefix `P`, duct writes:

- `Pinfo.json`: system info plus an `execution_summary` (exit code, wall-clock time, peak/average RSS and VSZ, peak/average CPU and memory percent, sample/report counts, start/end time, working directory) and the `output_paths`.
- `Pusage.jsonl`: JSON Lines, one resource sample row per report interval (per-process and aggregate stats over time).
- `Pstdout` and `Pstderr`: captured output streams.

`info.json` is the file a reviewer should read first; it is small and holds the headline numbers.

## Reviewing A Run

Pretty-print, list, and plot helpers ship with `con-duct[all]`:

```bash
con-duct ls   .duct/logs/*info.json     # tabular index of past runs
con-duct pp   .duct/logs/<prefix>info.json   # human-readable dump of one run
con-duct plot .duct/logs/<prefix>usage.jsonl # resource-usage-over-time chart
```

For a compact, dependency-free review summary suitable for pasting into a notebook entry or a PR review, use the helper in this skill:

```bash
python skills/duct/scripts/summarize_run.py .duct/logs/<prefix>info.json
python skills/duct/scripts/summarize_run.py .duct/logs/          # newest run under a dir
python skills/duct/scripts/summarize_run.py .duct/logs/<prefix>info.json --json
```

It reads `info.json`, prints exit code, wall-clock time, peak/average memory, and peak/average CPU in readable units, and flags whether the run produced any samples (very short runs may record none).

## Guardrails

1. Respect any parent constitution, project policy, or task-level write constraint already in scope.
2. Treat the captured numbers as best-effort: duct polls at an interval, so very short runs may record zero samples and report `null` for peak memory or CPU. Lower `--sample-interval` or report that the run was too short to measure.
3. duct tracks a process session; a command that starts a brand-new session escapes tracking, and duct stops collecting once the primary process exits even if children remain. Note this when reviewing background jobs.
4. Write logs to a per-run prefix (keep `{datetime}` and `{pid}`) so parallel runs never overwrite each other.
5. Do not capture secrets: streams written to `stdout`/`stderr` files may contain credentials or tokens; use `-c none` or scrub before sharing when output is sensitive.
6. Report the wrapped command's real exit code; do not let the wrapper mask a failure as success.

## With labnb

When running an experiment under the `labnb` skill, wrap the verify or benchmark command with `duct` and store the logs inside the experiment's `artifacts/` directory:

```bash
duct -p "$EXPERIMENT_DIR/artifacts/verify-{datetime}-{pid}_" -- $VERIFY_COMMAND
```

This satisfies the labnb requirement to instrument runs well enough to inspect logs, progress, and resource consumption from outside the process, and it gives a later resume or review step real numbers to compare against the recorded metric.

The captured `info.json` can also be fed straight into labnb's loop breaker so a slice is cut short on runaway memory:

```bash
python skills/labnb/scripts/monitor_slice.py check \
  --experiment-dir "$EXPERIMENT_DIR" \
  --usage-file "$EXPERIMENT_DIR/artifacts/verify-<prefix>_info.json" \
  --max-rss-bytes 8000000000 --max-pmem 90
```
