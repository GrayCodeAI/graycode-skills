---
name: agent-governance-review
description: "Risk-score autonomous agents, run consensus judges, detect config drift, and emit compliance evidence for trust/authorization checks."
license: Apache-2.0
tags:
- governance
- security
- compliance
---

# Know Your Agents (KYA) Governance Review

Use this skill to answer a different question from "is the run fast?" (see `duct`) or "is the metric improving within budget?" (see `labnb`): **is the agent authorized, policy-compliant, and uncompromised?**

It wraps [`veldt-kya`](https://github.com/veldtlabs/veldt-kya) ("Know Your Agents", Apache-2.0), a governance SDK that risk-scores agents, runs consensus judges over their behavior, detects drift from an approved definition, and produces regulator-grade compliance evidence.

This is the third review axis in this repo: `duct` = resource accounting, `labnb` = budget / experimental-validity accounting, `kya` = trust / authorization / compliance accounting.

## When To Use

- Before granting an agent a privileged action (writing outside scope, executing SQL, calling external services), score or consensus-check it first.
- When a long-running labnb experiment should stop if the agent drifts from its approved configuration or trips a policy judge — not only when the metric stalls.
- When a run touches regulated or PII-bearing data and needs auditable authorization evidence (GDPR, HIPAA, EU AI Act, and similar).

Skip it for ordinary, low-stakes local iteration; governance has real cost (see Guardrails).

## Install

```bash
pip install veldt-kya   # Apache-2.0
```

`veldt-kya` is a heavier, pre-1.0 dependency (database, identity bindings, optional external judges). Keep it **optional** — it is never required by the `labnb` core. Install it only in environments that need governance.

## Core Capabilities

```python
from kya import score_agent, normalize_agent_def
from kya import canonical_hash, detect_drift
from kya.scorer_orchestrator import check_consensus, register_available_adapters
from kya import compliance_summary
```

- **Pre-deployment scoring** — `score_agent(...)` returns an object with `score`, a severity `bucket` (e.g. `"critical"`), and per-factor `factors` (each with `.name` / `.delta`).
- **Runtime consensus** — `check_consensus(...)` runs multiple judges in parallel and returns `consensus` (`OK` / `SPLIT` / `UNCLEAR` / `BREACH`), `per_dimension` scores (input_safety, safety, faithfulness), and per-`judges` detail.
- **Drift detection** — `canonical_hash(definition)` plus `detect_drift(...)` flag unauthorized configuration changes against an approved baseline.
- **Compliance evidence** — `compliance_summary(...)` emits model cards / breach-notification artifacts across many regimes.

## Producing A labnb Governance Verdict

`labnb`'s `monitor_slice.py check` can break a slice on a **governance** signal, but it stays dependency-free: it reads a small JSON **verdict file** rather than importing KYA. This skill's job is to run a governance check and write that verdict.

Canonical verdict schema (all keys optional):

```json
{
  "decision": "allow | warn | block",
  "trust_score": 0.0,
  "drift": false,
  "reasons": ["short human-readable reasons"]
}
```

Map a KYA result onto it, then write it with the bundled helper:

```python
from kya.scorer_orchestrator import check_consensus
verdict = check_consensus(...)              # consensus: OK | SPLIT | UNCLEAR | BREACH
decision = "block" if verdict.consensus == "BREACH" else (
    "warn" if verdict.consensus in ("SPLIT", "UNCLEAR") else "allow")
```

```bash
python skills/kya/scripts/write_verdict.py \
  --output "$EXPERIMENT_DIR/artifacts/governance.json" \
  --decision "$decision" \
  --trust-score 0.41 \
  --reason "consensus=BREACH on faithfulness judge"
```

`write_verdict.py` is deterministic and tool-agnostic: it validates the fields and writes the canonical schema, so you can drive it from KYA, `detect_drift`, or any other governance source.

## Feeding It Into The Loop

Point `labnb`'s monitor at the verdict so a compromised or unauthorized slice breaks (with the highest break priority — governance outranks budget, engineering, and validity):

```bash
python skills/labnb/scripts/monitor_slice.py check \
  --experiment-dir "$EXPERIMENT_DIR" \
  --governance-file "$EXPERIMENT_DIR/artifacts/governance.json" \
  --min-trust-score 0.6 --break-on-drift
```

A `block` decision, a `trust_score` below `--min-trust-score`, or `drift: true` (with `--break-on-drift`) breaks the slice and moves the entry to `blocked`; a `warn` decision is advisory. This also fits `labnb`'s Action Gate: run the check before any write-bearing or privileged step.

The gate fails closed: once `--governance-file` is set, if the verdict file is missing, unreadable, or malformed the monitor treats it as a `block`. So always write a verdict before the check — including a conservative one (e.g. `decision: "warn"` or `"block"`) when KYA or its judges are unavailable — rather than leaving the file absent.

## Guardrails

1. Respect any parent constitution, project policy, or task-level write constraint already in scope.
2. Keep `veldt-kya` optional. Never make it a hard dependency of the `labnb` core or of offline CI; the verdict-file seam exists precisely so labnb stays dependency-free.
3. Governance has cost. Consensus judging may call LLMs or external services (e.g. Fiddler, Presidio); count that time and spend against the same labnb budget, per labnb's budget policy.
4. Handle a degraded/offline path: if KYA or its judges are unavailable, emit a conservative verdict (for example `decision: "warn"`) rather than silently treating the run as authorized.
5. Treat the project as pre-1.0 and verify its behavior before relying on it for real compliance decisions; do not present its output as legal/regulatory advice.
6. Do not send secrets or unminimized PII to external judges; use KYA's PII scanning and scrub before sharing.
