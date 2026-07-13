---
name: tl-render-deploy
description: Deploy applications to Render by analyzing codebases, generating render.yaml
  Blueprints, and providing Dashboard deeplinks. Use when the user wants to deploy,
  host, publish, or set up their applica...
license: MIT
tags:
- general
metadata: None
author: github.com/openai/skills
version: 1.0.0
---

# Post-deploy verification and basic triage (All Methods)

Keep this short and repeatable. If any check fails, fix it before redeploying.

1. Confirm the latest deploy is `live` and serving traffic
2. Hit the health endpoint (or root) and verify a 200 response
3. Scan recent error logs for a clear failure signature
4. Verify required env vars and port binding (`0.0.0.0:$PORT`)

Detailed checklist and commands: references/post-deploy-checks.md

If the service fails to start or health checks time out, use the basic triage guide:
references/troubleshooting-basics.md

## Troubleshooting

### Escalated Network Access

If deployment fails due to network issues (timeouts, DNS errors, connection resets), rerun the deploy with escalated permissions (use `sandbox_permissions=require_escalated`). The deploy requires escalated network access when sandbox networking blocks outbound requests.

Example guidance to the user:

```
The deploy needs escalated network access to deploy to Render. I can rerun the command with escalated permissions—want me to proceed?
```

Optional: If you need deeper diagnostics (metrics/DB checks/error catalog), suggest installing the
`render-debug` skill. It is not required for the core deploy flow.
