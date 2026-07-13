---
name: azure-hosted-copilot-sdk-ms
description: "Build and deploy GitHub Copilot SDK apps to Azure. USE FOR: build copilot app, create copilot app, copilot SDK, @github/copilot-sdk, scaffold copilot project, copilot-powered app, deploy copilot ap..."
license: MIT
tags: [aws]
metadata: None
author: Microsoft
version: 1.0.0
---

# GitHub Copilot SDK on Azure

## Step 1: Route

| User wants | Action |
|------------|--------|
| Build new (empty project) | Step 2A (scaffold) |
| Add new SDK service to existing repo | Step 2B (scaffold alongside) |
| Deploy existing SDK app to Azure | Step 2C (add infra to existing SDK app) |
| Add SDK to existing app code | Integrate SDK |
| Use Azure/own model | Step 3 (BYOM config) |

## Step 2A: Scaffold New (Greenfield)

`azd init --template azure-samples/copilot-sdk-service`

Template includes API (Express/TS) + Web UI (React/Vite) + infra (Bicep) + Dockerfiles + token scripts — do NOT recreate. See SDK ref.

## Step 2B: Add SDK Service to Existing Repo

User has existing code and wants a new Copilot SDK service alongside it. Scaffold template to a temp dir, copy the API service + infra into the user's repo, adapt `azure.yaml` to include both existing and new services. See deploy existing ref.

## Step 2C: Deploy Existing SDK App

User already has a working Copilot SDK app and needs Azure infra. See deploy existing ref.

## Step 3: Model Configuration

Three model paths (layers on top of 2A/2B):

| Path | Config |
|------|--------|
| **GitHub default** | No `model` param — SDK picks default |
| **GitHub specific** | `model: "<name>"` — use `listModels()` to discover |
| **Azure BYOM** | `model` + `provider` with `bearerToken` via `DefaultAzureCredential` |

See model config ref.

## Step 4: Deploy

Invoke **azure-prepare** (skip its Step 0 routing — scaffolding is done) → **azure-validate** → **azure-deploy** in order.

## Rules

- Read `AGENTS.md` in user's repo before changes
- Docker required (`docker info`)