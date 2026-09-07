---
name: vitest-testing-framework
description: "Use for Vitest API and configuration questions — mocking with vi, spies, fake timers, coverage, fixtures, snapshots, and test filtering anywhere in the project."
license: Apache-2.0
tags:
- vitest
- testing
- mocking
---

Vitest is a next-generation testing framework powered by Vite. It provides a Jest-compatible API with native ESM, TypeScript, and JSX support out of the box. Vitest shares the same config, transformers, resolvers, and plugins with your Vite app.

**Key Features:**

- Vite-native: Uses Vite's transformation pipeline for fast HMR-like test updates
- Jest-compatible: Drop-in replacement for most Jest test suites
- Smart watch mode: Only reruns affected tests based on module graph
- Native ESM, TypeScript, JSX support without configuration
- Multi-threaded workers for parallel test execution
- Built-in coverage via V8 or Istanbul
- Snapshot testing, mocking, and spy utilities

> The skill is based on Vitest 3.x, generated at 2026-01-28.

## Core

| Topic         | Description                                                     | Reference                                    |
| ------------- | --------------------------------------------------------------- | -------------------------------------------- |
| Configuration | Vitest and Vite config integration, defineConfig usage          | core-config     |
| CLI           | Command line interface, commands and options                    | core-cli           |
| Test API      | test/it function, modifiers like skip, only, concurrent         | core-test-api |
| Describe API  | describe/suite for grouping tests and nested suites             | core-describe |
| Expect API    | Assertions with toBe, toEqual, matchers and asymmetric matchers | core-expect     |
| Hooks         | beforeEach, afterEach, beforeAll, afterAll, aroundEach          | core-hooks       |

## Features

| Topic        | Description                                                    | Reference                                                  |
| ------------ | -------------------------------------------------------------- | ---------------------------------------------------------- |
| Mocking      | Mock functions, modules, timers, dates with vi utilities       | features-mocking         |
| Snapshots    | Snapshot testing with toMatchSnapshot and inline snapshots     | features-snapshots     |
| Coverage     | Code coverage with V8 or Istanbul providers                    | features-coverage       |
| Test Context | Test fixtures, context.expect, test.extend for custom fixtures | features-context         |
| Concurrency  | Concurrent tests, parallel execution, sharding                 | features-concurrency |
| Filtering    | Filter tests by name, file patterns, tags                      | features-filtering     |

## Advanced

| Topic        | Description                                             | Reference                                                    |
| ------------ | ------------------------------------------------------- | ------------------------------------------------------------ |
| Vi Utilities | vi helper: mock, spyOn, fake timers, hoisted, waitFor   | advanced-vi                     |
| Environments | Test environments: node, jsdom, happy-dom, custom       | advanced-environments |
| Type Testing | Type-level testing with expectTypeOf and assertType     | advanced-type-testing |
| Projects     | Multi-project workspaces, different configs per project | advanced-projects         |
