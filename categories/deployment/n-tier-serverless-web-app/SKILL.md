---
name: n-tier-serverless-web-app
description: "Design and implement secure n-tier serverless web applications with strict private tiers, including Terraform, security checklists, zero-trust networking, and Private Service Connect."
license: Apache-2.0
tags:
- serverless
- architecture
- terraform
- security
- microservices
---

<!-- disableFinding(all) -->
<!-- mdlint off -->

# Secure n-tier serverless web application with strict private application tiers

This skill guides agents through the workflow of designing and implementing a
secure serverless web application with as many architectural design layers as
specified by the user. It uses Cloud Run for the serverless layers and Cloud SQL
for PostgreSQL as the data layer. A three-tier web application might be
represented in three architectural layers: a Cloud Run presentation layer, a
Cloud Run application layer, and a Cloud SQL for PostgreSQL database layer.

The architecture enforces strict physical and network isolation across all tiers (T1 to TN):

*   **Tier 1 presentation tier (frontend / reverse proxy)**: Public-facing UI rendering/gateway service (Cloud Run). Exposes the entry point via Cloud Load Balancing and routes requests downstream to internal tiers privately via Direct VPC Egress.
*   **Tier 2..N application tier (internal microservices / business logic)**: Private application services (Cloud Run). 100% isolated from the internet (Ingress: VPC-internal, `INGRESS_TRAFFIC_INTERNAL_ONLY`), reachable exclusively via upstream VPC routing (`egress = "ALL_TRAFFIC"` with Private Google Access on the subnet for `*.run.app` URLs).
*   **Data tier**: Private Cloud SQL for persistent data and Memorystore for
    Redis for caching, reachable exclusively from authorized application tiers.

## General guidance to the LLM

### 1. Direct Resource Map (Zero-Search File Access)
All necessary reference architectures, HCL templates, and checklists are co-located in this skill. Use exact relative paths from this skill folder:

| Asset Path | Purpose & Usage |
| :--- | :--- |
| `assets/main.tf` | **Single Source of Truth for Terraform (HCL)**. Contains all security boundaries, Cloud Run v2 configs, PSC endpoints, DNS private zones, and firewall rules. |
| `assets/output-template.md` | Standardized Solution Architecture report markdown structure. |
| `references/non-negotiable-architectural-rules.md` | Non-negotiable security rules, audit checklist, and product mappings. |
| `references/related-guidance.md` | Supplemental deep reference (do NOT read for standard design or IaC tasks; read only if specialized edge-case troubleshooting is explicitly required). |

- **No Directory Crawling**: Do NOT run `list_dir` chains down workspace directories to discover these files.
- **No Search Thrashing on Local Files**: Do NOT run `code_search` or `find_by_name` queries to look inside `assets/main.tf`. Read the file directly using `view_file` once and reuse the context.
- **No Redundant Skill Searches**: Do NOT call `skill_search` for serverless or n-tier architecture skills while executing this skill.

### 2. Direct Inline Generation (No Subagent Delegation)
- Perform all architecture compilation, Terraform drafting, `gcloud` command assembly, and validation script generation **directly in the primary conversation**.
- Do **NOT** invoke subagents (`invoke_subagent`) to research external GitHub Terraform modules, probe environment configs, or draft reports. All required patterns are fully contained in `assets/main.tf` and `references/`.

### 3. One-Shot Clean Artifact Writing
- Generate complete, fully-rendered, and valid HCL blocks and Markdown reports in a single `write_to_file` call.
- Avoid leaving placeholders or malformed code fences that require multi-turn `replace_file_content` and `grep_search` patch loops.
- **No Unpopulated Placeholders**: When embedding code or scripts inside architecture reports (e.g., Section 6 of `assets/output-template.md`), always inline the actual complete Terraform code, gcloud commands, and validation script code. Never output literal template placeholder comments (e.g., `# [Paste of main.tf file contents]`).
- **In-Response Direct Rendering (Mandatory)**: Whenever Terraform code, deployment scripts, or architecture reports are requested or generated (e.g., "provide a design and Terraform code", "generate IaC"), you **MUST print the complete generated ```terraform ... ``` HCL code block and full solution report directly in your chat response text**, in addition to writing them to files on disk. Never output only an architectural design summary or file links when code is requested; automated evaluation frameworks (such as Yardstick) evaluate the raw response text and fail all code assertions if the ```terraform``` code block is missing from the message.

### 4. Technical Completeness Checklist
- When providing a concise architecture summary or security checklist (e.g., when instructed not to generate full IaC), you MUST explicitly include the following technical specifications:
    - For regional load balancer deployments: regional proxy-only subnet purpose (`REGIONAL_MANAGED_PROXY`) and `network` parameter on regional forwarding rules.
    - Cloud SQL PostgreSQL version (`POSTGRES_18`), Edition (`Enterprise Edition`), High Availability (`Regional HA`), and Private Service Connect (`psc_enabled = true`).
    - Cloud NGFW Firewall Policies:
        - MUST configure explicit Cloud NGFW network firewall policies (`google_compute_network_firewall_policy`, `google_compute_network_firewall_policy_association`, and `google_compute_network_firewall_policy_rule` with `enable_logging = var.enable_monitoring`) rather than legacy `google_compute_firewall`.
        - Enforce default egress deny (`0.0.0.0/0`).
        - Allow frontend egress to backend / PGA VIPs.
        - Allow backend database egress explicitly permitting TCP port `443` to Private Google Access VIPs (`199.36.153.4/30 / 199.36.153.8/30`) in addition to TCP port `5432` so the Cloud SQL Auth Proxy sidecar can query `sqladmin.googleapis.com` on startup for IAM certificate exchange.

## Workflow

> [!TIP]
> **Optional MCP Server Integration**: If your AI coding client supports the **Model Context Protocol (`MCP`)**, you can connect the [Google Developer Knowledge MCP Server](https://developers.google.com/knowledge/mcp) (`npx -y @google/mcp-developer-knowledge-server`) to dynamically query real-time Google Cloud documentation (`cloud.google.com/docs`) alongside this skill's offline knowledge base (`references/related-guidance.md`).

The solution design and implementation workflow is divided into the following
phases:

*   **Phase 1: Requirements discovery and analysis**: Analyze the workload's
    requirements, constraints, dependencies, and current state.
*   **Phase 2: Solution design & IaC drafting**: Build a technology stack, architecture, and deployment configuration for the workload. **IMPORTANT: You should offer to generate the complete Terraform code (based on `assets/main.tf` and adhering to all Phase 3 specifications) alongside the solution architecture during this phase.** This allows the user to immediately review and iteratively modify the code as the conversation continues. However, if the user explicitly states they do not want code, do not generate it yet.
*   **Phase 3: Implementation plan & iterative refinement**: Modify and refine the generated design and deployment instructins as the conversation and user feedb *   **Frontend Ingress Block**: Verify that direct internet access targeting the Tier 1 Frontend's default `*.run.app` URL is blocked (`HTTP 403 Forbidden` from edge screening).
    *   **Backend Ingress Block**: Verify that direct internet access targeting internal compute tiers' `*.run.app` URLs (`INGRESS_TRAFFIC_INTERNAL_ONLY`) is blocked across all internal microservice tiers (`HTTP 404 Not Found` or `HTTP 403 Forbidden`).
    *   **Frontend Public Access via Application Load Balancer**: Verify that accessing the custom domain routes successfully to the presentation tier via the Application Load Balancer (`HTTP 200` to `399`).
    *   **Edge WAF Protection**: Verify that a simulated SQL injection request (`/?id=1%20OR%201=1` on the custom domain) is intercepted and blocked (`HTTP 403 Forbidden` from Cloud Armor).
    *   **Private Server-to-Server Connectivity**: Verify via Cloud Run application logs (`Logs Explorer`) and database connection pooling telemetry (`Cloud SQL Query Insights`) that tier 1 -> tier 2 -> data tier queries succeed over private VPC fiber (`Direct VPC Egress` + `Private Service Connect` / `Private Services Access`).

2.  **Generate tailored automated validation script**: Rather than relying on a static pre-packaged script, **generate a custom automated validation script** (e.g., self-contained Python validation script using standard built-in `urllib` / `subprocess` libraries, or a cross-platform bash/PowerShell script) customized precisely to the user's deployed domain, SSL certificate name, and exact multi-tier `*.run.app` URIs.

3.  **Provide cross-platform execution guidance**: Explain how the user can execute the generated script across their target OS (`macOS`, `Linux`, `Windows PowerShell`, or zero-install **Google Cloud Shell** (`https://shell.cloud.google.com`)).

4.  **Compile validation report**: Document the validation checks, the generated verification script code, execution commands, and expected outcomes in Section 6.4 ("Solution verification guide and custom automated validation script") inside `assets/output-template.md`.

5.  **Conduct validation and finalize**: Assist the user in running the generated verification script, inspecting logs, and troubleshooting any DNS or WAF propagation issues. Request final approval.
