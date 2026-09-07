---
name: cloud-cost-management
description: "Query cloud costs, forecast spending, and optimize usage across subscriptions to reduce waste."
license: MIT
tags:
- cost
- finops
- optimization
- budgeting
---

# Azure Cost Management Skill

Query historical costs, forecast future spending, optimize to reduce waste.

## Routing

| User Intent | Workflow |
|-------------|----------|
| Understand current costs | Cost Query |
| Reduce costs / find waste | Cost Optimization |
| Project future costs | Cost Forecast |

## Quick Reference

| Property | Value |
|----------|-------|
| **Query API** | `POST {scope}/providers/Microsoft.CostManagement/query?api-version=2023-11-01` |
| **Forecast API** | `POST {scope}/providers/Microsoft.CostManagement/forecast?api-version=2023-11-01` |
| **Required Role** | Cost Management Reader + Monitoring Reader + Reader (on target scope) |

## Scope Patterns

- Subscription: `/subscriptions/<id>`
- Resource Group: `/subscriptions/<id>/resourceGroups/<name>`
- Management Group: `/providers/Microsoft.Management/managementGroups/<id>`
- Billing Account: `/providers/Microsoft.Billing/billingAccounts/<id>`

## Service-Specific Optimization

- Redis
- Storage

## References

- MCP Tools, Best Practices, Safety
- SDK: Redis .NET
