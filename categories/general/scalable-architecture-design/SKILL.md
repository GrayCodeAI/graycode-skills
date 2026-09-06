---
name: scalable-architecture-design
description: "Designs scalable distributed systems: workload analysis, bottleneck identification, load balancing, caching, sharding, auto-scaling, and load testing for large-scale traffic."
license: MIT
tags:
- scalability
- distributed-systems
- performance
- caching
- load-balancing
---

# Skills

## When to use

Activate this skill when any of the following situations, signals, or requests are detected:

- A user asks how to scale a system, service, application, or infrastructure component to handle more users, traffic, requests, or data.
- A user describes performance degradation, high latency, timeout errors, resource exhaustion, or capacity concerns in an existing system.
- A user requests a review or critique of an existing architecture for scalability readiness or bottleneck identification.
- A user is designing a new system and wants guidance on making it scalable from the start (greenfield scalability design).
- A user asks about load balancing, caching, sharding, replication, partitioning, CDN strategies, message queues, or event-driven architectures in the context of handling growth.
- A user needs to plan for anticipated traffic spikes, seasonal load patterns, viral growth, or migration from monolith to distributed architecture.
- A user asks about auto-scaling policies, cloud-native scaling, container orchestration scaling, or serverless scaling strategies.
- A user wants to understand tradeoffs (CAP theorem, consistency vs. availability, cost vs. performance, latency vs. throughput) for a system under scale.
- A user requests a scalability test plan, load testing strategy, or performance benchmarking approach.
- A user needs documentation, architecture decision records, or rationale for scalability choices made in a system design.
- A system design discussion involves any combination of: high concurrency, large datasets, real-time processing, geo-distribution, multi-tenancy, or rapid user growth.

If the request touches scalability, performance under load, distributed system design, or capacity planning in any meaningful way, activate this skill and follow the full instruction sequence below, adapting depth and scope to the specificity of the user's request.

## Instructions

### Phase 1: Workload Discovery and Requirements Gathering

1. **Extract the system context.** Before proposing any solution, systematically gather or infer the following about the system under discussion. If the user has not provided these details, ask targeted clarifying questions. Do not guess critical parameters—ask.

   - **System purpose and domain:** What does the system do? (e-commerce platform, real-time chat, IoT data pipeline, SaaS application, API gateway, etc.)
   - **Current scale indicators:** Approximate number of users, requests per second (RPS), data volume, storage size, and number of services or components.
   - **Growth projections:** Expected growth rate (e.g., 10x users in 12 months, 50x data in 3 years). If unknown, help the user estimate by asking about business goals.
   - **Traffic patterns:** Is traffic steady-state, bursty, diurnal, seasonal, event-driven, or unpredictable? Identify peak-to-average ratios.
   - **Latency and throughput requirements:** What are the acceptable response times (p50, p95, p99)? What throughput must the system sustain at peak?
   - **Data characteristics:** Read-heavy vs. write-heavy workloads, data freshness requirements, hot vs. cold data ratios, data retention policies.
   - **Consistency requirements:** Does the system need strong consistency, eventual consistency, or can different components have different consistency models?
   - **Availability targets:** What is the target uptime SLA (99.9%, 99.99%)? What is the acceptable recovery time objective (RTO) and recovery point objective (RPO)?
   - **Existing technology stack:** Languages, frameworks, databases, cloud providers, container orchestration, CI/CD pipelines, monitoring tools already in use.
   - **Budget and operational constraints:** Cost sensitivity, team size and expertise, regulatory or compliance constraints, data residency requirements.

2. **Classify the workload type.** Based on gathered information, categorize the workload into one or more of the following archetypes, as this drives all downstream architecture decisions:

   - **Request-Response (synchronous):** REST/GraphQL APIs, web applications, mobile backends.
   - **Real-Time Streaming:** Live dashboards, chat systems, collaborative editing, gaming.
   - **Batch Processing:** ETL pipelines, report generation, ML model training.
   - **Event-Driven:** Order processing, notification systems, IoT ingestion, workflow orchestration.
   - **Mixed / Hybrid:** Combinations of the above (most real-world systems).

3. **Identify the primary scaling dimension.** Determine whether the core scaling challenge is:
   - **Compute-bound:** CPU-intensive processing, complex business logic, ML inference.
   - **I/O-bound:** Database queries, external API calls, file system operations.
   - **Memory-bound:** Large in-memory datasets, session state, caching.
   - **Network-bound:** High fan-out, large payload transfer, cross-region communication.
   - **Storage-bound:** Rapidly growing datasets, high write throughput, large binary objects.

### Phase 2: Current Architecture Analysis and Bottleneck Identification

4. **Map the current architecture.** If an existing system is being scaled, reconstruct or confirm the current architecture by identifying:
   - All services, components, and their responsibilities.
   - Communication patterns between components (synchronous HTTP, gRPC, async messaging, shared databases).
   - Data stores and their roles (primary database, read replicas, caches, search indices, object storage, data warehouses).
   - External dependencies (third-party APIs, payment gateways, identity providers).
   - Infrastructure topology (single server, multi-server, multi-region, cloud provider specifics).

5. **Perform systematic bottleneck analysis.** Walk through every layer of the system and identify actual or likely bottlenecks using the following checklist:

   **Application Layer Bottlenecks:**
   - Single-threaded or blocking request processing.
   - Inefficient algorithms or data structures (O(n²) operations on growing datasets).
   - Memory leaks or excessive garbage collection pauses.
   - Synchronous calls to slow downstream services creating cascading latency.
   - Lack of connection pooling to databases or external services.
   - Monolithic deployment preventing independent scaling of hot components.
   - Session affinity or sticky state preventing horizontal scaling.

   **Database Layer Bottlenecks:**
   - Single database instance handling all reads and writes.
   - Missing or inefficient indexes causing full table scans on growing tables.
   - Write contention from row-level or table-level locks.
   - N+1 query patterns or excessive join complexity.
   - Connection pool exhaustion under concurrent load.
   - Unbounded table growth without archival or partitioning.
   - Cross-shard or cross-partition queries in distributed databases.

   **Infrastructure Layer Bottlenecks:**
   - Single points of failure (single load balancer, single DNS entry, single availability zone).
   - Insufficient CPU, memory, or network bandwidth on provisioned instances.
   - Disk I/O saturation (especially with spinning disks or unoptimized EBS volumes).
   - Network bandwidth limits between services, between availability zones, or to the internet.
   - DNS resolution bottlenecks or TTL misconfigurations.
   - Missing or misconfigured auto-scaling policies causing slow reaction to traffic changes.

   **External Dependency Bottlenecks:**
   - Rate-limited third-party APIs without retry/backoff/circuit-breaking.
   - Synchronous dependency on slow or unreliable external services in the critical path.

6. **Quantify bottleneck severity.** For each identified bottleneck, estimate:
   - At what scale does it become critical? (e.g., "database write throughput saturates at 5,000 writes/sec")
   - What is the blast radius? (e.g., "if the cache goes down, database load increases 20x and the entire system degrades")
   - What is the effort to resolve? (quick fix, moderate refactor, major re-architecture)
   - Rank bottlenecks by: **(severity of impact) × (likelihood of hitting scale threshold) / (effort to resolve)**

### Phase 3: Scalable Architecture Design

7. **Establish foundational architecture principles.** Before selecting specific technologies, explicitly state the architectural principles that will govern the design:

   - **Statelessness:** Application services must not store session or request state locally. All state must be externalized to dedicated state stores (databases, caches, object storage). This enables any instance to handle any request and allows free horizontal scaling.
   - **Loose Coupling:** Services communicate through well-defined interfaces (APIs, message contracts). Changes to one service must not require changes to other services. Loose coupling enables independent scaling, deployment, and failure isolation.
   - **Idempotency:** All write operations and message handlers must be idempotent. In distributed systems, retries are inevitable; idempotency prevents duplicate side effects.
   - **Graceful Degradation:** When a component is overloaded or unavailable, the system must degrade gracefully rather than fail catastrophically. Define what "degraded mode" looks like for each critical user journey.
   - **Design for Failure:** Assume every component can and will fail. Design retry logic, circuit breakers, timeouts, fallback responses, and bulkheads into every inter-service communication path.

8. **Design the service architecture.** Based on the workload classification and bottleneck analysis, design or refactor the service architecture:

   **For Monolith-to-Distributed Migration:**
   - Identify bounded contexts using domain-driven design principles.
   - Prioritize extraction of the component that is the scaling bottleneck (not the easiest one to extract).
   - Use the Strangler Fig pattern: route traffic to the new service for the extracted capability while the monolith still handles everything else.
   - Establish an API gateway or BFF (Backend for Frontend) layer to abstract internal service topology from clients.
   - Define service communication contracts (OpenAPI specs, protobuf schemas, AsyncAPI for event contracts).

   **For Greenfield Distributed Systems:**
   - Decompose by business capability, not by technical layer.
   - Keep services small enough to be owned by a single team but large enough to avoid excessive inter-service communication overhead.
   - Define synchronous (request-response) vs. asynchronous (event-based) communication for each interaction. Default to asynchronous unless the caller needs an immediate response.
   - Design each service to be independently deployable and scalable.

   **For All Architectures:**
   - Identify the critical path (the sequence of operations that determines end-to-end latency for the most important user action) and optimize it relentlessly.
   - Move non-critical work off the critical path using asynchronous processing (e.g., sending confirmation emails, updating analytics, generating thumbnails).

9. **Design the load balancing and traffic distribution strategy.** Select and configure load balancing at every layer:

   - **DNS-Level:** Use weighted DNS (Route 53, Cloud DNS) for geo-routing and multi-region failover. Set appropriate TTLs (low TTLs for failover scenarios, higher for stable routing).
   - **Edge/CDN Level:** Place a CDN (CloudFront, Cloudflare, Fastly, Akamai) in front of all static assets, and evaluate whole-page or API response caching for read-heavy, cacheable endpoints. Configure cache invalidation strategies (TTL-based, purge-on-write, stale-while-revalidate).
   - **Application Load Balancer Level:** Use Layer 7 load balancers (ALB, Envoy, NGINX, HAProxy) to distribute requests across application instances. Choose the load balancing algorithm based on workload:
     - Round Robin: when all instances are homogeneous and requests are uniform cost.
     - Least Connections: when request processing times vary significantly.
     - Weighted: when instances have different capacities.
     - Consistent Hashing: when request affinity to a specific instance improves cache hit rates (but design the system to work correctly without affinity).
   - **Service Mesh Level (if applicable):** For complex microservices, consider a service mesh (Istio, Linkerd) for transparent load balancing, retries, circuit breaking, and observability between services.
   - **Database Level:** Use read replicas with a connection proxy (PgBouncer, ProxySQL, Amazon RDS Proxy) to distribute read traffic. Route writes to the primary.

10. **Design the caching strategy.** Implement a multi-layer caching architecture, being explicit about what is cached, where, for how long, and how it is invalidated:

    - **Client-Side Caching:** HTTP cache headers (Cache-Control, ETag, Last-Modified) for browser and mobile client caching. Specify max-age, stale-while-revalidate, and private vs. public directives.
    - **CDN/Edge Caching:** Cache static assets aggressively (long TTL with cache-busting via content hashing in filenames). Cache API responses where appropriate with shorter TTLs and Vary headers.
    - **Application-Level Caching (Local):** In-process caches (Caffeine for JVM, lru-cache for Node.js, functools.lru_cache for Python) for small, frequently accessed, rarely changing data (e.g., feature flags, configuration). Be aware of cache coherence issues across multiple application instances.
    - **Distributed Caching (Remote):** Use Redis or Memcached for shared cached data across application instances. Design the cache interaction pattern:
      - **Cache-Aside (Lazy Loading):** Application checks cache first, on miss reads from database, writes result to cache. Best for read-heavy workloads with tolerant staleness.
      - **Write-Through:** Application writes to cache and database simultaneously. Ensures cache is always up to date but adds write latency.
      - **Write-Behind (Write-Back):** Application writes to cache, cache asynchronously writes to database. Best throughput but risk of data loss if cache fails before persisting.
      - **Read-Through:** Cache itself is responsible for loading data from the database on miss. Simplifies application code.
    - **Cache Invalidation Strategy:** This is the hardest part. Choose one:
      - **TTL-Based Expiration:** Simple, predictable, but data can be stale for up to TTL duration.
      - **Event-Based Invalidation:** When data changes, publish an event that triggers cache deletion/update. More complex but fresher data.
      - **Versioned Keys:** Include a version number in cache keys; increment version on data change. Old cached data naturally expires.
    - **Cache Sizing and Eviction:** Estimate working set size. Provision cache memory at 1.5-2x working set. Use LRU or LFU eviction. Monitor hit rate; target >95% for hot-path caches.
    - **Cache Stampede Prevention:** Implement locking (e.g., Redis SETNX) or probabilistic early expiration to prevent thundering herd when a popular cache key expires.

11. **Design the database scaling strategy.** Based on data characteristics and access patterns, design the appropriate database scaling approach:

    **Read Scaling:**
    - Deploy read replicas (PostgreSQL streaming replication, MySQL replication, MongoDB secondaries).
    - Route read queries to replicas using a connection proxy or application-level routing.
    - Accept and design for replication lag (eventual consistency on reads). Implement read-your-own-writes consistency where needed (route user's reads to primary for N seconds after a write).

    **Write Scaling:**
    - **Vertical Scaling First:** Before sharding, ensure the database instance is optimally sized and tuned (connection limits, buffer pool, WAL settings, query optimization).
    - **Functional Partitioning:** Split different tables/domains into separate database instances (e.g., user data in one database, order data in another). This is simpler than sharding and should be tried first.
    - **Horizontal Sharding:** When a single table exceeds the capacity of one instance:
      - Choose a shard key carefully. It must: (a) distribute data evenly, (b) distribute writes evenly, (c) allow most queries to target a single shard. Common shard keys: user_id, tenant_id, geographic region.
      - Avoid shard keys that create hotspots (e.g., timestamp-based keys concentrate recent writes on one shard).
      - Plan for re-sharding. Use consistent hashing or virtual shards (many logical shards mapped to fewer physical nodes) to make adding shards less disruptive.
      - Accept that cross-shard queries are expensive. Design the data model to minimize them.
    - **Consider purpose-built databases for specific access patterns:**
      - Time-series data → TimescaleDB, InfluxDB, or Amazon Timestream.
      - Full-text search → Elasticsearch or OpenSearch.
      - Graph relationships → Neo4j or Amazon Neptune.
      - High-velocity key-value access → DynamoDB, Cassandra, or ScyllaDB.
      - Analytics/OLAP → ClickHouse, BigQuery, Redshift, or Snowflake.

    **Data Partitioning (within a single database):**
    - Use table partitioning (range, list, or hash partitioning) for large tables. Partition by time for time-series data (enables efficient partition pruning and archival).
    - Implement data lifecycle management: archive old data to cold storage, delete expired data, compress historical partitions.

12. **Design asynchronous processing and event-driven architecture.** For work that does not need to be on the synchronous critical path:

    - **Message Queues (point-to-point):** Use RabbitMQ, Amazon SQS, or similar for task distribution where each message should be processed by exactly one consumer. Design for at-least-once delivery and idempotent consumers.
    - **Event Streaming (pub-sub with replay):** Use Apache Kafka, Amazon Kinesis, or Redpanda for event-driven architectures where:
      - Multiple consumers need to process the same event independently.
      - Event replay capability is needed (new consumers can read historical events).
      - Event ordering within a partition/shard is important.
      - High throughput (millions of events/sec) is required.
    - **Design event schemas carefully.** Use a schema registry (Confluent Schema Registry, AWS Glue). Version schemas. Prefer backward-compatible evolution (adding optional fields).
    - **Handle backpressure.** When producers outpace consumers:
      - Scale consumers horizontally (add more consumer instances, increase partition count).
      - Implement dead-letter queues for messages that repeatedly fail processing.
      - Monitor consumer lag and alert when it exceeds thresholds.
    - **Saga Pattern for distributed transactions:** When a business operation spans multiple services, use choreography-based sagas (each service reacts to events) or orchestration-based sagas (a central coordinator manages the workflow). Implement compensating transactions for rollback.

13. **Design auto-scaling strategies.** Configure auto-scaling for every scalable component:

    - **Compute Auto-Scaling (VMs/Containers):**
      - Define scaling metrics: CPU utilization, memory utilization, request count, queue depth, custom application metrics (e.g., request latency p99).
      - Set scale-out thresholds aggressively (e.g., scale out at 60% CPU) and scale-in thresholds conservatively (e.g., scale in at 30% CPU) to avoid flapping.
      - Configure cooldown periods to prevent rapid oscillation.
      - Use predictive scaling for predictable traffic patterns (e.g., scale up before the daily traffic peak).
      - Pre-warm instances: ensure new instances are ready to receive traffic quickly (pre-loaded caches, warm JVM, pre-established connection pools).
    - **Database Auto-Scaling:**
      - Use auto-scaling read replicas (Aurora Auto Scaling, DynamoDB auto-scaling for read/write capacity).
      - For serverless databases (Aurora Serverless, DynamoDB on-demand), understand the cold-start and throttling characteristics.
    - **Queue/Stream Consumer Auto-Scaling:**
      - Scale consumers based on queue depth or consumer lag, not CPU. Use KEDA (Kubernetes Event-Driven Autoscaling) for Kubernetes environments.
    - **Cost Guardrails:** Set maximum instance counts and spending alerts. Use spot/preemptible instances for fault-tolerant workloads (batch processing, stateless workers) to reduce costs by 60-90%.

14. **Design for resilience under high load.** Ensure the system degrades gracefully rather than collapsing under extreme load:

    - **Rate Limiting:** Implement rate limiting at the API gateway level (per user, per API key, per IP). Use token bucket or sliding window algorithms. Return HTTP 429 with Retry-After header.
    - **Circuit Breakers:** Implement circuit breakers (Hystrix pattern, Resilience4j, Polly) on all calls to downstream services and databases. Define open/half-open/closed states with appropriate thresholds and recovery timers.
    - **Bulkheads:** Isolate critical resources. Use separate thread pools or connection pools for different downstream services so that slowness in one dependency does not exhaust resources needed for others.
    - **Timeouts:** Set explicit timeouts on every network call. Calculate timeout budgets: if the end-to-end SLA is 500ms and there are 3 sequential service calls, each gets ~150ms (with margin).
    - **Backpressure and Load Shedding:** When the system is at capacity, reject excess requests early (at the load balancer or API gateway) rather than accepting them and degrading performance for all requests. Implement priority queues to ensure high-value requests are processed first.
    - **Graceful Degradation Playbook:** Define what features can be disabled under extreme load (e.g., disable recommendation engine, serve cached search results, show simplified product pages). Implement feature flags to enable/disable these dynamically.

15. **Evaluate CAP and consistency tradeoffs explicitly.** For every data store and inter-service interaction, explicitly document the chosen tradeoff:

    - State whether the component prioritizes CP (consistency + partition tolerance) or AP (availability + partition tolerance).
    - For AP systems, define the staleness window that is acceptable (e.g., "product inventory can be stale for up to 5 seconds; over-selling is handled by compensating transactions").
    - For CP systems, acknowledge the availability cost and design clients to handle unavailability gracefully (retries, cached fallback responses).
    - Apply the PACELC framework where useful: "During Partition, choose A or C; Else (normal operation), choose Latency or Consistency."

### Phase 4: Performance Monitoring and Scalability Validation

16. **Design the observability strategy.** Ensure the system has comprehensive monitoring to detect scalability issues before they become outages:

    - **Metrics (numeric time-series data):**
      - Infrastructure: CPU, memory, disk I/O, network I/O per instance.
      - Application: Request rate, error rate, latency distribution (p50, p95, p99), active connections, thread pool utilization.
      - Business: Orders per minute, sign-ups per hour, active users.
      - Database: Query latency, connection pool utilization, replication lag, lock wait time, cache hit ratio.
      - Queue: Queue depth, consumer lag, processing rate, dead-letter queue size.
      - Use Prometheus + Grafana, Datadog, New Relic, or CloudWatch. Define dashboards for each layer.
    - **Distributed Tracing:** Implement OpenTelemetry or Jaeger to trace requests across service boundaries. Use trace data to identify the slowest service in the critical path and optimize it.
    - **Structured Logging:** Use structured JSON logs with correlation IDs. Aggregate in ELK stack, Loki, or CloudWatch Logs Insights. Log at appropriate levels: errors always, warnings for degradation, info for business events, debug only when diagnosing issues.
    - **Alerting:** Define alerts based on SLO burn rates (e.g., "error budget consumed 10% in the last hour" rather than "error rate > 1%"). Page on symptoms (user-facing impact), not causes (high CPU). Use PagerDuty, OpsGenie, or equivalent.

17. **Design the load testing and scalability validation strategy.** Validate the architecture can handle target scale before real traffic arrives:

    - **Load Testing Types:**
      - **Baseline Test:** Establish current performance at normal traffic levels.
      - **Stress Test:** Gradually increase load until the system breaks. Identify the breaking point and the failure mode.
      - **Spike Test:** Simulate sudden traffic spikes (e.g., 10x normal in 60 seconds). Validate auto-scaling response time.
      - **Soak Test:** Run at sustained high load (e.g., 80% of peak) for 12-24 hours. Detect memory leaks, connection leaks, and gradual degradation.
      - **Chaos Test:** Randomly kill instances, introduce network latency, and simulate dependency failures during load tests. Validate resilience.
    - **Tools:** Recommend appropriate tools: k6, Gatling, Locust, JMeter, or Artillery for load generation. Use distributed load generation to avoid bottlenecking the test client itself.
    - **Test Environment:** Test against a production-like environment. If cost-prohibitive, test against a proportionally scaled-down environment and extrapolate carefully, noting the limitations.
    - **Key Metrics to Capture During Tests:** Latency percentiles (not averages), error rates, throughput ceiling, resource utilization at each tier, auto-scaling reaction time, and recovery time after load decreases.

### Phase 5: Structured Output and Documentation

18. **Produce a structured scalability architecture document.** Organize all findings and recommendations into a clear, actionable document with the following sections:

    - **Executive Summary:** One paragraph summarizing the key scalability challenge, the proposed approach, and the expected outcome.
    - **Current State Assessment:** Architecture diagram (described textually or in diagram notation), identified bottlenecks ranked by severity, current capacity limits.
    - **Target State Architecture:** Proposed architecture with all scaling mechanisms described, technology choices with explicit rationale for each choice (why this technology over alternatives), architecture diagram of the target state.
    - **Scaling Strategy by Component:** For each major component (API layer, each service, each database, cache, queue, CDN), specify: current capacity, scaling mechanism (horizontal/vertical/auto), scaling limits, and estimated cost at target scale.
    - **Tradeoff Decisions:** Explicitly document every significant tradeoff made (consistency vs. availability, cost vs. performance, simplicity vs. optimal performance) with rationale.
    - **Migration Plan (if applicable):** Ordered list of changes from current state to target state, with each step being independently deployable and rollback-safe. Prioritize changes by impact-to-effort ratio.
    - **Risk Register:** Identify remaining scalability risks after implementing the proposed changes, with mitigation strategies.
    - **Validation Plan:** Specific load tests to run, with target metrics that constitute success.
    - **Cost Estimate:** Estimated infrastructure cost at current scale, target scale, and 3x target scale. Identify cost optimization opportunities (reserved instances, spot instances, right-sizing, storage tiering).

19. **Provide implementation-ready recommendations.** For each recommendation, include:
    - **What** to do (specific, unambiguous action).
    - **Why** it matters (which bottleneck or risk it addresses).
    - **How** to implement it (specific technologies, configurations, code patterns).
    - **Priority** (P0: do immediately, P1: do before next growth milestone, P2: do when capacity allows).
    - **Estimated effort** (hours/days/weeks).
    - **Validation criteria** (how to confirm the change achieved the desired effect).

20. **Iterate based on feedback.** After presenting the scalability architecture:
    - Ask the user if any constraints were missed or assumptions were incorrect.
    - Refine recommendations based on feedback about budget, team capabilities, timeline, or technology preferences.
    - Offer to deep-dive into any specific component (e.g., "Would you like me to detail the Redis cluster configuration and failover strategy?" or "Should I design the Kafka topic partitioning strategy in detail?").
    - If the user provides new information about actual production metrics or load test results, re-evaluate bottleneck rankings and adjust recommendations accordingly.
