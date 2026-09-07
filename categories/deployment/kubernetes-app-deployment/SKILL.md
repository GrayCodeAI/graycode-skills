---
name: kubernetes-app-deployment
description: "Containerize and deploy an existing web app or API to a running Kubernetes cluster with manifests and safeguards."
license: MIT
tags:
- kubernetes
- containers
- deployment
- docker
---

# Deploy to AKS

**Use when:** deploying a web app/API to AKS; containerizing for Kubernetes; generating manifests; AKS CI/CD; DS001–DS013 failures.

**Not for:** provisioning clusters (`azure-kubernetes`), AKS Automatic readiness (`azure-kubernetes-automatic-readiness`), non-AKS targets.

## Workflow

Requires: existing AKS cluster, `az login`, `kubectl` configured. Follow `phases/quick-deploy.md`. On failure: `references/rollback.md`.

## References

- detection.md — framework/port/health detection
- safeguards.md — DS001-DS013 checklist
- workload-identity.md — Workload Identity setup
- rollback.md — recovery procedures
- base-images.md — base image policy and `<LATEST_STABLE_*>` resolution

## Knowledge Packs

Load `knowledge-packs/frameworks/<framework>.md` per detected framework. Available: `spring-boot`, `express`, `nextjs`, `fastapi`, `django`, `nestjs`, `aspnet-core`, `go`, `flask`

## Templates

`templates/` (dockerfiles/, k8s/, github-actions/, mermaid/).
