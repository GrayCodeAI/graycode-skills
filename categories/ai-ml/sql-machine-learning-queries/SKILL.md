---
name: sql-machine-learning-queries
description: "Runs machine learning and generative AI directly in SQL, including forecasting, anomaly detection, classification, semantic search, embeddings, summarization, and translation."
license: Apache-2.0
tags:
- sql
- machine-learning
- genai
- analytics
---

# BigQuery AI & ML

BigQuery integrates with Vertex AI to provide powerful machine learning and
generative AI capabilities directly within SQL queries using built-in functions
like `AI.FORECAST`, `AI.KEY_DRIVERS`, `AI.DETECT_ANOMALIES`, and `AI.GENERATE`.

## Reference Directory

-   **Functions Reference**:

    -   **AI.AGG**: ai_agg.md - Multi-row semantic
        aggregation and summarization.
    -   **AI.CLASSIFY**: ai_classify.md - Classify
        text.
    -   **AI.DETECT_ANOMALIES**:
        ai_detect_anomalies.md - Detect
        anomalies.
    -   **AI.EVALUATE**: ai_evaluate.md - Evaluate
        models.
    -   **AI.FORECAST**: ai_forecast.md -
        Time-series forecasting.
    -   **AI.GENERATE**: ai_generate.md - Generate
        text using LLMs.
    -   **AI.GENERATE_EMBEDDING**:
        ai_generate_embedding.md -
        Generate embeddings.
    -   **AI.GENERATE_TABLE**:
        ai_generate_table.md - Table-valued
        AI generation.
    -   **AI.IF**: ai_if.md - Evaluate semantic
        conditions.
    -   **AI.KEY_DRIVERS**: ai_key_drivers.md -
        Identifies key drivers, this is a TVF.
    -   **AI.SCORE**: ai_score.md - Score data.
    -   **AI.SEARCH**: ai_search.md - Semantic
        search.
    -   **AI.SIMILARITY**: ai_similarity.md -
        Semantic similarity.
    -   **Remote Models**: remote_models.md -
        Working with remote models (Vertex AI).
    -   **CONTRIBUTION_ANALYSIS**:
        ml_contribution_analysis.md
        -   Finds contributing factors, key drivers of change. Requires creating
            a MODEL entity.
    -   **VECTOR_SEARCH**: vector_search.md -
        Vector search best practices.

## Related Skills

-   BigQuery Basics Skill: SKILL.md file for core BigQuery
    concepts, resource management, CLI, and client libraries.
