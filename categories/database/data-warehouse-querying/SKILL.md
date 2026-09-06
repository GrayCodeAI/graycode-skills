---
name: data-warehouse-querying
description: "Manages datasets, tables, and jobs in a serverless data warehouse, running SQL queries and performing basic data ingestion and analysis."
license: Apache-2.0
tags:
- database
- data-warehouse
- sql
- analytics
---

# BigQuery Basics

BigQuery is a serverless, AI-ready data platform that enables high-speed
analysis of large datasets using SQL and Python. Its disaggregated architecture
separates compute and storage, allowing them to scale independently while
providing built-in machine learning, geospatial analysis, and business
intelligence capabilities.

## Setup and Basic Usage

1.  **Enable the BigQuery API:**

    ```bash
    gcloud services enable bigquery.googleapis.com --quiet
    ```

2.  **Create a Dataset:**

    ```bash
    bq mk --dataset --location=US my_dataset
    ```

3.  **Create a Table:**

    Create a file named `schema.json` with your table schema:

    ```json
    [
      {
        "name": "name",
        "type": "STRING",
        "mode": "REQUIRED"
      },
      {
        "name": "post_abbr",
        "type": "STRING",
        "mode": "NULLABLE"
      }
    ]
    ```

    Then create the table with the `bq` tool:

    ```bash
    bq mk --table my_dataset.mytable schema.json
    ```

4.  **Run a Query:**

    ```bash
    bq query --use_legacy_sql=false \
    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` \
    WHERE state = "TX" LIMIT 10'
    ```

## Reference Directory

- Core Concepts: Storage types, analytics
  workflows, and BigQuery Studio features.

- Change History: Tracking and querying
  incremental table changes using APPENDS and CHANGES.

-   Continuous Queries: Running continuous
    SQL statements to analyze incoming data in real time.

- CLI Usage: Essential `bq` command-line tool
  operations for managing data and jobs.

- Client Libraries: Using Google Cloud
  client libraries for Python, Java, Node.js, and Go.

- MCP Usage: Using the BigQuery remote MCP server and
  Gemini CLI extension.

- Infrastructure as Code: Terraform examples for
  datasets, tables, and reservations.

- IAM & Security: Roles, permissions, and data
  governance best practices.

*If you need product information not found in these references, use the
Developer Knowledge MCP server `search_documents` tool.*

## Related Skills

- BigQuery AI & ML Skill:
  SKILL.md file for BigQuery AI and ML capabilities (forecast, anomaly
  detection, text generation).
