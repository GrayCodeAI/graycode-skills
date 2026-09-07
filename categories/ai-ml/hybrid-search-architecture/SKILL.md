---
name: hybrid-search-architecture
description: "Designs dynamic hybrid search systems combining semantic and keyword search with vector indexing, SQL filtering, faceted attributes, reranking, and in-database AI validation."
license: Apache-2.0
tags:
- hybrid-search
- vector-search
- rag
- architecture
- sql
---

# Dynamic Hybrid Search using AlloyDB

This skill provides a workflow to design and implement secure, low-latency, and
high-accuracy hybrid search solutions combining structured dataset filtering,
vector search indexing, faceted metadata filtering, semantic reranking, recall
evaluation, in-database AI validation, database abstraction layers, and
serverless application hosting.

## Overview of the workflow

The workflow consists of the following phases:

1. **Requirements discovery**. Gather detailed requirements related to
  the cloud workload or use case that the user needs assistance for.
2. **Solution architecture**. Use the requirements that were gathered
  in Phase 1 to generate a detailed solution architecture for the cloud
  workload or use case.
3. **Solution validation**. Create a plan to validate the generated
  solution, generate validation instructions and scripts, and run the
  validation.
4. **Solution packaging and presentation**. Consolidate the generated
  content and present the solution.

**Important notes about the workflow**:

- **Strict phase separation**: During Phase 1 (Requirements discovery), when you
  ask the user clarifying questions, DON'T recommend, propose, or outline any
  architectural designs, cloud services, or component mappings. This prevents
  premature architecture commitments or hallucinations before the full scope is
  understood.
- **Halting for approval**: For any step where you are instructed
  to "obtain approval before proceeding", you MUST stop executing, present the
  completed tasks to the user, and wait for their explicit approval. You MUST
  NOT proceed to execute any subsequent tasks or generate any further guidance
  in that response.
- **Ground all generated content**: For all tasks across all phases, you MUST
  first look in the following resources:
  - Product Mappingdeployment guidance with the user.

## Phase 3: Solution validation

### Task 3.1: Pre-deployment validation

- [ ] **Step 1**: Create a pre-deployment plan to statically validate the
  generated solution and verify that it meets the workload requirements
  without provisioning live resources:
  - **Deployment dry-run**: Validate infrastructure syntax and preview the
    resources that will be provisioned using dry-run commands (e.g.,
    `terraform plan` or (where supported) `gcloud ... --dry-run`).
  - **Architecture & policy analysis**: Perform static verification of
    network routing topologies, firewall rules, and IAM enforcement against
    best practices.
- [ ] **Step 2**: Present the static validation plan to the user, obtain
  approval (the user MUST explicitly say "yes" or "I approve"), and execute the
  dry-run commands.
- [ ] **Step 3**: Troubleshoot and fix any errors or policy discrepancies
  identified during dry-run checks until validation succeeds.
- [ ] **Step 4**: Proceed to Task 3.2

### Task 3.2: Runtime validation (Post-deployment)

- [ ] **Step 1**: Ask the user whether they choose to deploy the infrastructure
  now to perform live runtime verification, or skip directly to Phase 4.
- [ ] **Step 2**: **If the user chooses to deploy the infrastructure**:
  - After the user deploys the infrastructure, generate runtime
    verification commands (using tools like `curl`, `ping`, or `gcloud`)
    and provide them to the user to execute, to test live endpoint
    reachability, networking paths, and load balancer routing.
  - Troubleshoot any deployment or runtime routing issues until checks pass.
- [ ] **Step 3**: Proceed to Phase 4.

## Phase 4: Solution packaging and presentation

- [ ] **Step 1**: Consolidate the final text artifacts that were generated in
  Phase 2 into a single Markdown file named `solution-architecture-guide.md`,
  based on the template in Output Template.
- [ ] **Step 2**: Request the user's permission to write the code files in the
  user's workspace.
- [ ] **Step 3**: After the user gives permission, write the final code files in
  the user's workspace.
