---
name: ai-app-sdk-javascript
description: "Builds AI-powered applications with Genkit in Node.js/TypeScript, covering flows, agents, prompts, middleware, CLI tracing and debugging, and error troubleshooting for the JavaScript AI SDK."
license: Apache-2.0
tags:
- ai
- genkit
- typescript
- agents
- llm
---

# Genkit JS

## Prerequisites

Ensure the `genkit` CLI is available.
-   Run `genkit --version` to verify. Minimum CLI version needed: **1.29.0**
-   If not found or if an older version (1.x < 1.29.0) is present, install/upgrade it: `npm install -g genkit-cli@^1.29.0`.

**New Projects**: I you are setness**:
    -   Run type checks (e.g., `npx tsc --noEmit`) after making changes.
    -   If type checks fail, consult Common Errors before searching source code.
    -   Verify with traces, not a blind run. Running the app directly (`node`/`tsx`/`npm start`) does **not** capture dev traces. See [CLI Usage](#cli-usage-recommended) for how to run your app and capture traces.
6.  **Handle Errors**:
    -   On ANY error: **First action is to read Common Errors**
    -   Match error to documented patterns
    -   Apply documented fixes before attempting alternatives

## Finding Documentation

Use the Genkit CLI to find authoritative documentation:

1.  **Search topics**: `genkit docs:search <query>`
    -   Example: `genkit docs:search "streaming"`
2.  **List all docs**: `genkit docs:list`
3.  **Read a guide**: `genkit docs:read <path>`
    -   Example: `genkit docs:read js/flows.md`

## CLI Usage (recommended)

`genkit start` unintrusively wraps any Node.js program that uses the Genkit library, running it unchanged while capturing traces from every Genkit action so you can **prove tools were actually called and inspect model I/O** from the terminal, even for headless checks. It forwards stdio, so interactive CLI tools that rely on stdin/stdout work without issues. Running your app directly (`node`/`tsx`/`npm start`) skips trace capture, so you're debugging blind.

**Primary pattern (default):** prefix `genkit start --` to your normal run command. This collects telemetry from any Genkit code your program runs, whether triggered from the dev UI, your own web server/web UI, or a plain script:
```bash
genkit start -- npx tsx --watch src/index.ts
genkit start --noui -- npx tsx src/index.ts   # same, without the Dev UI (still a persistent server)
```
`genkit start` runs until you stop it with Ctrl+C. That is expected and correct for the common cases: a server your web/mobile app calls, or an interactive CLI you exit yourself. `--noui` only drops the Dev UI; it is **not** a one-shot command and will not exit on its own. Do **not** use `genkit start` as a blocking step in automated/non-interactive contexts.

**Non-interactive use (agents/CI):** add the global `--non-interactive` flag before `--` so the CLI uses defaults and never blocks on a prompt (e.g. the first-run analytics notice): `genkit start --non-interactive -- npx tsx src/index.ts` (works with `flow:run` too).

**Run a flow (`flow:run`):** invoke a specific flow by name from the CLI. Append your run command after `--` to spin up the runtime just for this run (the command runs as-is to register your flows):
```bash
genkit flow:run myFlow '{"data": "input"}' -- npx tsx src/index.ts
```
This is **self-terminating**: it runs the flow once, prints a `Trace ID`, then exits (inspect it with `genkit trace:get <id>`). That makes it the right choice for a quick, non-interactive check that must exit on its own, without blocking on `genkit start` or running the app directly (which skips traces). Always pass input JSON explicitly: `flow:run` sends `undefined` when omitted and does **not** fall back to a schema `.default()`. Note: `flow:run` runs **flows** (`ai.defineFlow`), not agents; you can't `flow:run` an agent (`ai.defineAgent`) directly. To exercise an agent from the CLI, wrap one turn in a throwaway flow and run that (see Agents).

**Debugging with traces:** the fastest way to see prompts, model inputs/outputs, tool calls, latencies, and errors. Inspect from the terminal after any run under `genkit start`:
```bash
genkit trace:list                        # find recent trace IDs
genkit trace:get <traceId>               # full trace details (inputs, outputs, tool calls, errors)
genkit trace:get <traceId> --format json # machine-readable JSON, safe to pipe into jq or other parsers
```

For machine-readable output, pass `--format json` to get clean JSON you can pipe into `jq` or other parsers. The **default** output is human-oriented (banner/log lines, possible truncation on large traces), so don't pipe that form directly; use `--format json`, grep, or the Dev UI trace viewer.


See CLI Reference for more commands, and `genkit --help` for the full list.


## References

-   Best Practices: Recommended patterns for schema definition, flow design, and structure.
-   Dotprompt: `.prompt` files — `promptDir`, `ai.prompt()`, variants, partials, named schemas, and `tools`/`maxTurns`/`returnToolRequests`/`use` frontmatter.
-   Docs & CLI Reference: Documentation search, CLI tasks, and workflows.
-   Common Errors: Critical "gotchas", migration guide, and troubleshooting.
-   Setup Guide: Manual setup instructions for new projects.
-   Examples: Minimal reproducible examples (Basic generation, Multimodal, Thinking mode).
-   Agents (Beta): Agent basics, serving, and client-managed state. Deeper topics: sessions, human-in-the-loop, branching, background agents, state, artifacts, multi-agent, custom agents, deployment.
-   Middleware: using middleware and the `@genkit-ai/middleware` package. See also building custom middleware.
