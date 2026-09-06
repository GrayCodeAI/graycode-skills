---
name: multi-agent-gateway-security
description: "Designs, deploys, and secures agent gateway solutions for multi-agent systems, configuring ingress and egress patterns with model armor, IAP, and agent registry."
license: Apache-2.0
tags:
- agentic-ai
- security
- gateway
- model-armor
- iam
---

# Agent Gateway multi-agent security

## Critical Enforcement Rules & Rationale

*   **Gcloud Release Tracks**: Always use the exact release tracks specified in
    the commands (e.g., `gcloud beta network-services agent-gateways`). Omitting
    these prefixes causes commands to fail because Agent Gateway features are
    located in specialized, non-default namespaces.
*   **API Enablement**: Include `modelarmor.googleapis.com` in the API
    enablement list when setting up guardrails. Excluding it prevents Model
    Armor policies and filters from successfully attaching to the Gateway.
*   **Egress Verification**: Egress policy verification requires using the
    Python script
    (scripts/verify_egress_policies.py),
    not `curl`. Egress gateways rely on runtime SDK lifecycle handling and JWT
    context that a standard curl command cannot simulate correctly.
*   **Model Armor Keys**: In `model-armor-config.yaml`, always include both
    `piAndJailbreakFilterSettings` and `sdpFilterSettings` (`filterEnforcement:
    ENFORCE`). Invalid or missing filters cause deployment validation failures
    or lead to silent bypasses of the guardrails.
*   **Subnet Private Access**: Any subnet hosting a Private Service Connect
    network attachment for Egress Gateways must have `private_ip_google_access =
    true` enabled in Terraform. Disabling this blocks connectivity to
    Google-managed endpoints, causing total routing failures for agents.
*   **Direct Delivery**: Immediately provide the requested architecture,
    configuration files, CLI commands, scripts, and diagrams in full. Do not
    stop at a planning phase, do not generate a plan artifact, and do not ask
    for user confirmation before delivering outputs.
*   **No Infrastructure Execution**: Do not attempt to run deployment or
    verification commands (such as `gcloud` `kubec--------------------------------------------------------------------------

## Quick Reference: Required Filenames

Always generate files with these exact names when requested:

1.  `agw-ingress-config.yaml`
    ([assets/agw-ingress-config.yaml](assets/agw-ingress-config.yaml))
2.  `agw-egress-config.yaml`
    ([assets/agw-egress-config.yaml](assets/agw-egress-config.yaml))
3.  `agw-authz-extension.yaml`
    ([assets/agw-authz-extension.yaml](assets/agw-authz-extension.yaml))
4.  `agw-authz-policy.yaml`
    ([assets/agw-authz-policy.yaml](assets/agw-authz-policy.yaml))
5.  `model-armor-config.yaml`
    ([assets/model-armor-config.yaml](assets/model-armor-config.yaml))
6.  `sgp-policy.yaml` ([assets/sgp-policy.yaml](assets/sgp-policy.yaml))
7.  `iap-policy.json` ([assets/iap-policy.json](assets/iap-policy.json))
8.  `model-armor-payload.json`
    ([assets/model-armor-payload.json](assets/model-armor-payload.json))

--------------------------------------------------------------------------------

## 1. Dual Ingress & Egress Architecture Design (`dual_ingress_egress_architecture_design`)

-   **Ingress Pattern**: `CLIENT_TO_AGENT` fronted by Ingress Control Plane
    (Agent Gateway, Model Armor).
-   **Egress Pattern**: `AGENT_TO_ANYWHERE` utilizing Egress Control Plane
    (Agent Gateway, `roles/iap.egressor` CEL policies, Cloud DNS) and Egress
    Data Plane (PSC Interface, Cloud Run, PSC Google APIs Global Endpoint),
    coordinated via Agent Registry & Agent Engine runtime.
-   **Mermaid Diagram**:

    ```mermaid
    graph TD
        Client["External Clients"] -->|HTTPS / MCP| GLB["Global Load Balancer"]
        GLB --> Ingress["Ingress Agent Gateway (CLIENT_TO_AGENT)"]
        Ingress --> MA["Model Armor (CONTENT_AUTHZ)"]
        MA --> Agent["Agent Engine Agents (BillingAgent, SupportAgent, FraudAgent)"]
        Agent --> Egress["Egress Agent Gateway (AGENT_TO_ANYWHERE)"]
        Egress --> PSC["Private Service Connect Network Attachment"]
        PSC --> Tools["Private MCP Tool Backends"]
    ```

--------------------------------------------------------------------------------

## 2. Ingress & Egress Guardrail Policy Config (`ingress_and_egress_guardrail_policy_config`)

When requested for Ingress & Egress guardrail policy configs, you MUST generate
and create all required files in the workspace:

-   `agw-ingress-config.yaml`
    ([assets/agw-ingress-config.yaml](assets/agw-ingress-config.yaml)): Declares
    `governedAccessPath: CLIENT_TO_AGENT` with protocols `HTTP` and `MCP`.
-   `agw-egress-config.yaml`
    ([assets/agw-egress-config.yaml](assets/agw-egress-config.yaml)): Declares
    `governedAccessPath: AGENT_TO_ANYWHERE` with protocol `MCP`.
-   `agw-authz-extension.yaml`
    ([assets/agw-authz-extension.yaml](assets/agw-authz-extension.yaml)):
    Configures AuthzExtension service for IAP authorization.
-   `agw-authz-policy.yaml`
    ([assets/agw-authz-policy.yaml](assets/agw-authz-policy.yaml)): Configures
    `AuthzPolicy` action `ALLOW` targeting both Ingress and Egress gateways.
-   `iap-policy.json` ([assets/iap-policy.json](assets/iap-policy.json)): Binds
    `roles/iap.egressor` with CEL condition checking
    `iap.googleapis.com/mcp.toolName == 'get_account_balance' &&
    iap.googleapis.com/mcp.tool.isReadOnly == true`.
-   `model-armor-config.yaml`
    ([assets/moel-armor-config.yaml](assets/modecurity authz-policies import`.

--------------------------------------------------------------------------------

## 4. Ingress & Egress Security Validation (`ingress_and_egress_security_validation`)

When validating security for Ingress and Egress:

1.  **Ingress 403 Unauthenticated Test**: Provide the copy-pasteable
    verification curl command from
    scripts/validate_ingress_unauth.sh
    sending an unauthenticated POST request to the Reasoning Engine endpoint
    expecting HTTP 403 Forbidden.
2.  **Python Egress Verification Script (MUST use Python script snippet, NOT
    curl)**: Provide the Python verification script snippet from
    scripts/verify_egress_policies.py
    snding JSON-RPC `tools/call` reto acquire an OIDC / OAuth ID
            token.
        4.  Pass the token in the `Authorization: Bearer <TOKEN>` header.
    -   **Verification Command**: Provide the curl command from
        scripts/verify_ingress_auth.sh.

-   **Egress 403 (Agent-to-Anywhere)**:

    -   **Root Cause**: Missing `roles/iap.egressor` IAM bindings on the Agent
        Identity, malformed principal ID, or mismatched CEL condition on tool
        metadata.
    -   **Fix Command**: Provide the exact `gcloud` command from
        scripts/fix_egress_iap.sh.

--------------------------------------------------------------------------------

## 6. Hybrid VPN Connectivity & Egress Routing (`hybrid_vpn_connectivity_egress_routing`)

-   **Terraform HCL**: Refer to baseline Terraform config in
    assets/main.tf for VPC, subnets
    (`private_ip_google_access = true`), PSC network attachment, Cloud DNS
    private forwarding for `aws.internal.`, and HA VPN gateway/router.
-   **Egress Gateway Config (`agw-egress-config.yaml`)**: Generate configuration
    declaring `governedAccessPath: AGENT_TO_ANYWHERE`, pointing to the PSC
    network attachment, and referencing `aws.internal.` in `dnsPeeringConfig`
    (see assets/agw-egress-config.yaml).
-   **Python SDK Deployment Script**: Refer to
    scripts/hybrid_vpn_agent.py for the complete
    script initializing Vertex AI with `agent_to_anywhere_config` referencing
    the Egress Gateway, enabling telemetry, and deployng `HybridAgent` using
    `e ILB IP `10.0.1.50`.
-   **Explicit TLS Warning**: Agent Gateway egress **does not natively trust
    sef-signed certificates or private enterntrols Model Armor SGP (`governance_controls_model_armor_sgp`)

When configuring dual safety layers with Model Amor on Ingress and SGP on
Egressml](assets/sgp-policy.yaml)) with Natural Language
    Constraints blocking transactions > $1000 and sanitizing PII.
3.  **Curl PATCH Command**: Provide the curl command from
    [scripts/enforce_sgp_patch.sh](scripts/enforce_sgp_patch.sh) to update
    `authzExtensions` with `sgpEnforcementMode` set to `ENFORCE`.

--------------------------------------------------------------------------------

## 9. Multi-Agent Cloud Run Egress Routing (`multi_agent_cloud_run_egress_routing`)

Do NOT produce a plan artifact or stop at planning. When configuring multi-agent
Cloud Run egress routing, you MUST directly provide and generate ALL required
components:

1.  **Egress Gateway Config (`agw-egress-config-run.yaml`)**: Generate
    configuration declaring `governedAccessPath: AGENT_TO_ANYWHERE`, PSC network
    attachment, and DNS peering for `*.run.app` (see
    [assets/agw-egress-config-run.yaml](assets/agw-egress-config-run.yaml)).
2.  **Register Cloud Run Services in Agent Registry**: Provide the registration
    commands from
    [scripts/register_cloud_run_services.sh](scripts/register_cloud_run_services.sh)
    registering all 3 Cloud Run services (`marketing-tool-service`,
    `sales-tool-service`, `support-tool-service`) in the `us-east4` Agent
    Registry.
3.  **`iap-policy.json` (Multi-Agent)**: Generate `iap-policy.json`
    ([assets/iap-policy-multi-agent.json](assets/iap-policy-multi-agent.json))
    containing all 3 `principal://` bindings in the `members` list under
    `roles/iap.egressor`.
4.  **Python SDK Deployment Script**: Refer to
    [scripts/multi_agent_cloud_run.py](scripts/multi_agent_cloud_run.py) for the
    complete GenAI SDK deployment script.

--------------------------------------------------------------------------------

## 10. Advanced Model Armor Filtering (`advanced_model_armor_filtering`)

For custom keyword matching, configure `userDefinedFilterSettings` (see
[assets/model-armor-advanced.yaml](assets/model-armor-advanced.yaml)).

--------------------------------------------------------------------------------

## 11. Known Traps & Gotchas (`known_traps_and_gotchas`)

*   **`network_attachment` is `ForceNew`**: Enabling Semantic Governance
    Policies (SGP) or modifying network attachments after the initial Terraform
    apply will force-recreate the gateway resource. If not managed carefully,
    this can cause dependency deadlocks during destroy operations. Plan
    infrastructure sequencing accordingly.
*   **Authz Policy Limit**: An Agent Gateway allows at most **4 custom
    authorization policies** attached concurrently. Ensure your security posture
    consolidates rules within this limit.
