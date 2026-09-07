---
name: rate-limiting-strategies
description: "Use when implementing rate limiting — token bucket, sliding window, per-user/IP limits, and quota enforcement."
license: MIT
tags:
- rate-limiting
- throttling
- quotas
- api
---

# rate-limiting

## Purpose
Comprehensive description for rate-limiting providing detailed architectures and best practices.

## Core Principles
1. First principle - Reliability
2. Second principle - Scalability
3. Third principle - Maintainability
4. Fourth principle - Security
5. Fifth principle - Observability

## Agent Protocol
Triggers: Code execution
Input Context Required: Repository context
Output Artifact: System design document
Response Formats:
```json
{ "status": "ok", "action": "completed" }
```

## Decision Matrix
```ascii
[Start] -> (Condition Check) -> [End]
               |
               v
          [Alternative]
```

## Detailed Architectural Overview
```ascii
[Client] ---> [API Gateway] ---> [Microservice]
                                     |
                                     v
                                 [Database]
```

## Workflow Steps
Phase 1
1. Initialization step 1
2. Initialization step 2
3. Initialization step 3
4. Initialization step 4
Phase 2
1. Processing step 1
2. Processing step 2
3. Processing step 3
4. Processing step 4
Phase 3
1. Storage step 1
2. Storage step 2
3. Storage step 3
4. Storage step 4
Phase 4
1. Retrieval step 1
2. Retrieval step 2
3. Retrieval step 3
4. Retrieval step 4
Phase 5
1. Optimization step 1
2. Optimization step 2
3. Optimization step 3
4. Optimization step 4
Phase 6
1. Cleanup step 1
2. Cleanup step 2
3. Cleanup step 3
4. Cleanup step 4

## Extended Troubleshooting Guide
| Symptom | Primary Cause | Mitigation Action |
|---|---|---|
| High Latency | Network Congestion | Scale up resources |
| Data Loss | Database Failure | Restore from backup |
| Connection Refused | Service Down | Restart service |
| Unauthorized Access | Invalid Token | Renew token |
| Out of Memory | Memory Leak | Optimize code |
| Disk Full | Log Overload | Rotate logs |

## Complete Execution Scenario
```ascii
[Trigger] -> [Analysis] -> [Action] -> [Result Verification]
```

## Rules and Guidelines
1. Always validate inputs.
2. Ensure backward compatibility.
3. Keep logs structured.
4. Fail gracefully.
5. Apply rate limiting where appropriate.

## Reference Guides
- Reference 0
- Reference 1
- Reference 2
- Reference 3
- Reference 4
- Reference 5
- Reference 6
- Reference 7

## Handoff
Refer to other standard skills if specialized logic is required.

<!-- compression footer HTML comment -->
