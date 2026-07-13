---
name: std-golang-concurrency
description: "Write safe concurrent Go code with goroutines, channels, and context. Use when implementing concurrency with goroutines, channels, or context in Go."
license: MIT
tags: [general]
metadata: None
triggers: None
keywords: None
---

# Golang Concurrency

## **Priority: P0 (CRITICAL)**

## Principles

- **Share Memory by Communicating**: Use channels instead of shared memory.
- **Context King**: Always pass `ctx` to manage cancellation/timeouts.
- **Prevent Leaks**: Never start goroutine without knowing how it will stop.
- **Race Detection**: Always run tests with `go test -race`.

## Implementation Workflow

1. **Choose primitive** — Channels for data passing, `sync.Mutex` for simple state protection, `errgroup` for parallel tasks with error handling.
2. **Pass context** — Every goroutine that I/O or long work must accept `context.Context`.
3. **Define exit paths** — Every goroutine must clear shutdown mechanism (context cancellation, channel close, or WaitGroup).
4. **Use select for multiplexing** — Handle multiple channels or timeouts with `select`.
5. **Test with race detector** — Run `go test -race` in CI.

See ErrGroup and concurrency patterns and context timeout examples

## Anti-Patterns

- **No goroutine leaks**: ensure every goroutine known exit path.
- **No shared global state**: use channels or sync primitives across goroutines.
- **No bare goroutines**: use `errgroup` or `WaitGroup` for lifecycle management.

## References

- Concurrency Patterns
- Context Usage