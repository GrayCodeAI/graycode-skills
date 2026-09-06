---
name: cloud-account-onboarding
description: "Guide a new developer through first cloud setup: tool verification, authentication, project selection or creation, billing linkage, and first-resource deployment, with consent gates."
license: Apache-2.0
tags:
- cloud
- onboarding
- getting-started
- billing
---

# Onboarding to Google Cloud

This skill provides a streamlined, non-interactive "happy path" for a singleton developer to get started with [Google Cloud](https://cloud.google.com/). It covers everything from environment verification and authentication to project selection, billing account linkage, and downstream safety chaining.

> [!IMPORTANT]
> For autonomous agents executing this skill:
> 1. **Check-Before-Mutate Audits**: Always perform silent pre-execution state audits prior to proposing or executing any project or billing changes.
> 2. **Single-Question Policy**: Ask the user for exactly **one** operational parameter or confirmation at a time during interactive execution.
> 3. **Non-Interactive Output**: Append non-interactive overrides (`--quiet`, `--format="json"`) to all mutation commands to guarantee deterministic, machine-parseable outputs and prevent terminal hangs.
> 4. **First Turn Interaction Rules (Trigger Turn)**: When the developer first triggers this skill with a general onboarding request (e.g. says "I want to get started with Google Cloud"):
>    - **Preamble Guidance**: Proactively include a short orienting preamble guiding the developer to create a Google Cloud account (pointing to the console at `https://console.cloud.google.com/`) and run `gcloud auth login` to authorize their workstation, even if they appear to be already logged in.
>    - **First Turn Single-Question**: Perform pre-flight audits silently, but do not present a complete parameters summary table or ask for final consent in the first turn. Instead, ask the developer exactly **one** initial operational question (e.g., *"Would you like to reuse an existing active project, or create a brand new one?"*).
>    *Note: If the developer's initial prompt explicitly states "I approve the onboarding configuration", "Let's proceed with onboarding", or requests a dry-run plan (e.g., "Show me the exact plan or dry-run commands"), bypass the general preamble and initial question, and proceed directly to the requested step.*

---

## Overview

For an individual developer, onboarding to Google Cloud involves verifying local terminal tools, establishing an authenticated session, selecting or instantiating a workspace ([Project](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy.md.txt)), and linking it to an active billing account. Google Cloud offrs a Free Tier 