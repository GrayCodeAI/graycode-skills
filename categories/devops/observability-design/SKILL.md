---
name: observability-design
description: "Designs monitoring and observability: metrics, SLI/SLO/error budgets, distributed tracing, logging, alerting, dashboards, and incident detection for distributed systems."
license: MIT
tags:
- monitoring
- observability
- alerting
- tracing
- slo
---

# Skills

This skill serves as the AI agent's end-to-end framework for monitoring and observability architecture. It activates whenever the agent must reason about system visibility, operational health, alerting, metrics design, log aggregation, distributed tracing, or any task that requires understanding how systems are observed, measured, and kept reliable. The agent follows a structured, phased approach—moving from discovery through design, implementation guidance, and documentation—producing actionable, production-grade monitoring strategies.

## When to use

Activate this skill when any of the following situations, requests, or contextual signals are present:

- A user asks for help designing a monitoring or observability strategy for a new or existing system.
- A user needs to define SLIs, SLOs, or error budgets for one or more services.
- A user requests guidance on alerting thresholds, alert fatigue reduction, or incident detection rules.
- A user asks how to implement distributed tracing across microservices.
- A user needs a centralized logging architecture or log aggregation strategy.
- A user wants to design dashboards or operational visibility views.
- A user is troubleshooting blind spots, missing signals, or gaps in existing monitoring.
- A user asks about monitoring cloud-native infrastructure (Kubernetes, serverless, managed services, containers).
- A user needs to integrate monitoring with incident response, on-call workflows, or runbooks.
- A user asks about anomaly detection, proactive alerting, or predictive monitoring.
- A user wants to evaluate, compare, or select monitoring tools and platforms.
- A user requests a monitoring audit, review, or maturity assessment of their current setup.
- A user needs monitoring considerations for a migration, new deployment, or architectural change.
- A user asks about observability across multiple environments (development, staging, production).
- A user needs to ensure monitoring systems themselves are scalable and performant.
- Any conversation involves reliability engineering, operational visibility, or production readiness from a monitoring perspective.

When activated, always execute the phases below in order, adapting depth and detail to the scope of the request. For narrowly scoped questions, compress phases but never skip the reasoning structure.

## Instructions

### Phase 1 — System Discovery and Context Acquisition

1. **Gather system context explicitly.** Before producing any monitoring recommendation, ask for or extract the following. Do not assume what is not stated:
   - What type of system is being monitored (monolith, microservices, serverless, hybrid, data pipeline, event-driven, etc.).
   - The technology stack: languages, frameworks, databases, message brokers, caches, CDNs, API gateways, load balancers.
   - The deployment environment: cloud provider(s), on-premises, Kubernetes, ECS, VMs, serverless platforms, edge.
   - The number and names of services, their ownership, and team boundaries.
   - Existing monitoring tools already in use (Prometheus, Grafana, Datadog, New Relic, CloudWatch, OpenTelemetry, ELK, Splunk, Jaeger, Tempo, PagerDuty, OpsGenie, etc.).
   - Current pain points: alert fatigue, blind spots, slow incident detection, missing traces, log noise, cost concerns.
   - Compliance, regulatory, or data residency requirements affecting telemetry data.
   - Scale indicators: requests per second, number of pods/instances, data volume, user base size.

2. **Map the system architecture.** Produce or request a logical architecture map that identifies:
   - All services and their responsibilities.
   - Synchronous dependencies (HTTP/gRPC calls between services).
   - Asynchronous dependencies (message queues, event buses, streaming platforms).
   - External dependencies (third-party APIs, SaaS integrations, DNS, payment providers).
   - Data stores and their access patterns (read-heavy, write-heavy, mixed).
   - Entry points (public APIs, webhooks, scheduled jobs, user interfaces).
   - Critical paths: the request flows that, if degraded, directly impact end-user experience or revenue.

3. **Identify operational risks and failure modes.** For each component and dependency, explicitly enumerate:
   - What can fail (network partition, resource exhaustion, dependency timeout, data corruption, deployment regression).
   - What degradation looks like (increased latency, partial failures, error spikes, queue backlog growth).
   - What the blast radius is (single user, single tenant, entire service, cascading cross-service failure).
   - Historical incidents if known, and what signals were missing when they occurred.

4. **Classify components by criticality.** Assign each service and dependency a criticality tier:
   - **Tier 1 — Critical:** Direct user-facing, revenue-impacting, or safety-critical. Requires real-time monitoring, aggressive alerting, and full tracing.
   - **Tier 2 — Important:** Supports critical paths indirectly. Requires comprehensive monitoring and timely alerting.
   - **Tier 3 — Standard:** Internal tooling, batch jobs, non-user-facing services. Requires baseline monitoring and trend alerting.
   - **Tier 4 — Best-effort:** Development utilities, experimental services. Requires minimal monitoring.

Document this classification explicitly. It drives every subsequent monitoring decision.

---

### Phase 2 — Metrics Strategy Design

5. **Define the golden signals for every Tier 1 and Tier 2 service.** For each service, specify concrete metrics across the four golden signals:
   - **Latency:** Measure request duration at p50, p90, p95, and p99. Separate successful request latency from error request latency. Specify the measurement point (client-side, server-side, or both). Define latency by endpoint or operation when granularity matters.
   - **Traffic:** Measure request rate (requests per second), broken down by endpoint, method, and response status class. For asynchronous systems, measure message throughput, consumption rate, and publish rate.
   - **Errors:** Measure error rate as a percentage of total requests. Classify errors by type (HTTP 5xx vs 4xx, application exceptions, timeout errors, circuit breaker trips). Track both explicit errors (error responses) and implicit errors (successful responses with wrong data, slow responses treated as errors by callers).
   - **Saturation:** Measure resource utilization: CPU, memory, disk I/O, network bandwidth, file descriptors, thread pool usage, connection pool usage, queue depth, and any resource with a hard limit. Identify the resource most likely to be exhausted first (the bottleneck resource).

6. **Define RED and USE metrics where applicable.**
   - For request-driven services, apply RED (Rate, Errors, Duration) at every service boundary.
   - For infrastructure and resource-oriented components, apply USE (Utilization, Saturation, Errors) for every significant resource (CPU, memory, disk, network interfaces, GPU if applicable).

7. **Design custom business and application metrics.** Beyond infrastructure signals, identify domain-specific metrics that reflect business health:
   - Examples: orders processed per minute, payment success rate, login failure rate, search result relevance scores, cart abandonment signals, data pipeline lag, ML model inference latency, feature flag evaluation counts.
   - These metrics must be tied to specific business outcomes or user experience indicators.
   - Specify the instrumentation point: application code, middleware, proxy, or synthetic monitoring.

8. **Specify metric instrumentation standards.**
   - Define the naming convention for metrics (e.g., `service_name.operation.metric_type.unit`, following OpenTelemetry semantic conventions or Prometheus naming best practices).
   - Define standard labels/tags: `service`, `environment`, `region`, `version`, `endpoint`, `status_code`, `error_type`. Warn against high-cardinality labels (user IDs, request IDs, full URLs) on metrics.
   - Specify the collection method: pull-based (Prometheus scraping) vs. push-based (StatsD, OTLP export), and justify the choice for the given architecture.
   - Define metric resolution: 10-second intervals for Tier 1 services, 30–60 seconds for Tier 2, 60+ seconds for Tier 3.

---

### Phase 3 — SLI / SLO / Error Budget Framework

9. **Define Service-Level Indicators (SLIs) for each critical user journey.** SLIs must be:
   - Expressed as a ratio: (good events / total events) × 100%.
   - Tied to a specific user-facing operation or critical system function, not to an internal infrastructure metric.
   - Measurable from the perspective closest to the user (load balancer logs, API gateway metrics, client-side telemetry, or synthetic monitors).
   - Examples:
     - Availability SLI: Proportion of HTTP requests that return a non-5xx response.
     - Latency SLI: Proportion of HTTP requests served in under 300ms (measured at the load balancer).
     - Correctness SLI: Proportion of data pipeline runs that produce output matching validation checksums.
     - Freshness SLI: Proportion of time that the data in a dashboard is less than 5 minutes old.

10. **Set Service-Level Objectives (SLOs) for each SLI.**
    - Express each SLO as a target percentage over a rolling window (e.g., 99.9% of requests succeed over a 30-day rolling window).
    - Choose the SLO target based on: user expectations, business impact of violations, engineering capacity to maintain the target, and the SLO targets of downstream dependencies.
    - Calculate the implied error budget: for a 99.9% SLO over 30 days, the error budget is approximately 43.2 minutes of total downtime or 0.1% of requests.
    - Document what happens when the error budget is consumed: feature freeze, mandatory reliability work, incident review triggers.

11. **Design SLO burn-rate alerting.** Replace static threshold alerts on SLIs with multi-window burn-rate alerts:
    - **Fast burn (critical):** Alert when 2% of the 30-day error budget is consumed in 1 hour (burn rate ~14.4x). Use a short window (5 min) confirmed by a longer window (1 hour). This catches severe outages.
    - **Medium burn (warning):** Alert when 5% of the error budget is consumed in 6 hours (burn rate ~6x). Use a short window (30 min) confirmed by a longer window (6 hours). This catches sustained degradation.
    - **Slow burn (ticket):** Alert when 10% of the error budget is consumed in 3 days (burn rate ~1x). This catches slow leaks. Route to a ticket, not a page.
    - Document the exact PromQL, LogQL, or platform-specific query for each burn-rate alert.

---

### Phase 4 — Distributed Tracing Design

12. **Design the tracing architecture.**
    - Select the tracing protocol and format: prefer OpenTelemetry (OTLP) as the standard. Specify whether to use W3C TraceContext or B3 propagation headers.
    - Identify every service boundary where trace context must be propagated: HTTP calls, gRPC calls, message queue publish/consume, database calls, cache lookups, external API calls.
    - Specify the tracing backend: Jaeger, Tempo, Zipkin, X-Ray, Datadog APT, Honeycomb, or a vendor-managed solution. Justify based on scale, cost, query needs, and existing tooling.

13. **Define the instrumentation plan.**
    - For each service, specify whether instrumentation is automatic (agent/SDK auto-instrumentation) or manual (code-level span creation).
    - List the spans that must be created manually for business-critical operations (e.g., payment processing, order fulfillment steps, ML inference calls).
    - Define span attributes that must be attached: `user.id` (if allowed), `tenant.id`, `order.id`, `feature.flag`, `deployment.version`, `db.statement` (sanitized), `http.route`, `error.message`.
    - Specify which attributes are indexed for search and which are stored but not indexed (to control costs).

14. **Design the sampling strategy.**
    - **Head-based sampling:** Define the base sampling rate (e.g., sample 10% of traces). Use adaptive sampling to increase the rate for low-traffic services and decrease for high-traffic services.
    - **Tail-based sampling:** If supported by the backend, configure tail-based sampling to always retain: traces with errors, traces exceeding a latency threshold (e.g., p99), traces for specific operations (payment, authentication), and a random baseline sample.
    - **Always-sample rules:** Certain operations (health checks, readiness probes) should never be sampled. Certain operations (admin actions, security events) should always be sampled at 100%.
    - Document the expected trace volume and storage cost implications of the sampling strategy.

15. **Define trace-to-log and trace-to-metric correlation.**
    - Ensure every log line emitted during a traced request includes the `trace_id` and `span_id`.
    - Ensure exemplars are attached to metrics (e.g., Prometheus exemplars linking a histogram bucket to a specific trace_id).
    - Verify that dashboards and alerting UIs allow one-click navigation from a metric spike → exemplar trace → individual spans → correlated logs.

---

### Phase 5 — Centralized Logging Strategy

16. **Design the log aggregation architecture.**
    - Specify the log pipeline: collection agent (Fluentd, Fluent Bit, Vector, Filebeat, OpenTelemetry Collector) → transport (Kafka, direct push) → processing/enrichment → storage backend (Elasticsearch, Loki, CloudWatch Logs, Splunk, BigQuery).
    - Justify each component choice based on: log volume (GB/day), query patterns (full-text search vs. label-based filtering), retention requirements, cost constraints, and team familiarity.
    - Design for resilience: buffering at the agent level, dead-letter queues for failed log delivery, backpressure handling.

17. **Define structured logging standards.**
    - All logs must be structured (JSON). No unstructured free-text logs in production.
    - Define the mandatory fields for every log line:
      - `timestamp` (ISO 8601, UTC)
      - `level` (DEBUG, INFO, WARN, ERROR, FATAL)
      - `service` (service name)
      - `environment` (dev, staging, production)
      - `trace_id` (when in a traced context)
      - `span_id` (when in a traced context)
      - `message` (human-readable description)
      - `error.type`, `error.message`, `error.stack` (when logging errors)
    - Define optional contextual fields: `user.id`, `tenant.id`, `request.id`, `http.method`, `http.path`, `http.status_code`, `duration_ms`.
    - Prohibit logging sensitive data: passwords, tokens, credit card numbers, PII (unless masked/hashed and compliant with data policies).

18. **Define log levels and their usage rules.**
    - **DEBUG:** Detailed diagnostic information. Disabled in production by default. Enable dynamically per-service for troubleshooting.
    - **INFO:** Significant business events and state transitions (service started, order placed, deployment completed). Not for per-request logging in high-traffic services.
    - **WARN:** Unexpected conditions that are handled but indicate potential problems (retry succeeded, cache miss fallback, approaching resource limit).
    - **ERROR:** Unhandled failures requiring attention (unrecoverable exception, dependency timeout after all retries, data integrity violation).
    - **FATAL:** The service is unable to continue operating and will shut down.

19. **Design log retention and lifecycle policies.**
    - Hot storage (fast query): 7–14 days for production, 3 days for staging.
    - Warm storage (slower query, lower cost): 30–90 days.
    - Cold/archive storage (compliance, forensics): 1–7 years based on regulatory requirements.
    - Define index/rotation policies to prevent storage cost explosion.
    - Implement log volume monitoring: alert if log volume spikes unexpectedly (possible log storm, debug logging left on, retry loop).

---

### Phase 6 — Alerting Strategy and Incident Detection

20. **Design the alerting hierarchy.** Every alert must be categorized:
    - **Page (Critical):** Requires immediate human response. Only for conditions that are actively impacting users or will imminently impact users. Must be routed to an on-call responder via PagerDuty, OpsGenie, or equivalent. Target: fewer than 5 unique paging alert types per service. Each paging alert must have a runbook.
    - **Warning (Urgent ticket):** Requires attention within hours. Routed to a team channel and a ticket system. Examples: error budget burn rate approaching threshold, disk usage above 80%, certificate expiring in 14 days.
    - **Informational (Notification):** Awareness only. Routed to a monitoring channel. Examples: deployment completed, autoscaler activated, config change detected.

21. **Apply alert quality principles rigorously.**
    - Every alert must be **actionable**: if a human receives it, there must be a clear action they can take. If no action exists, it is not an alert—it is a dashboard metric.
    - Every alert must be **relevant**: it must correspond to actual or imminent user impact. Alerts on internal metrics with no user-facing consequence must be eliminated or downgraded.
    - Every alert must have **low false-positive rate**: use appropriate evaluation windows (avoid 1-minute windows for noisy metrics), use `for` durations (alert must fire continuously for N minutes before triggering), use rate-of-change rather than absolute thresholds where appropriate.
    - Every alert must be **documented** with: description, severity, likely cause, immediate remediation steps (runbook link), escalation path, and dashboard link.

22. **Define specific alerting rules for common failure patterns.** Provide concrete alert definitions (with example PromQL/query syntax) for:
    - **Error rate spike:** `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01` sustained for 5 minutes.
    - **Latency degradation:** `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2.0` sustained for 10 minutes.
    - **Resource saturation:** `container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.9` sustained for 5 minutes.
    - **Dependency failure:** Circuit breaker open state, or error rate to a specific downstream service exceeding threshold.
    - **Queue backlog growth:** Consumer lag increasing over 3 consecutive evaluation windows.
    - **Certificate/credential expiry:** Days until expiration < 14 (warning), < 3 (critical).
    - **Deployment regression:** Error rate increase of >2x within 15 minutes of a deployment event (correlated via deployment annotations).

23. **Design alert routing and escalation.**
    - Map each alert to an owning team based on service ownership.
    - Define escalation timers: if a page is not acknowledged within 5 minutes, escalate to secondary on-call. If not acknowledged within 15 minutes, escalate to engineering manager.
    - Define alert suppression and grouping rules: group related alerts for the same incident into a single notification. Suppress downstream dependency alerts when the root dependency is already alerting (dependency-aware alerting).
    - Define maintenance window policies: suppress alerts during planned maintenance with automatic re-enablement.

---

### Phase 7 — Dashboard and Visualization Design

24. **Design a dashboard hierarchy with clear audiences and purposes.**
    - **Executive / Business Dashboard:** High-level system health. Shows: overall availability (SLO status), key business metrics (transactions/sec, revenue flow), active incidents, error budget remaining. Updated every 1–5 minutes. Audience: leadership, product managers.
    - **Service Overview Dashboard (one per Tier 1/2 service):** Golden signals for the service (latency percentiles, request rate, error rate, saturation). SLO burn-rate visualization. Dependency health status. Recent deployments annotated on time series. Audience: service-owning team.
    - **Infrastructure Dashboard:** Kubernetes cluster health (node status, pod restarts, resource allocation vs. usage, HPA activity). Cloud resource health (RDS, ElastiCache, load balancers, Lambda concurrency). Network metrics (inter-service latency, DNS resolution time, packet loss). Audience: platform/infrastructure team.
    - **Incident Investigation Dashboard:** Deep-dive views with high-resolution metrics, log panels, trace search, and error breakdowns. Pre-filtered by service and time range. Audience: on-call engineers during incidents.
    - **On-Call Handoff Dashboard:** Summary of the last 24 hours: alerts fired, incidents opened/resolved, error budget consumption, pending action items. Audience: incoming on-call engineer.

25. **Apply dashboard design best practices.**
    - Use consistent time ranges across all panels within a dashboard. Support variable-based filtering (service, environment, region, version).
    - Place the most critical signals (SLO status, error rate) in the top-left of every dashboard (highest visual priority).
    - Use color semantically: green = healthy, yellow = warning, red = critical. Do not use color as the only indicator (support colorblind users with icons/text).
    - Include annotations for deployments, config changes, scaling events, and incidents on time-series graphs.
    - Avoid dashboard sprawl: each dashboard must have a stated purpose and audience. Review dashboards quarterly; archive unused ones.

---

### Phase 8 — Cloud Infrastructure and Container Monitoring

26. **Design Kubernetes-specific monitoring** (when applicable).
    - **Cluster level:** Node readiness, node resource usage, cluster autoscaler events, etcd health, API server latency and error rates, scheduler queue depth.
    - **Workload level:** Pod restart counts (alert on restart loops), container OOMKill events, pod scheduling failures, CrashLoopBackOff detection, init container failures.
    - **Resource management:** Requests vs. limits vs. actual usage for CPU and memory. Detect resource over-provisioning (wasted cost) and under-provisioning (risk of OOM/throttling).
    - **Networking:** Service mesh metrics (Istio, Linkerd): request success rate, latency between services, mTLS certificate health. Ingress controller metrics: request rate, error rate, connection counts.
    - **Storage:** PersistentVolume usage and IOPS. Alert on PV usage > 85%.

27. **Design cloud-managed service monitoring** (when applicable).
    - For every managed service (RDS, DynamoDB, S3, SQS, Lambda, Cloud Functions, Pub/Sub, etc.), identify the vendor-provided metrics that matter most and supplement with custom metrics where vendor metrics are insufficient.
    - Examples:
      - **RDS/Aurora:** CPU, FreeableMemory, ReadIOPS, WriteIOPS, ReplicaLag, DatabaseConnections vs. max_connections, DiskQueueDepth.
      - **SQS/Pub/Sub:** ApproximateNumberOfMessagesVisible (queue depth), ApproximateAgeOfOldestMessage (consumer lag), NumberOfMessagesSent vs. NumberOfMessagesReceived.
      - **Lambda/Cloud Functions:** Invocation count, error count, duration, throttles, concurrent executions, cold start frequency.
    - Configure CloudWatch/Cloud Monitoring metric exports to the centralized monitoring platform to avoid tool fragmentation.

28. **Design synthetic monitoring and external probes.**
    - Implement synthetic checks (e.g., using Checkly, Pingdom, CloudWatch Synthetics, or custom probes) for:
      - Critical API endpoints: health checks and key user-journey endpoints tested every 1–5 minutes from multiple geographic regions.
      - DNS resolution time and correctness.
      - TLS certificate validity and expiration.
      - Third-party dependency availability (payment gateway, identity provider, CDN).
    - Synthetic results feed into the SLI calculation for availability and latency.

---

### Phase 9 — Cross-Environment Observability

29. **Ensure monitoring parity across environments with appropriate differentiation.**
    - **Production:** Full monitoring, alerting, tracing (with sampling), logging at INFO level, SLO tracking. All Tier 1/2 services fully instrumented.
    - **Staging:** Near-production monitoring fidelity. Alerting active but routed to a staging channel (no pages). Used to validate monitoring configurations before production deployment.
    - **Development:** Minimal alerting. Full tracing (100% sampling at low volume) to support debugging. Log level DEBUG enabled. Monitoring of CI/CD pipeline health.
    - Use environment-specific label/tag values (`env=production`, `env=staging`) on all telemetry. Ensure dashboards and alerts filter by environment by default.
    - Validate that every monitoring change (new alert, new dashboard, new metric) is deployed to staging first and verified before production rollout.

30. **Design monitoring-as-code practices.**
    - All alert rules, dashboard definitions, SLO configurations, and recording rules must be stored in version control (Git).
    - Use infrastructure-as-code tools: Terraform for monitoring resources (Datadog monitors, CloudWatch alarms), Jsonnet/Grafonnet for Grafana dashboards, PrometheusRule CRDs for Kubernetes-based alerting.
    - Implement CI/CD for monitoring configuration: linting, validation, automated deployment to staging then production.
    - Require peer review for alert and SLO changes just as for application code.

---

### Phase 10 — Anomaly Detection and Proactive Monitoring

31. **Design anomaly detection for signals where static thresholds are insufficient.**
    - Identify metrics with strong seasonality (traffic patterns that vary by hour/day/week) where static thresholds cause false positives during low-traffic periods and miss issues during high-traffic periods.
    - Implement baseline anomaly detection: use rolling averages, standard deviation bands, or platform-native anomaly detection (Datadog anomaly monitors, CloudWatch Anomaly Detection, Prometheus recording rules for dynamic thresholds).
    - Apply anomaly detection to: request rate (traffic anomalies), error rate deviations from baseline, latency shifts, resource usage patterns, and log volume.
    - Always pair anomaly detection alerts with static threshold alerts as a safety net. Anomaly detection is complementary, not a replacement.

32. **Design capacity planning and trend-based alerting.**
    - Implement forecasting for resources with predictable growth: disk usage, database size, connection pool exhaustion, certificate expiration.
    - Alert on projected exhaustion: "At current growth rate, disk will be full in 7 days" rather than "disk is 90% full."
    - Use linear regression or exponential smoothing on weekly metric data to project resource exhaustion dates.
    - Feed capacity projections into quarterly planning processes.

---

### Phase 11 — Incident Response Integration

33. **Integrate monitoring with the incident response workflow.**
    - Every paging alert must automatically create an incident in the incident management platform (PagerDuty, OpsGenie, Incident.io, FireHydrant).
    - Every alert notification must include: a direct link to the relevant dashboard, a link to the runbook, the current metric values, the threshold that was breached, and the impacted service/SLO.
    - Define automated diagnostics that trigger when specific alerts fire: collect thread dumps, capture heap snapshots, gather recent deployment history, snapshot current pod status, run connectivity checks to dependencies.
    - Ensure post-incident review includes a monitoring effectiveness assessment: Were the right alerts in place? Did they fire promptly? Were there false negatives? What monitoring improvements are needed?

34. **Design runbooks for every paging alert.**
    - Each runbook must contain:
      - **Alert description:** What this alert means in plain language.
      - **Impact assessment:** What is affected and how to verify impact scope.
      - **Diagnostic steps:** Specific queries, dashboard links, and log searches to run first.
      - **Remediation options:** Ordered by likelihood and safety (e.g., 1. Check if recent deployment—rollback. 2. Check dependency health. 3. Scale horizontally. 4. Engage secondary on-call).
      - **Escalation criteria:** When to escalate and to whom.
    - Runbooks must be reviewed and updated after every incident that uses them.

---

### Phase 12 — Monitoring System Health and Scalability

35. **Monitor the monitoring system itself (meta-monitoring).**
    - Track: metric ingestion rate and lag, log pipeline throughput and delivery latency, trace ingestion success rate, storage utilization of monitoring backends, query latency for dashboards and alert evaluation.
    - Alert on: metric scrape failures, log delivery pipeline backup, tracing collector queue saturation, monitoring backend approaching storage limits, alert evaluation failures.
    - Maintain a separate, minimal meta-monitoring path (e.g., a simple external health check that does not depend on the primary monitoring stack) so that monitoring failures are detected even when the monitoring system is down.

36. **Plan for monitoring scalability.**
    - Estimate current and projected telemetry volume: metrics data points per second, log GB per day, traces per second.
    - Design horizontal scaling strategies for each monitoring component: sharded Prometheus (Thanos/Cortex/Mimir), scaled Elasticsearch clusters or Loki with object storage, trace backend scaling with object storage tiers.
    - Implement cost management: use recording rules to pre-aggregate high-cardinality metrics, apply log filtering to drop verbose/low-value logs before ingestion, use tiered storage (hot/warm/cold) for all telemetry types.
    - Review monitoring costs monthly. Set budget alerts on monitoring infrastructure spend.

---

### Phase 13 — Documentation and Output Delivery

37. **Produce a structured monitoring architecture document** that includes:
    - **System Context:** Architecture overview, service inventory, dependency map, criticality tiers.
    - **Metrics Catalog:** Every metric defined, its source, labels, collection interval, and purpose.
    - **SLI/SLO Definitions:** Each SLI formula, SLO target, error budget, measurement source, and burn-rate alert configuration.
    - **Alerting Rules:** Each alert with its query, threshold, evaluation window, severity, routing destination, and runbook link.
    - **Tracing Design:** Propagation protocol, sampling strategy, span attribute standards, backend choice and sizing.
    - **Logging Design:** Pipeline architecture, structured log schema, log level policies, retention tiers.
    - **Dashboard Inventory:** Each dashboard with its purpose, audience, and link.
    - **Infrastructure Monitoring:** Cloud and Kubernetes monitoring specifics.
    - **Operational Procedures:** On-call integration, runbook index, incident response hooks, post-incident monitoring review checklist.
    - **Cost and Scalability Plan:** Current telemetry volume, projected growth, scaling strategy, cost management measures.

38. **Validate the monitoring design against a completeness checklist.**
    - [ ] Every Tier 1 service has golden signal metrics defined.
    - [ ] Every critical user journey has an SLI and SLO.
    - [ ] Every SLO has multi-window burn-rate alerts configured.
    - [ ] Every paging alert has a runbook.
    - [ ] Distributed tracing covers all inter-service communication paths.
    - [ ] All logs are structured with trace_id correlation.
    - [ ] Dashboards exist for every Tier 1/2 service.
    - [ ] Synthetic monitoring covers critical external endpoints.
    - [ ] Monitoring configuration is in version control.
    - [ ] The monitoring system itself is monitored.
    - [ ] Alert routing and escalation paths are tested.
    - [ ] Log and metric retention policies are defined and implemented.
    - [ ] Monitoring is deployed and validated in staging before production.
    - [ ] Cost projections and budgets are established.

39. **Tailor the output format to the request.** Depending on what the user asked for, deliver the output as:
    - A full monitoring architecture document (for greenfield design requests).
    - A gap analysis with prioritized recommendations (for monitoring audits).
    - Specific alert rules, queries, or configurations (for targeted implementation questions).
    - A comparison matrix with trade-off analysis (for tooling selection questions).
    - A migration plan with phased rollout (for monitoring platform migrations).
    - A concise advisory with the single most impactful improvement (for quick questions).

Always present recommendations in priority order: highest impact and lowest effort first. Always justify each recommendation with the specific risk it mitigates or the visibility gap it closes.
