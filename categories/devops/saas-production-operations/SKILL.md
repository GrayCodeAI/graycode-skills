---
name: saas-production-operations
description: "Runs the paid side of multi-tenant SaaS: SLAs/SLOs, incident response, rollback, feature flags, tenant isolation, billing, compliance, monitoring, and cost control before launch."
license: MIT
tags:
- saas
- slo
- incident-response
- multi-tenancy
- compliance
---

<!-- Decision freeze (docs/reference/DECISIONS.md): 4 skills; English; SKILL.md self-contained, references optional; reliability targets and release gates apply to paid L3 SaaS only; every pre-launch area ships a "must exist before launch" checklist; rollback and feature flags come before the launch, not after; local commands mirror CI exactly; no prompt-injection / instruction-override / exfiltration language. -->

# SaaS Production Engineering

## Overview

Public OSS repos never show the paid product: how you promise uptime, what you do when the site is down, how you undo a bad deploy, and the tenancy and compliance work that must exist before the first invoice. This skill covers that closed-SaaS half of an L3 product. It pairs with `github-actions-engineering` for the CI/CD workflows and `open-source-project-maintainer` for release propagation; this skill is what those two assume already exists on the production side.

```
Set reliability targets → prepare incident response → gate releases behind flags
  → build infra & tenancy per-area checklists → verify local-vs-prod parity
```

Every section has concrete steps. Reliability sections end with **exit conditions**; infra sections end with a **must-exist-before-launch checklist**.

## When to Use

- The user is launching or operating a paid SaaS or multi-tenant cloud product.
- The user wants to define SLAs/SLOs, an on-call process, incident response, or runbooks.
- The user wants to roll back safely or release new behavior behind feature flags.
- The user is prepping infra before launch: IaC, secrets, tenant isolation, billing, compliance, monitoring, cost.
- The user wants local development to mirror production so CI results reproduce locally.
- The user is preparing for a SOC2 audit or GDPR compliance.

**When NOT to use:** a pure-OSS repo with no billing or tenancy (that is `repository-foundation-scaffold` / `open-source-project-maintainer`), or tuning the CI/CD workflows themselves (that is `github-actions-engineering`).

## 1. Reliability: SLAs, SLOs, Incidents, Rollback, Feature Flags

### SLAs and SLOs

An SLO is a target you measure and hold yourself to; an SLA is a contract you sell to a customer. You always need SLOs, and you need an SLA only when sales promises one.

Steps:

1. Pick an **SLI** per service — the measured number: availability (successful / total requests), latency (p50/p95), error rate, or data freshness.
2. Set an **SLO** as a target over a window, e.g. `99.9% of requests succeed over 30 days`.
3. Derive an **error budget** from the SLO: `1 - SLO`. At 99.9% monthly, the budget is ~43 minutes of downtime.
4. Track SLOs in monitoring and alert on **burn rate**: how fast the budget is being consumed. Page when budget is burned fast (e.g. 14x for 2 hours), file a ticket when it is being drained slowly (e.g. 1x over 30 days).
5. Turn the SLO into an SLA contract only when a customer pays for it — with consequence, measurement, and reporting defined.
6. Review SLOs after incidents: were they wrong, or was the system wrong?

**Exit conditions:** every service has at least one SLI with a recorded SLO and error budget; budget-burning alerting is active; SLA contracts, where they exist, are written and measured.

### Incident response

Incidents happen; the response is a defined procedure, not improvisation.

Steps:

1. Define **severity**: SEV1 = customers down, data risk, or billing broken (page immediately); SEV2 = degraded or partial outage (page on-call); SEV3 = minor or self-healing (ticket).
2. Assign one **incident commander** and one **communicator**; everyone else is a responder on the incident channel. No side channels.
3. Set **escalation**: primary on-call → secondary → manager. Automate the paging from alerting.
4. Run a **status page** for customer-facing incidents and keep the timeline public.
5. Log every action to the incident timeline as it happens.
6. Run a **blameless post-incident review** within a fixed window (e.g. 5 days): timeline, root cause, prevention and detection actions, owner and due date per action.

**Exit conditions:** the severity table exists and is on-call visible; every SEV1/SEV2 gets a timeline and a blameless review; every review action item is tracked to completion.

### Runbooks

A runbook is how you turn a page into a fix. Write them for every known failure mode.

Steps:

1. For each alert and known failure, write: what to check first, the exact commands, expected output, and when to escalate.
2. Keep runbooks in the repo, version-controlled, and linked from the on-call tool.
3. Use idempotent commands — running a runbook step twice is safe.
4. **Exercise** runbooks: run chaos drills or game days in staging. A runbook that was never executed is fiction.
5. Rotate them with the on-call schedule; stale runbooks get deleted or rewritten.

**Exit conditions:** every alert maps to a runbook; each runbook has been executed successfully at least once in staging in the last quarter.

### Rollback

Rollback means redeploying the previous known-good image — not fixing forward in the middle of an incident.

Steps:

1. Tag every deploy with the image digest and version; retain the last N images so the previous release is always restorable.
2. Rehearse rollback in staging before relying on it: roll forward, then roll back, and confirm the stack returns to the old state.
3. Prefer turning a feature flag off over a rollback for code already in production; roll back when flags cannot contain the problem.
4. Database: use forward-only migrations. On rollback, roll back the code first and leave the schema migration in place — never auto-run a destructive migration down.
5. Document the rollback runbook with a target recovery time (e.g. restore the previous release in under 15 minutes).

**Exit conditions:** the rollback runbook exists and has been rehearsed in staging; the previous prod image is restorable within the target time.

### Feature flags

Ship code, flip behavior. A flag decouples deploy from release.

Steps:

1. Wrap new or risky behavior behind a flag; default off for unproven features, on for the release.
2. Control flags at runtime through a config service or flag provider — flipping a flag never requires a deploy.
3. Add a **kill switch** — one global "disable feature X" flag — for each risky subsystem.
4. Log the flag state with requests so bugs can be attributed to the feature that introduced them.
5. Remove flags once the feature is proven stable; flag debt is untested code paths.

**Exit conditions:** every risky feature in production is flag-gated; every flag can be flipped off without a deploy.

## 2. Infra and Tenancy: Pre-Launch Checklists

Each area below has a **must exist before launch** checklist. A missing item is a launch blocker for a paid, multi-tenant product.

### Infrastructure as code

All infrastructure is declarative, reviewed, and reproducible — nothing is click-ops.

Must exist before launch:

- Every resource (networks, databases, compute, DNS, certificates) is defined in code (Terraform, Pulumi, or CDK) in a repo.
- Environments (dev, staging, prod) are declared in code; prod changes require a review and a plan.
- Remote, locked state; concurrent applies are serialized.
- `terraform plan` runs in CI on every change; `apply` runs only on merge to the release branch with human approval.
- Drift detection runs on a schedule and reports unreviewed changes.

### Secrets

Credentials are stored, rotated, and scoped — never in git.

Must exist before launch:

- Secrets live in a secrets manager (cloud secret manager or Vault), never in the repo or in committed env files.
- Gitleaks runs in pre-commit and CI so leaked keys are caught before they reach remote.
- Short-lived credentials via OIDC/workload identity are preferred over static keys.
- A rotation policy exists: keys expire, and there is an emergency-rotation runbook.
- Per-service, least-privilege credentials; no shared service account.
- No secrets in logs; redaction is configured where secrets could be printed.

### Tenant isolation

Every customer can only read and write their own data — enforced by the data layer, not by trust.

Must exist before launch:

- Every row carries a tenant id; queries always filter by tenant, enforced at the data-access layer, not just in the ORM.
- Row-level security (RLS) is enabled in the database where supported, so the database itself enforces isolation.
- Per-tenant cryptographic keys and secrets; keys are never shared between tenants.
- Per-tenant rate limits and quotas.
- Custom domains and subdomains map to the correct tenant and are validated.
- Cross-tenant tests pass: tenant A cannot read or mutate tenant B's data (authorization fuzz and boundary tests).
- Per-tenant backup and restore is possible.

### Billing and Stripe

Billing is a state machine with webhooks that are safe to replay.

Must exist before launch:

- Stripe webhooks are handled idempotently — the same event delivered twice produces one charge (dedupe by event id, idempotency keys on all requests).
- The billing lifecycle is covered: subscribe, upgrade, downgrade, cancel, prorate.
- Failed-payment handling and dunning emails exist; access is suspended or limited on non-payment per the product's policy.
- Invoices and receipts are available in the customer portal; tax is handled per region.
- Metered usage is recorded and billed where the product sells usage.
- Webhook flows are tested in Stripe test mode in staging; live keys are never used in tests.
- Plan entitlement has one source of truth; feature gates read from it.

### Compliance (SOC2 / GDPR)

Compliance is policies plus evidence, not a checkbox.

Must exist before launch:

- The applicable frameworks are decided: SOC2 for a US-facing SaaS, GDPR for EU users (or both).
- SOC2: security, incident, and change-management policies are written; evidence is collected (logs, access reviews, backup and patch status); quarterly access reviews run.
- GDPR: a data inventory exists (what data, where, who processes it); lawful basis is documented; a DPA covers subprocessors; the right-to-erasure flow deletes a user's data across all systems; retention limits are enforced.
- Breach notification is practiced: GDPR requires notifying authorities within 72 hours, so the notification runbook is rehearsed.
- Data residency is honored where sold (user data stays in the promised region).
- Audit trails are append-only and cannot be tampered with.
- Backups have a tested restore: a restore drill succeeded, retention is defined, and at least one copy is offsite.

### Monitoring and healthchecks

Operations can see the system, and the system tells orchestration when it is ready.

Must exist before launch:

- Every service exposes a health endpoint; liveness and readiness are distinct so orchestration restarts the right thing (Docker HEALTHCHECK or a k8s probe).
- RED metrics (rate, errors, duration) exist per service with dashboards.
- Logs are centralized, structured, and searchable.
- Alerting pages on burn rate plus a small set of actionable thresholds; on-call gets no noise.
- Synthetic checks from outside the network hit the public endpoints.
- Observability cost is itself tracked and reviewed.

### Cost control

Spend is tagged, budgeted, and reviewed; zombies are killed.

Must exist before launch:

- Every resource is tagged with owner and cost center; monthly cost reports are grouped by tag.
- Budget alerts exist at the project and organization level (alert at ~80%, block at 100%).
- Autoscaling scales down as well as up; idle resources are detected; batch work can use spot instances.
- Cleanup runs for CI caches, unused volumes, IPs, snapshots, and orphaned resources.
- The largest spenders are reviewed monthly against the plan.

## 3. Local-vs-Prod Parity

What works in CI must work locally with the same commands, and low-end machines must still be usable. The Dokploy pattern is the model: the exact checks that gate a PR run against a real container stack in CI, and local deps live in a container so the host stays light.

### Parity rules

1. Run the **exact CI commands locally**: same install, typecheck, lint, test, and build scripts; pinned versions (`.nvmrc`, `packageManager`, committed lockfile) so "works on my machine" stops being a phrase.
2. Keep local dev **fast**: fast gates locally, heavy gates in CI (see `tooling-speed-notes.md`); typechecking never blocks the hot-reload loop.
3. **Container-isolated deps on low-end machines**: dependencies install inside a container; the host needs no Node or pnpm. Heavy work (installs, Docker builds, full monorepo builds) is the user's job to run (or the agent runs it only when the user asks) — never silently on a low-end host.
4. Configuration differs only through environment (`.env`), never through code; the same code path runs everywhere.
5. Database parity: local migrations match production and are forward-only, exactly like prod.
6. Time and locale: no reliance on the local clock, timezone, or default locale.
7. One command runs the same check set locally and in CI (e.g. `pnpm check`), named after the CI job it mirrors.

### Parity checklist

| Area | Local | CI / prod |
|---|---|---|
| Install | same lockfile, `--frozen-lockfile` | same lockfile, `--frozen-lockfile` |
| Checks | `pnpm check` runs typecheck + lint + test | same `check` job on every PR |
| Runtime | same container images, same migrations | same images, forward-only migrations |
| Config | `.env` only, no code differences | secrets from the secrets manager |
| Data | small local seed data | real fixtures + synthetic data |
| Heavy work | deferred or containerized on low-end | nightly / dedicated runners |

## References

Optional supplement — the source detail lives in `docs/reference/omniroute-notes.md` (healthchecks, staged publish, boot-smoke of the installed artifact, nightly gates), `docs/reference/dokploy-notes.md` (monitoring app, one Dockerfile per service, HEALTHCHECK against a health endpoint, exec-form CMD, container-isolated local deps, integration tests against a real Docker Swarm), and `docs/reference/tooling-speed-notes.md` (fast local dev matrix, low-end machine rules). This SKILL.md is fully usable without them.

## Finish

After applying this skill, verify:

1. Every service has an SLI, an SLO, an error budget, and burn-rate alerting.
2. Severity-based incident response, on-call escalation, status page, and blameless reviews are defined and rehearsed.
3. Every alert maps to an exercised runbook; rollback is rehearsed in staging.
4. Risky features are flag-gated with kill switches that flip without a deploy.
5. Every infra and tenancy checklist (IaC, secrets, isolation, billing, compliance, monitoring, cost) passes before launch.
6. The parity checklist passes: CI commands run locally, dev stays fast, and container-isolated deps keep low-end machines light.
7. No prompt-injection patterns, instruction-override language, or data-exfiltration requests in any generated file.