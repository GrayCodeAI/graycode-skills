---
name: role-based-access-control
description: "Use when implementing role-based access control with OIDC token validation and policy enforcement."
license: MIT
tags:
- rbac
- oidc
- access-control
- security
---

# RBAC and OIDC Integration

## Purpose
Comprehensive Role-Based Access Control with OIDC flow integration.

## Core Principles
1. Principle of least privilege
2. Secure token validation
3. Strict policy enforcement
4. Auditability of access
5. Separation of duties

## Agent Protocol
Triggers: Access requests
Input Context Required: User identity, requested resource, action
Output Artifact: Access decision
Response Formats:
```json
{
  "allowed": true,
  "reason": "Role has permission"
}
```

## Decision Matrix
```
[Request] -> [Check Token] -> [Extract Roles] -> [Evaluate Policy] -> [Decision]
```

## Detailed Architectural Overview
```
Client -> API Gateway -> RBAC Service -> Policy DB
                         |
                         v
                    OIDC Provider
```

## Workflow Steps
Phase 1: Initialization
1. Load policies
2. Connect to DB
3. Init cache

Phase 2: Token Validation
1. Parse JWT
2. Verify signature
3. Check expiry

Phase 3: Role Extraction
1. Get claims
2. Map to roles
3. Resolve hierarchy

Phase 4: Policy Evaluation
1. Find matching policies
2. Check conditions
3. Calculate final decision

Phase 5: Audit Logging
1. Format log entry
2. Add context
3. Write to stream

Phase 6: Response
1. Format response
2. Add headers
3. Send to client

## Extended Troubleshooting Guide
| Symptom | Primary Cause | Mitigation Action |
|---------|---------------|-------------------|
| Token rejected | Expired token | Refresh token |
| Role missing | Claim not mapped | Check mapping config |
| Policy failure | Condition not met | Review policy rules |
| High latency | DB slow | Add caching |
| Audit failed | Stream full | Increase capacity |
| Unknown error | Unhandled exception | Check logs |

## Complete Execution Scenario
```
Request -> Valid Token -> Role Admin -> Allow Action
```

## Rules and Guidelines
1. Always validate tokens first
2. Fail closed on errors
3. Log all access decisions
4. Cache policies for performance
5. Regularly review role mappings

## Reference Guides
1. OIDC Auth Code Flow
2. OIDC Implicit Flow
3. RBAC Core Logic
4. RBAC Decision Matrix
5. RBAC Policy Evaluation
6. OIDC Token Validation
7. RBAC Audit Logging
8. RBAC Integration Patterns

## Handoff
Refer to auth skill.
<!-- compression footer -->
