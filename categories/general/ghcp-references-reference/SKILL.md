---
name: ghcp-references-reference
description: "Skill: ghcp-references-reference"
license: MIT
tags: [general]
---

# Reference Index

| File | Brief description |
| --- | --- |
| empty-strings-handling.md | Oracle treats '' as NULL; PostgreSQL keeps empty strings distinct—patterns to align behavior in code, tests, and migrations. |
| no-data-found-exceptions.md | Oracle SELECT INTO raises "no data found"; PostgreSQL doesn’t—add explicit NOT FOUND handling to mirror Oracle behavior. |
| oracle-parentheses-from-clause.md | Oracle allows `FROM(TABLE_NAME)` syntax; PostgreSQL requires `FROM TABLE_NAME`—remove unnecessary parentheses around table names. |
| oracle-to-postgres-sorting.md | How to preserve Oracle-like ordering in PostgreSQL using COLLATE "C" and DISTINCT wrapper patterns. |
| oracle-to-postgres-to-char-numeric.md | Oracle allows TO_CHAR(numeric) without format; PostgreSQL requires format string—use CAST(numeric AS TEXT) instead. |
| oracle-to-postgres-type-coercion.md | PostgreSQL strict type checks vs. Oracle implicit coercion—fix comparison errors by quoting or casting literals. |
| postgres-concurrent-transactions.md | PostgreSQL allows only one active command per connection—materialize results or use separate connections to avoid concurrent operation errors. |
| postgres-refcursor-handling.md | Differences in refcursor handling; PostgreSQL requires fetching by cursor name—C# patterns to unwrap and read results. |
| oracle-to-postgres-timestamp-timezone.md | CURRENT_TIMESTAMP / NOW() return UTC-normalised timestamptz in PostgreSQL; Npgsql surfaces DateTime.Kind=Unspecified—force UTC at connection open and in application code. |