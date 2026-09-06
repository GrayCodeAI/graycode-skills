---
name: production-backend-implementation
description: "Use when implementing production-grade backends in Express, Fastify, NestJS, Hono, or Next.js APIs with intent-first analysis, validation, and library-first code."
license: MIT
tags:
- backend
- api
- typescript
- security
- best-practices
---

# Skills

This skill is the agent's guarantee of **production-grade, human-crafted backend engineering**. It exists so that any backend the agent produces looks and behaves like a senior backend engineer built it on purpose for that specific product — properly validated, typed, secured, observable, and maintainable — never a throwaway tutorial scaffold. The agent must treat this skill as mandatory whenever it is triggered and complete the intent-first analysis below BEFORE writing any code. Skipping the analysis phase is forbidden.

## When to use

Activate this skill when the user's prompt contains ANY of the following terms or signals:

- `backend`, `API`, `server`, `server-side`, `service`, `endpoint`, `REST API`, `RESTful`, `CRUD`, `webhook`, `route`.
- `Express`, `Fastify`, `NestJS`, `Hono`, `Next.js API`, `Next.js route handler`, `Node.js`, `TypeScript server`, `tRPC`.
- `authentication`, `auth`, `JWT`, `OAuth`, `login`, `RBAC`, `authorization`, `password hashing`, `sessions`.
- `database`, `Prisma`, `Drizzle`, `ORM`, `PostgreSQL`, `MySQL`, `MongoDB`, `SQLite`, `schema`, `migration`, `Redis`.
- `production backend`, `production-grade`, `industry-level`, `secure API`, `best practice backend`, `scalable backend`.
- `build me a backend`, `build an API for my app`, `backend for my [web/mobile] app`, `add an API`, `make the server`.
- `validation`, `rate limiting`, `logging`, `observability`, `error handling`, `health check`, `file upload`, `queue`, `background job`.
- User asks to implement an API contract, turn a requirement/PRD into a working backend, or generate framework-specific backend code.
- ANY task where the user expects working, production-worthy server code rather than an architecture discussion.

When in doubt, activate. This skill composes with `backend-core` (architecture design) and `api-design` (contracts): those decide WHAT and WHY; `backend-craft` decides HOW to implement it cleanly. `requirements-analysis`/PRD feeds the intent here.

## Instructions

### Phase 0 — Intent-First Analysis (MANDATORY, do this BEFORE any code)

Never generate a backend directly from a prompt. Execute these steps in order and briefly state the outcome of each so the user can follow your reasoning.

1. **Deconstruct the project intent.**
   - What is being built? (product SaaS core, BFF for a frontend, internal admin tool, MVP proof-of-concept, e-commerce, dashboard API...)
   - Who consumes it and what is the primary goal — serve a product, integrate systems, power an app, enable internal ops?
   - Restate in one line: *"This backend exists to [capability] for [consumer] and should be [maturity/rigor]."*

2. **Classify the backend type (Mode).** Select exactly one and state it — this sets the rigor switch:
   - **CRUD / MVP:** A simple, fast-shipping resource API. Minimal moving parts, but still safe and typed.
   - **Production-SaaS:** Full rigor — auth, RBAC, validation, observability, rate limiting, tests, env validation, security headers, graceful shutdown, migrations.
   - **BFF / API layer:** A thin aggregation/adapter layer tailored to specific clients; typed contracts, session/edge-friendly, mostly read + orchestration.
   - **Internal:** An internal tool/admin API on a trusted network; solid but lighter rigor than public SaaS.
   - If uncertain, ASK the user for scope and maturity before proceeding.

3. **Select the stack and structure by intent.** Choose a framework and tooling that fit the backend type and the team context, and state the choice + why:
   - **Framework/runtime:** Next.js App Router route handlers (full-stack integration), Express/Fastify (pure API), NestJS (enterprise modular), Hono (edge/serverless), tRPC (type-safe full-stack).
   - **Language:** TypeScript (default) unless the environment dictates otherwise.
   - **ORM/query layer:** Prisma or Drizzle for typed data access + migrations.
   - **Validation:** Zod everywhere.
   - **Auth:** jose/jsonwebtoken, lucia, or framework-native session/OAuth.
   - **Cache/queue:** Redis + BullMQ where needed.
   - Prefer the mature, popular choice for each area (see Library-First Principle below).

4. **Take user input where ambiguous.** If scope, auth model, data source, framework preference, deployment target, or "expected output" shape is unclear, ask 2–4 targeted questions so the result matches expectation. Never silently pick critical defaults when intent is ambiguous.

5. **Industry-level reasoning, then generate.** For each significant decision (validation boundary, error envelope, folder layout, auth flow, migration strategy) give a one-line "why" as a senior engineer would. Only then write code.

### Library-First Principle (Human-Written Over Self-Written) — MANDATORY

Mirror the frontend human-crafted tooling approach, enforced on the backend:

- **Use mature, maintained, human-written libraries for every standard concern** — validation, env parsing, ORM/migrations, logging, security headers, rate limiting, auth/JWT, pagination, UUIDs, queues, uploads, object storage, email, PDF, caching, compression. Do not reimplement what the ecosystem already solves.
- **Write custom code ONLY when** no suitable library exists, OR the need is genuinely project-unique business logic (your domain rules, custom algorithms, proprietary integrations).
- **Decision gate per need:**
  1. Does a mature, popular, maintained library exist? → **USE it** (name it and say why).
  2. Library exists but is overkill? → pick a smaller popular alternative first.
  3. No library, or the need is genuinely project-specific → **then** write custom, typed, documented code and state explicitly why no library was used.

- **Forbidden from-scratch patterns** (avoid unless the item above step 3 applies): hand-rolled validation, ad-hoc env parsing, manual JWT signing, raw hand-written SQL-per-endpoint for CRUD, ad-hoc `console.log`-only logging, from-scratch rate limiters, hand-rolled hashing.
- **Result:** the AI writes less code and leans on proven human-written libraries, so the output is expected, production-grade, and human-crafted.

### Production-Grade Non-Negotiables (apply in every mode; intensity scales per mode)

- **Type safety:** Strict TypeScript; no `any` leakage to boundaries; typed request/response contracts.
- **Validate all inputs:** Zod schemas for request bodies, query params, path params, AND environment variables (e.g., `@t3-oss/env` or `zod`). Never trust raw client input.
- **Centralized error handling:** a shared error envelope with machine-readable codes and human messages; no raw stack traces to clients; correct, consistent HTTP status codes.
- **Structured logging:** Pino (or equivalent) with request-ID/trace correlation; never log secrets, tokens, or PII.
- **Config/secrets:** validated env config + a committed `.env.example`; never hardcode credentials or secrets into code.
- **Security baseline:** helmet-style headers, correct CORS config (never `*` on authenticated APIs), rate limiting (required for Production-SaaS), input sanitization, dependency audit notes (`npm audit`).
- **Reliability:** graceful shutdown, explicit timeouts on outbound calls, idempotency for risky writes, pagination on all collections, typed entity models + migrations.
- **Testing baseline:** at least unit tests for critical logic and integration tests against a test DB for core flows; strict `eslint`/`prettier`; CI-ready scripts.
- **Operational readiness:** health-check endpoint, structured response envelope consistency, clear `README` with run/migration/test commands.

### Per-Mode Rigor Table

| Concern | CRUD/MVP | Production-SaaS | BFF/API | Internal |
|---------|----------|-----------------|---------|----------|
| Input validation (Zod) | Required | Required | Required | Required |
| Centralized error envelope | Required | Required | Required | Required |
| Structured logging + request IDs | Basics | Full | Full | Moderate |
| Env validation + `.env.example` | Required | Required | Required | Required |
| Security headers + CORS | Required | Required | Required | Required |
| Rate limiting | Optional | Required | Required | Optional |
| Auth/RBAC | Simple | Full | Session/edge | Minimal/token |
| Tests (unit + integration) | Optional | Required | Required | Recommended |
| Migrations | Required | Required | Required | Required |
| Graceful shutdown / timeouts | Required | Required | Required | Required |

### Anti-AI-Backend-Tell Checklist (NEVER ship in any mode)

Audit your output against every item before presenting it.

- [ ] No single throwaway `app.listen` with no error handling or graceful shutdown.
- [ ] No unhandled raw `req.body` straight into the database without validation.
- [ ] No `res.status(500).send('error')` scattered everywhere instead of a centralized error handler + envelope.
- [ ] No hardcoded DB creds, API keys, or magic strings in source; always via env + `.env.example`.
- [ ] No `any`-everywhere, no missing response contracts.
- [ ] No `CORS: *` on an authenticated API and no `helmet`.
- [ ] No empty `catch {}` blocks swallowing errors silently.
- [ ] No `console.log`-only logging with no request correlation.
- [ ] No copy-paste tutorial scaffold with no project-specific intent-driven adaptation.
- [ ] No hand-rolled reimplementation of a concern that a mature library covers (Library-First violation).
- [ ] No missing env validation, no missing migrations, no missing test seed/DB strategy.

### Popular Backend Library Kit (use these; don't reinvent)

- **Validation:** Zod, with `@t3-oss/env` for env vars (do not hand-validate).
- **ORM/migrations:** Prisma, Drizzle (+ Drizzle Kit migrations).
- **Logging:** Pino (structured, low overhead).
- **Security:** helmet, express-rate-limit / rate-limit middleware.
- **Auth/JWT:** jose, jsonwebtoken, lucia; bcrypt/argon2 for hashing.
- **IDs/pagination:** UUID via `crypto.randomUUID()`/`uuid`; cursor helper from ORM where possible.
- **Queues/jobs:** BullMQ + Redis.
- **API docs/typing:** zod-openapi or OpenAPI generation (Fastify Swagger, orval), tRPC for full-stack.
- **Files/upload:** multer or framework-native; object storage SDKs (S3/GCS).
- **Email:** Resend / Nodemailer / the SES/Postmark SDK.

### Uniqueness Rule (every backend differs from every other backend)

No two backends the agent produces may read like the same template. Structure must derive from intent + explicit user input:

- Deliberately vary and record these decisions per project: folder/module layout, module boundaries, error-envelope shape and naming, auth flow design, endpoint/module naming, validation strategy, database modeling approach, config layout.
- Derive choices from the user's stated intent and answered questions. If no preference, pick the combination that best serves the product — and say why.
- End each build with *"Why this backend is structured for this project:"* + bullets tying decisions to the specific product/framework.

### Output Contract

Every delivered backend must summarize:

1. **Backend type/mode + why** (CRUD/MVP, Production-SaaS, BFF/API, Internal).
2. **Intent analysis summary** (serves what, for whom, intended rigor).
3. **Stack + libraries chosen + why**, and where custom code was written because no library fit.
4. **Endpoints/resource inventory** with validation + auth contracts.
5. **Security & ops notes**: env sample (`.env.example` fields), migrations, run/test commands, health-check.
6. **Anti-AI-tell self-check** — confirm each checklist item passes.
7. **Uniqueness statement** — why this structure fits this project.
