---
name: node-rest-api-development
description: "Use when building, configuring, or debugging Fastify Node.js backend servers and REST APIs — defining routes, plugins, JSON Schema validation, error handling, auth, CORS, and deployment."
license: MIT
tags:
- nodejs
- rest-api
- backend
- http
---

## When to use

Use this skill when you need to:
- Develop backend applications using Fastify
- Implement Fastify plugins and route handlers
- Get guidance on Fastify architecture and patterns
- Use TypeScript with Fastify (strip types)
- Implement testing with Fastify's inject method
- Configure validation, serialization, and error handling

## Quick Start

A minimal, runnable Fastify server to get started immediately:

```ts
import Fastify from 'fastify'

const app = Fastify({ logger: true })

app.get('/health', async (request, reply) => {
  return { status: 'ok' }
})

const start = async () => {
  await app.listen({ port: 3000, host: '0.0.0.0' })
}
start()
```

## Recommended Reading Order for Common Scenarios

- **New to Fastify?** Start with `plugins.md` → `routes.md` → `schemas.md`
- **Adding authentication:** `plugins.md` → `hooks.md` → `authentication.md`
- **Improving performance:** `schemas.md` → `serialization.md` → `performance.md`
- **Setting up testing:** `routes.md` → `testing.md`
- **Going to production:** `logging.md` → `configuration.md` → `deployment.md`

## How to use

Read individual rule files for detailed explanations and code examples:

- rules/plugins.md - Plugin development and encapsulation
- rules/routes.md - Route organization and handlers
- rules/schemas.md - JSON Schema validation
- rules/error-handling.md - Error handling patterns
- rules/hooks.md - Hooks and request lifecycle
- rules/authentication.md - Authentication and authorization
- rules/testing.md - Testing with inject()
- rules/performance.md - Performance optimization
- rules/logging.md - Logging with Pino
- rules/typescript.md - TypeScript integration
- rules/decorators.md - Decorators and extensions
- rules/content-type.md - Content type parsing
- rules/serialization.md - Response serialization
- rules/cors-security.md - CORS and security headers
- rules/websockets.md - WebSocket support
- rules/database.md - Database integration patterns
- rules/configuration.md - Application configuration
- rules/deployment.md - Production deployment
- rules/http-proxy.md - HTTP proxying and reply.from()

## Core Principles

- **Encapsulation**: Fastify's plugin system provides automatic encapsulation
- **Schema-first**: Define schemas for validation and serialization
- **Performance**: Fastify is optimized for speed; use its features correctly
- **Async/await**: All handlers and hooks support async functions
- **Minimal dependencies**: Prefer Fastify's built-in features and official plugins
