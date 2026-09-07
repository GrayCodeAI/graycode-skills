---
name: data-ingestion-api-setup
description: "Install client and utility libraries and set up authentication for a data manager API. Use when getting started with the API, installing the client library, or setting up local environment access."
license: Apache-2.0
tags:
- api
- data
- setup
- authentication
---

# Data Manager API Setup

## Setup Authentication

Refer to [Set up API access](https://developers.google.com/data-manager/api/devguides/quickstart/set-up-access.md.txt)
for more details.

1.  **Enable API (Prerequisite)**: Check that the user has enabled the Data
    Manager API in their Google Cloud project.
2.  **Generate ADC**: Authenticate the local workspace using Application
    Default Credentials (ADC) via `gcloud auth application-default login`.
    *   **Required Scopes**: Include scopes
        `https://www.googleapis.com/auth/datamanager` and
        `https://www.googleapis.com/auth/cloud-platform`.
    *   **Multi-API Scopes**: If using the same credentials for other APIs,
        append their scopes (e.g.,
        `https://www.googleapis.com/auth/adwords`).
    *   **Service Accounts**: Ensure the Service Account has the
        `Service Usage Consumer` IAM role, and the user executing `gcloud`
        has the Token Creator role
        (`roles/iam.serviceAccountTokenCreator`) on that Service Account
        for impersonation.

## Install Client & Utility Libraries

Refer to [Install a client library](https://developers.google.com/data-manager/api/devguides/quickstart/install-library.md.txt)
for more details.

The companion utility libraries provide pre-built helper classes
and functions to correctly format, hash, and encrypt user identifiers (such as
emails, phone numbers, and physical addresses) prior to API ingestion. Use of
these libraries is highly recommended to ensure that user identifier formatting
matches the API's specifications.

Select the language-specific installation guide below:

*   Python Setup Reference (packages: `google-ads-datamanager` and `google-ads-datamanager-util`)
*   Java Setup Reference (packages: `com.google.api-ads:data-manager` and `data-manager-util`)
*   Node Setup Reference (packages: `@google-ads/datamanager` and `@google-ads/data-manager-util`)
*   PHP Setup Reference (packages: `googleads/data-manager` and `googleads/data-manager-util`)
*   .NET Setup Reference (packages: `Google.Ads.DataManager.V1` and `Google.Ads.DataManager.Util.csproj`)
