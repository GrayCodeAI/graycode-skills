---
name: ai-app-sdk-dart
description: "Builds AI agents and flows in Dart/Flutter with the Genkit Dart SDK, covering generation, tools, prompts, agents, plugins, CLI tracing, and type-safe schema definitions for LLM integration."
license: Apache-2.0
tags:
- ai
- dart
- flutter
- agents
- llm
---

# Genkit Dart

Genkit Dart is an AI SDK for Dart that provides a unified interface for code generation, structured outputs, tools, flows, and AI agents.

## Core Features and Usage
If you need help with initializing Genkit (`Genkit()`), Generation (`ai.generate`), Tooling (`ai.defineTool`), Flows (`ai.defineFlow`), Embeddings (`ai.embedMany`), streaming, or calling remoe flow endpoints, plcustom compatible endpoints. |
| `genkit_middleware` | references/genkit_middleware.md | Load for Tooling for specific agentic behavior: `filesystem`, `skills`, and `toolApproval` interrupts. |
| `genkit_mcp` | references/genkit_mcp.md | Load for Model Context Protocol integration (Server, Host, and Client capabilities). |
| `genkit_chrome` | references/genkit_chrome.md | Load for Running Gemini Nano locally inside the Chrome browser using the Prompt API. |
| `genkit_shelf` | references/genkit_shelf.md | Load for Integrating Genkit Flow actions over HTTP using Dart Shelf. |
| `genkit_firebase_ai` | references/genkit_firebase_ai.md | Load for Firebase AI plugin interface (Gemini API via Vertex AI). |

## External Dependencies
Whenever you define schemas mapping inside of Tools, Flows, and Prompts, you must use the [schemantic](https://pub.dev/packages/schemantic) library. 
To learn how to use schemantic, ensure you read references/schemantic.md for how to implement type safe generated Dart code. This is particularly relevant when you encounter symbols like `@Schema()`, `SchemanticType`, or classes with the `$` prefix. Genkit Dart uses schemantic for all of its data models so it's a CRITICAL skill to understand for using Genkit Dart.

## Best Practices
- **Agent or flow?** If the task is conversational, multi-turn, or described as "an agent", "assistant", or "chatbot", build it with `ai.defineAgent` (see Agents) rather than hand-rolling a `generate` + tools loop inside a flow. Reach for a plain flow only for single-shot, stateless generation.
- Always check that code cleanly compiles using `dart analyze` before generating the final response.
- Always use the Genkit CLI for local development and debugging.
- Verify with traces, not a blind run. Running the app directly (`dart run`) does not capture dev traces. See the [Genkit CLI](#genkit-cli-recommended) section for how to run your app and capture traces.
