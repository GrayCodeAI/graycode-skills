---
name: distributed-sql-database
description: "Provision instances and databases, design performant schemas, and query a horizontally scalable relational database. Use when choosing primary keys, writing SQL, or diagnosing performance."
license: Apache-2.0
tags:
- database
- sql
- schema-design
- performance
---

# Spanner Basics

This skill provides core workflows and guidance for administering and developing with Google Cloud Spanner, a fully managed, mission-critical database service offering global transactional consistency and automatic, synchronous replication for high availability.

## Core Principles

-   **Performance First:** Spanner scales horizontally. Efficiency is tied to
    Primary Key design. Always warn against using monotonically increasing/decreasing
    values (like sequential timestamps) as the first part of a primary key to avoid hotspots.
-   **Schema Design:** Prefer interleaved tables for strongly related parent-child data
    that is frequently accessed together.

## Safety

> [!CAUTION] **CRITICAL INSTRUCTION:** You MUST obtain explicit user confirmation before making any non-emulator database changes (DML or DDL) or destructive operations (such as dropping tables, indexes, or any other Spanner resources). Do not execute them automatically; instead, output the command (e.g., `gcloud spanner databases ddl update`) and ask for explicit user approval.
> When database access is unavailable or authentication fails, do not block on trying to verify the existence of the instance, database, or table. Assume the provided resources exist and directly generate the DDL commands.

## Common Workflows

### Schema Evolution & DDL

1.  Use `gcloud spanner databases ddl update` to apply schema updates (such as CREATE, ALTER, or DROP tables and indexes).
2.  Reference schema-design.md for guidelines on primary key selection and interleaved tables.

### Diagnosing Performance Issues

1.  Use `SPANNER_SYS` tables to identify slow or resource-intensive queries.
2.  For example, query `SPANNER_SYS.QUERY_STATS_TOP_HOUR` to find queries with the highest CPU usage.

## Reference Directory

- Core Concepts: Explanation of Spanner internals, architecture, and design.
- CLI Usage: Essential `gcloud spanner` command-line operations for managing instances and databases.
- IAM Security: Roles, permissions, and data governance best practices for Spanner.
- Client Library Usage: Using Google Cloud client libraries for Spanner (Java, Go, Python, Node.js).
- Terraform Usage: Infrastructure as Code examples for provisioning Spanner instances and databases.
- MCP Usage: Using the Spanner remote MCP server.
- PostgreSQL Dialect: Best practices and examples for using the PostgreSQL interface in Spanner.
- Schema Design: Guidelines on primary key selection and interleaved tables for performance.

If you need product information that's not found in these references, use the
`search_documents` tool of the Developer Knowledge MCP server.
