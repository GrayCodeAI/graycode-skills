---
name: ai-agent-skill-registry
description: "Interacts with an AI agent platform skill registry to search, list, upload, update, and delete agent skills and monitor long-running operations, enabling agents to discover and register capabilities."
license: Apache-2.0
tags:
- agents
- registry
- discovery
- ai
---

# Skill Registry

This skill provides instructions for interacting with the **Skill Registry** on
the Gemini Enterprise Agent Platform.

## Core Capabilities

-   **Skill Discovery** - Query the registry to easily search, list, get
    specific skills, and inspect revision histories.
-   **Skill Lifecycle Management** - Upload, update, or permanently delete
    skills.
-   **Operation Monitoring** - Utility to check the completion status of
    long-running state changes (LROs).
-   **Generate Skill** - Automate the initial scaffolding of new agent skills
    locally.

## Core Directives

-   **Mandatory Validation**: ALWAYS execute the environment validation check
    before performing any operations.

    Before any operation, you **must** validate the core environment.

    ```bash
    # Execute the validation script
    python3 scripts/validate_env.py
    ```

## Prerequisites & Authentication

### Library & Authentication

Ensure you have the latest Google Cloud credentials and libraries installed.

```bash
# Install required libraries
pip install google-auth requests

# Authenticate with Google Cloud
gcloud auth application-default login
```

### Environment Variables

The following variables are required for operations:

-   `GCP_PROJECT_ID`: Your Google Cloud Project ID.
-   `GCP_LOCATION`: The region (e.g., `us-central1`).

--------------------------------------------------------------------------------

## Quickstart

Quickly search for available skills in the registry:

```bash
python3 scripts/skill_registry_ops.py search \
  --query "test skill" \
  --top-k 5
```

--------------------------------------------------------------------------------

## Operations

-   **Skill Discovery**: query-skills.md
-   **Skill Lifecycle**: manage-skills.md
-   **Monitor Operations**:
    monitor-operations.md
-   **Generate Skill**: generate-skill.md
