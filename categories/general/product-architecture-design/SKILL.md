---
name: product-architecture-design
description: "Use when designing or reviewing system architecture; guides requirements discovery, component decomposition, API contracts, scalability, reliability, and architecture decision records."
license: MIT
tags:
- system-design
- architecture
- scalability
- reliability
- api-design
---

# Skills

This skill serves as the AI agent's comprehensive framework for tackling any product architecture challenge. It provides a sequential, decision-driven workflow that transforms ambiguous product needs into well-reasoned, documented system architectures. The agent should treat each step as a mandatory checkpoint, producing concrete artifacts before advancing.

## When to use

Activate this skill when any of the following conditions are detected:

- A user asks for help designing a new system, platform, product, or service from scratch.
- A user requests a review, critique, or improvement of an existing system architecture.
- A user needs help decomposing a monolithic system into services or modules.
- A user asks about component design, service boundaries, API design, or integration patterns.
- A user poses questions about scalability, reliability, fault tolerance, or performance planning for a system.
- A user wants to evaluate tradeoffs between architectural approaches (e.g., monolith vs. microservices, SQL vs. NoSQL, synchronous vs. asynchronous communication).
- A user asks for an Architecture Decision Record (ADR), technical design document, or system design diagram description.
- A user describes a product idea, set of features, or business problem and expects a technical architecture recommendation.
- A user asks how to evolve, migrate, or modernize an existing architecture.
- A conversation involves terms such as "system design," "architecture," "tech stack," "infrastructure," "service boundary," "data model," "API contract," "high availability," "disaster recovery," "capacity planning," or similar architectural language.

Do NOT activate this skill for pure code-level implementation questions (e.g., "fix this function"), UX/UI-only design discussions with no backend implications, or project management/process questions with no architectural dimension.

## Instructions

### Phase 1 — Requirement Discovery and Problem Framing

1. **Clarify the scope and intent.** Before designing anything, explicitly determine what the user is asking for. Ask yourself (and the user, if ambiguous): Is this a greenfield design, a redesign, an extension, or a review of an existing system? State the scope clearly in one sentence before proceeding.

2. **Extract and enumerate functional requirements.** List every discrete capability the system must provide. Use the user's language but restructure it into a numbered list of concrete feature statements. Each statement should follow the pattern: *"The system must allow [actor] to [action] so that [outcome]."* If the user has not provided enough detail, ask targeted clarifying questions — never assume critical functionality.

3. **Extract and enumerate non-functional requirements.** For each of the following dimensions, either extract an explicit constraint from the user or state a reasonable default assumption and flag it as an assumption:
   - **Expected scale:** Number of users, requests per second, data volume, growth rate.
   - **Latency targets:** p50, p95, p99 response times for critical paths.
   - **Availability target:** e.g., 99.9%, 99.99%. Translate to allowable downtime.
   - **Data durability and consistency model:** Strong consistency, eventual consistency, or mixed.
   - **Security and compliance:** Authentication, authorization, encryption, regulatory constraints (GDPR, HIPAA, SOC 2, etc.).
   - **Budget and team constraints:** Cloud spend limits, team size, existing expertise.
   - **Deployment environment:** Cloud provider preferences, on-prem, hybrid, edge.
   - **Integration constraints:** Existing systems, third-party services, legacy dependencies.

4. **Identify key user journeys and critical paths.** Select the 3–5 most important end-to-end workflows (e.g., "user signs up → places first order → receives confirmation"). These will drive the architecture's primary design priorities. Rank them by business criticality.

5. **State explicit assumptions and constraints.** Consolidate all assumptions made during discovery into a single, numbered list. This list becomes a living contract — if any assumption is wrong, the architecture may need revision. Present this list to the user for validation before proceeding.

### Phase 2 — High-Level Architecture Design

6. **Select an architectural style with justification.** Based on the requirements gathered, choose the primary architectural pattern. Evaluate at minimum the following candidates and provide a brief rationale for selecting or rejecting each:
   - Modular monolith
   - Microservices
   - Service-oriented architecture (SOA)
   - Event-driven architecture
   - Serverless / function-as-a-service
   - Hybrid approaches
   
   State the chosen style and the top three reasons it fits the requirements. Acknowledge the top two risks of this choice.

7. **Define the system boundary.** Draw a clear line between what is inside the system and what is external. List all external actors (users, third-party services, partner systems, infrastructure services) and their interaction points. This establishes the system context.

8. **Decompose into top-level components or services.** Identify the major building blocks of the system. For each component, provide:
   - **Name:** A clear, intention-revealing name.
   - **Responsibility:** A single-sentence statement of what this component owns (apply the Single Responsibility Principle at the service level).
   - **Ownership boundary:** What data does this component exclusively own?
   - **Key interfaces:** What does it expose and what does it consume?
   
   Use domain-driven design principles: look for bounded contexts by identifying areas of the domain with distinct language, rules, and data. Services should align with bounded contexts, not with technical layers.

9. **Map critical user journeys onto the component architecture.** For each critical path identified in Step 4, trace the request flow through the components. Document the sequence: which component handles each step, what data flows between them, and where state changes occur. This is your architecture's "proof of correctness" — if a journey cannot be cleanly traced, the decomposition needs revision.

10. **Design the data architecture.** For each component that owns data:
    - Choose the storage technology (relational DB, document store, key-value store, search index, object storage, etc.) and justify the choice against the access patterns.
    - Define the core data entities and their relationships at a conceptual level (not full schema — just entity names, key attributes, and cardinality).
    - Specify the consistency model: strong, eventual, or causal. Justify against the business requirement.
    - Define the data partitioning strategy if the scale demands it (shard key selection, partition scheme).
    - Address cross-service data access: no shared databases. Define how services query each other's data (API calls, event-carried state transfer, CQRS read models).

### Phase 3 — Interface and Integration Design

11. **Design API contracts for inter-component communication.** For each interface identified in Step 8:
    - Specify the communication style: synchronous (REST, gRPC) or asynchronous (message queue, event stream).
    - For synchronous APIs: define resource names, HTTP methods (or RPC methods), request/response shapes (key fields, not exhaustive schemas), and error handling patterns.
    - For asynchronous interfaces: define event/message names, payload shapes, the broker/transport (Kafka, SQS, RabbitMQ, etc.), and consumer group strategies.
    - Apply the principle: use synchronous communication for queries and commands where the caller needs an immediate answer; use asynchronous communication for notifications, eventual state propagation, and workload decoupling.

12. **Design external integration points.** For each third-party system or external dependency:
    - Define the integration pattern (direct API call, webhook, file transfer, SDK, etc.).
    - Identify the failure modes and design the fallback strategy (circuit breaker, retry with backoff, graceful degradation, local cache).
    - Specify the contract ownership: who defines the schema? How will breaking changes be handled?

13. **Design the authentication and authorization architecture.** Define:
    - Identity provider and authentication protocol (OAuth 2.0, OIDC, SAML, API keys, mTLS for service-to-service).
    - Authorization model (RBAC, ABAC, policy engine like OPA).
    - Token propagation strategy across service boundaries.
    - Secret management approach (vault, cloud KMS, environment injection).

### Phase 4 — Scalability, Reliability, and Operational Readiness

14. **Design the scalability strategy.** For each component, determine:
    - **Scaling axis:** Horizontal (add instances), vertical (add resources), or data partitioning.
    - **Statelessness:** Is the component stateless? If stateful, how is state externalized or replicated?
    - **Bottleneck analysis:** Identify the most likely bottleneck for each critical path (CPU, memory, I/O, network, external dependency). Propose the mitigation (caching layer, read replicas, connection pooling, CDN, async offload).
    - **Auto-scaling triggers:** Define the metric and threshold that should trigger scaling (CPU > 70%, queue depth > 1000, p99 latency > 500ms, etc.).
    - **Caching strategy:** Identify what should be cached, where (client, CDN, application, distributed cache), TTL policies, and cache invalidation approach.

15. **Design the reliability and fault tolerance strategy.** Address each of the following:
    - **Redundancy:** Multi-AZ, multi-region, or single-region with justification. Define the blast radius of a single failure.
    - **Failure isolation:** Bulkheads between services, circuit breakers on outbound calls, timeouts on all network calls (specify default timeout values).
    - **Data backup and recovery:** Backup frequency, retention period, recovery time objective (RTO), recovery point objective (RPO).
    - **Graceful degradation:** For each critical path, define what happens when a downstream dependency is unavailable. The system should never return a blank screen or unhandled error to the user.
    - **Health checks and readiness probes:** Define what "healthy" means for each component.
    - **Idempotency:** All write operations and message consumers must be idempotent. Specify the idempotency key strategy.

16. **Design the observability stack.** Define the three pillars:
    - **Logging:** Structured logging format, correlation ID propagation, log levels, and aggregation destination.
    - **Metrics:** Key business and infrastructure metrics for each component. Define SLIs (Service Level Indicators) and SLOs (Service Level Objectives) for critical paths.
    - **Tracing:** Distributed tracing strategy, trace sampling rate, and trace context propagation.
    - **Alerting:** For each SLO, define the alerting rule, severity, and escalation path.

17. **Plan the deployment and release strategy.** Define:
    - CI/CD pipeline structure: build → test → stage → production.
    - Deployment strategy: rolling update, blue/green, canary, or feature flags. Justify the choice.
    - Infrastructure-as-code approach (Terraform, Pulumi, CloudFormation, etc.).
    - Environment parity: how staging mirrors production.
    - Rollback procedure: automated or manual, time-to-rollback target.

### Phase 5 — Tradeoff Evaluation and Decision Documentation

18. **Enumerate and evaluate architectural tradeoffs.** For every significant decision made in the preceding steps, explicitly document the tradeoff using this structure:
    - **Decision:** What was decided.
    - **Alternatives considered:** At least two alternatives.
    - **Tradeoff dimensions:** Evaluate each option against complexity, performance, cost, team expertise, time-to-market, operational burden, and future flexibility.
    - **Decision rationale:** Why the chosen option wins on the dimensions that matter most for this product.
    - **Reversal cost:** How hard is it to change this decision later? (Low / Medium / High). Prefer decisions with low reversal cost when options are otherwise comparable.

19. **Identify technical debt and deferred decisions.** List any shortcuts, temporary solutions, or decisions deliberately deferred. For each, state:
    - What was deferred and why.
    - The trigger condition for revisiting (e.g., "revisit when traffic exceeds 10K RPS").
    - The risk of deferral.

20. **Produce an Architecture Decision Record (ADR) for each major decision.** Use this template for each ADR:
    ```
    # ADR-[number]: [Title]
    ## Status: [Proposed | Accepted | Deprecated | Superseded]
    ## Context: What is the problem or situation?
    ## Decision: What is the change we are making?
    ## Consequences: What are the positive, negative, and neutral outcomes?
    ```

### Phase 6 — Architecture Deliverable Assembly

21. **Compose the final architecture document.** Organize all outputs from the preceding steps into a structured deliverable with these sections:
    1. **Executive Summary** — One-paragraph overview of the system and the architectural approach.
    2. **Requirements Summary** — Functional requirements, non-functional requirements, assumptions, and constraints (from Steps 2–5).
    3. **System Context Diagram Description** — Textual description of the system boundary and external actors (from Step 7). If possible, suggest a diagram using Mermaid or PlantUML syntax.
    4. **Component Architecture** — Component inventory with responsibilities, data ownership, and interfaces (from Steps 8–10). Suggest a component/container diagram.
    5. **Data Architecture** — Storage technologies, entity models, consistency models, partitioning (from Step 10).
    6. **Interface Contracts** — API and event specifications (from Steps 11–12).
    7. **Security Architecture** — Auth, authz, secrets management (from Step 13).
    8. **Scalability and Performance Plan** — Scaling strategies, caching, bottleneck mitigations (from Step 14).
    9. **Reliability and Operations Plan** — Fault tolerance, observability, deployment (from Steps 15–17).
    10. **Architectural Decisions and Tradeoffs** — ADRs and tradeoff analyses (from Steps 18–20).
    11. **Open Questions and Next Steps** — Unresolved items, deferred decisions, recommended follow-ups.

22. **Adapt the depth and format to the user's need.** Not every request requires all 21 preceding steps at full depth. Apply these guidelines:
    - **Quick consultation** (user asks a focused question, e.g., "should I use Kafka or SQS?"): Jump to Step 18 (tradeoff evaluation) and deliver a concise tradeoff analysis. Reference the relevant requirement dimensions.
    - **Component-level design** (user asks about a specific service or module): Execute Steps 1–5 scoped to that component, then Steps 8–17 for that component only.
    - **Full system design** (user asks for a complete architecture): Execute all steps sequentially, producing the full deliverable from Step 21.
    - **Architecture review** (user presents an existing design): Map the existing design onto the framework, identify gaps against each step, and provide a prioritized list of recommendations.
    
    Always state which depth level you are operating at and why.

23. **Maintain an iterative mindset.** Architecture is never done in one pass. After delivering the initial architecture:
    - Invite the user to challenge any decision.
    - Be prepared to re-enter any phase when new information surfaces.
    - When revising, trace the impact of the change through all downstream steps (e.g., changing the consistency model in Step 10 may affect the reliability strategy in Step 15 and create a new ADR in Step 20).
    - Version the architecture: clearly mark what changed between iterations.
