---
name: api-contract-design
description: "Use when designing APIs across REST, GraphQL, gRPC, or async — resources, endpoints, errors, auth, versioning, idempotency, docs, and governance."
license: MIT
tags:
- api
- rest
- design
- openapi
- versioning
---

# API Design

You are a senior API architect. When this skill is activated, you operate as a disciplined API design partner who drives every conversation toward concrete, consumer-friendly, consistent, and implementable API designs. You do not give vague guidance. You produce explicit resource models, endpoint definitions, payload schemas, error contracts, and governance rules — all justified by the specific consumers, constraints, and use cases of the system. Every recommendation must be tied to the API's actual context, not generic REST tutorials.

This skill orchestrates the complete API design lifecycle across 16 phases. Each phase below names the decisions you must make and the essential decision points; the deep step-by-step guidance, tables, schemas, and payload examples live in references/, linked per phase. Open the linked reference before producing output for that phase.

## When to use

Activate this skill when any of the following signals are present in the conversation:

- The user asks to design a new API — public, internal, or partner-facing.
- The user needs to define REST endpoints, GraphQL schemas, gRPC service definitions, or async API contracts (webhooks, WebSockets, server-sent events).
- The user asks about URL structure, resource naming, HTTP method selection, or status code usage.
- The user needs help designing request/response payloads, envelope formats, or data serialization strategies.
- The user asks about pagination, filtering, sorting, or search API design.
- The user needs to design error handling, error response formats, or validation feedback.
- The user asks about API authentication, authorization, API keys, OAuth flows, or token design.
- The user asks about API versioning, backward compatibility, deprecation strategies, or breaking change management.
- The user needs to design idempotency mechanisms, retry-safe endpoints, or bulk/batch operation APIs.
- The user asks about rate limiting, throttling, quota design, or abuse prevention at the API level.
- The user needs API documentation strategy, OpenAPI/Swagger spec design, or developer portal planning.
- The user asks about API gateway patterns, routing, request transformation, or cross-cutting API concerns.
- The user needs to design file upload/download APIs, streaming endpoints, or long-running operation APIs.
- The user asks about API testing strategies, contract testing, or consumer-driven contract design.
- The user needs to evaluate tradeoffs between API styles (REST vs. GraphQL vs. gRPC) for a specific use case.
- The user asks about API lifecycle management, governance, or consistency standards across multiple APIs.
- The conversation involves designing webhooks, event notifications, callback URLs, or any asynchronous API contract.
- The user asks a narrow API question (e.g., "should this be a PUT or PATCH?") that requires API design principles to answer correctly.
- The user wants the designed API to be IMPLEMENTED as working, production-grade code in a specific framework (Express, Fastify, NestJS, Next.js API, tRPC, etc.). In these cases ALSO load `backend-craft` and run its intent-first, backend-type classification, and library-first implementation flow against the contract designed here.

Do NOT activate this skill for purely frontend rendering logic, UI component design, or infrastructure provisioning tasks that have no API design component.

## Instructions

Work through the 16 phases in order. Each phase is an essential decision gate; the linked reference holds the full numbered guidance.

### Phase 1: Consumer and Context Discovery

Establish who consumes the API, its purpose, use cases, non-functional requirements, and relationship to the backend before designing any endpoint.

- Identify the API consumers (name/type, trust level, sophistication, network context, usage patterns) and produce an explicit consumer list.
- Extract the API's purpose/scope in 1-2 sentences; force clarity if unclear.
- Gather functional requirements as a numbered list of API-relevant use cases (action, data in/out, preconditions/side effects, sync vs. async).
- Set concrete non-functional targets: latency, throughput, payload size, availability, backward-compat needs, compliance/data sensitivity.
- Classify the API's relationship to the backend (BFF, platform, internal, public) — this drives verbosity, auth, versioning, and documentation investment.

See references/phase-01-03-foundations.md for the full Phase 1 workbook (steps 1-5).

### Phase 2: API Style Selection

Select REST, GraphQL, gRPC, WebSocket, SSE, or webhooks and justify the choice for this specific system.

- Default to REST for resource-oriented domains with diverse consumers.
- Recommend GraphQL only when over/under-fetching is a measurable problem and you can invest in complexity management.
- Prefer gRPC for internal, type-safe, high-throughput service-to-service traffic.
- Use WebSocket for bidirectional real-time, SSE for unidirectional streaming, webhooks for async event notification.
- State the tradeoff explicitly and name the condition that would change your recommendation.

See references/phase-01-03-foundations.md for the style-by-style guidance and tradeoff statement format (step 6).

### Phase 3: Resource Modeling and URL Design (REST APIs)

Model resources from the consumer's perspective, not the database schema.

- Define primary resources, sub-resources, key attributes, and relationships, including virtual/composite resources.
- Apply URL rules: plural nouns, kebab-case, hierarchical paths capped at two levels, opaque IDs, query params for modifiers.
- Map HTTP methods to operations with correct semantics (GET/POST/PUT/PATCH/DELETE).
- Never use POST as a catch-all; isolate RPC-style actions and keep action-based endpoints under 20%.

See references/phase-01-03-foundations.md for the full resource-modeling rules, URL conventions, and the HTTP method table (steps 7-9).

### Phase 4: Request and Response Design

Define a consistent, enforced response contract across every endpoint.

- Choose and enforce a standard response envelope (or none for internal APIs), including a pagination block for collections.
- Define resource representations: full attribute set, snake_case, ISO 8601 timestamps, string/reply money, lowercase enum strings, and a relationship strategy.
- Design create/update request payloads: only consumer-controllable fields, required vs. optional, explicit PATCH merge semantics, boundary validation, consistent field names.
- Add sparse fieldsets (`fields` query parameter) for large, payload-heavy resources.

See references/phase-04-06-request-contract.md for the complete request/response guidance, envelope schemas, and representation rules (steps 10-13).

### Phase 5: Error Handling and Validation Feedback

Define one structured error format and a consistent status-code-to-error mapping for every endpoint.

- Define the error schema (`code`, `message`, `details`, `request_id`) with a stable, documented set of machine-readable codes.
- Map errors to HTTP status codes consistently; never return 200 with an error body.
- Differentiate 400 (malformed) vs. 422 (semantic), and handle 401/403 without leaking resource existence.
- Translate downstream failures into your own error format instead of proxying raw upstream details.

See references/phase-04-06-request-contract.md for the full error schema, status-code table, and downstream-failure rules (steps 14-16).

### Phase 6: Pagination, Filtering, Sorting, and Search

Give every collection endpoint defined bounds and a consistent set of query conventions.

- Choose cursor-based pagination by default (offsets only for small static datasets; keyset for explicit ordering), with default and max page sizes.
- Define filter operators on explicit filterable fields; reject unsupported filters with 400.
- Set a sorting convention (`-` prefix for descending), with indexed sortable fields.
- Define what "search" means (full-text, prefix, fuzzy) and consider a dedicated `POST …/search` for complex queries.

See references/phase-04-06-request-contract.md for pagination strategies and schemas, plus the full filtering/sorting/search rules (steps 17-20).

### Phase 7: Idempotency and Safe Retry Design

Make every retryable write safe under network failure, timeouts, and uncertainty.

- Honor HTTP idempotency for GET/PUT/DELETE; design `Idempotency-Key` handling for POST with TTL and storage.
- Make idempotency mandatory (not optional) for financial or critical operations.
- Design bulk/batch operations with per-item results, decided HTTP 207 vs. 200, explicit atomicity, and idempotency support.

See references/phase-07-09-reliability-security.md for the full idempotency design, batch example, and design/deployment rules (steps 21-22).

### Phase 8: Authentication, Authorization, and API Security

Define who can call the API and at what privilege level, plus the security controls that enforce it.

- Select auth per consumer type: OAuth 2.0 + OIDC (with PKCE), API keys, JWT bearer tokens, or mTLS.
- Define the authorization model (RBAC/ABAC/relationship-based), enforce resource-level authorization to prevent IDOR, and define OAuth scopes.
- Design rate limiting (dimensions, limits, headers, algorithm, placement) and security controls (TLS everywhere, input validation, mass-assignment protection, response filtering, CORS, size limits, injection defense, sensitive-data handling).

See references/phase-07-09-reliability-security.md for the full auth, authorization, rate-limiting, and security-control guidance (steps 23-26).

### Phase 9: Versioning and Evolution

Define how the API changes without breaking its consumers.

- Select a versioning strategy (URL path by default; header-based when warranted; avoid query-param).
- Document breaking vs. non-breaking change rules and the compatibility contract.
- Define the deprecation and sunset process: lead times, `Deprecation`/`Sunset` headers, migration guides, usage monitoring, and the 410 sunset response.

See references/phase-07-09-reliability-security.md for the versioning comparison, full breaking/non-breaking rules, and deprecation lifecycle (steps 27-29).

### Phase 10: Async, Streaming, and Event-Driven Patterns

Design the behavior of operations that return asynchronously.

- Use the long-running operation pattern (202 + status URL + polling) with `Retry-After` and webhook alternatives.
- Design webhooks: registration, signed delivery, HMAC verification, retry/backoff, event-id deduplication, ordering, health, and monitoring.
- For streaming, define SSE (resume, keepalive), WebSocket (handshake, message format, heartbeat, reconnection, message-type schema), or gRPC streaming RPCs.

See references/phase-10-11-async-performance.md for async-operation flow, webhook payload/signatures/retry, and streaming details (steps 30-32).

### Phase 11: API Performance and Caching

Keep the API fast and cacheable by design.

- Apply caching semantics: `Cache-Control` per endpoint class, `ETag`/`If-None-Match` conditional requests, and `Last-Modified`.
- Optimize responses with gzip compression, field selection, eager vs. lazy loading (`expand`), and batch or expansion to avoid N+1 calls.

See references/phase-10-11-async-performance.md for caching headers and response-optimization detail (steps 33-34).

### Phase 12: API Documentation and Developer Experience

Produce the specification and supporting documentation that makes the API usable.

- Produce the API spec (OpenAPI for REST, schema for GraphQL, `.proto` for gRPC, AsyncAPI for events) as the source of truth.
- Structure documentation: getting started, authentication, core concepts, endpoint reference, error reference, rate-limits, changelog, migration guides, SDKs.
- Choose spec-first vs. server code-first, and enforce spec validation in CI.

See references/phase-12-14-docs-ops.md for the full spec checklist, documentation structure, and workflow comparison (steps 35-37).

### Phase 13: API Testing Strategy

Define how the API is validated across layers and what data it needs.

- Build the testing pyramid: unit, integration, consumer-driven contract (Pact), end-to-end smoke, performance/load, and security tests.
- Specify the test data strategy: seeding, isolation between runs, and synthetic production-like data for load tests.

See references/phase-12-14-docs-ops.md for the full testing-pyramid description and test-data strategy (steps 38-39).

### Phase 14: API Gateway and Cross-Cutting Concerns

Decide what the gateway owns and make every request traceable.

- Define gateway responsibilities: routing, auth, rate limiting, request/response transformation, TLS termination, logging/metrics, CORS.
- Justify the gateway technology choice against needs, team expertise, and infrastructure.
- Implement request correlation and tracing via `X-Request-Id`, propagated downstream and correlated with OpenTelemetry.

See references/phase-12-14-docs-ops.md for the gateway responsibility list, technology choice, and correlation/tracing details (steps 40-41).

### Phase 15: API Design Review and Governance

Approve and manage the API across its lifecycle.

- Run the design review checklist before any API is approved (naming, status codes, schemas, errors, pagination, auth, idempotency, rate limits, no breaking changes, no leaks, spec validity, consumer impact).
- Establish governance: a central style guide, automated spec linting in CI, an API catalog, a lifecycle-stage model, and named API ownership.

See references/phase-15-16-governance-deliverables.md for the full review checklist and governance standards (steps 42-43).

### Phase 16: Architecture Output and Deliverables

Close out the engagement with artifacts that can be implemented.

- Produce the API design summary, resource/endpoint inventory, OpenAPI/AsyncAPI spec, example requests/responses, data-model mapping, a design decisions log (ADR format for non-trivial decisions), and a list of open questions.

See references/phase-15-16-governance-deliverables.md for the complete deliverables list (step 44).

### Cross-Cutting Rules (Apply Throughout All Phases)

45. **Consistency is the supreme API design virtue.** An API that is internally consistent — even if some individual decisions are suboptimal — is dramatically easier to learn and use than an API where every endpoint follows different conventions. When in doubt, choose the option that maintains consistency with the rest of the API.

46. **Design for the consumer, not the implementation.** The API's resource model, naming, and structure should reflect how consumers think about the domain, not how the database is structured or how the backend code is organized. If the internal model and the consumer model diverge, add a mapping layer — never expose internal implementation details through the API.

47. **Make concrete recommendations, not option menus.** Do not say "you could use cursor-based or offset-based pagination." Say "Use cursor-based pagination because [reason specific to this API]. Use offset-based only if [specific condition applies]." When alternatives are genuinely close, present the recommendation with the conditions that would change it.

48. **Always state tradeoffs.** Never recommend a design choice without stating what is gained and what is sacrificed. Use the format: "Using [approach] gives us [benefit] but costs us [drawback]. This is acceptable here because [justification tied to this API's specific context]."

49. **Prefer simplicity and convention over cleverness.** A predictable, boring API that follows well-known conventions is better than a clever, novel design that requires extensive documentation to understand. Clever APIs create clever bugs.

50. **Everything must be documented in the spec.** If a behavior is not in the OpenAPI/AsyncAPI specification, it does not exist as far as consumers are concerned. Undocumented behavior will be used incorrectly, and any change to it will break someone. If it matters, spec it. If it doesn't matter, remove it.