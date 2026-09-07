---
name: retrieval-augmented-generation
description: "Designs and optimizes Retrieval Augmented Generation systems: ingestion, chunking, embeddings, vector indexing, retrieval, reranking, prompt construction, and evaluation."
license: MIT
tags:
- rag
- llm
- embeddings
- vector-database
- ai
---

# Skills

Complete framework for an AI agent to architect, implement, and iteratively improve a production-grade Retrieval Augmented Generation pipeline from initial requirements through deployment and continuous optimization.

## When to use

- Designing a new RAG system architecture from scratch
- Building a knowledge retrieval pipeline that feeds context into an LLM
- Creating or selecting a vector database and search system for document retrieval
- Implementing document ingestion, chunking, and embedding workflows
- Improving an existing RAG system that suffers from poor retrieval quality, hallucinations, or latency issues
- Reducing hallucinations in a knowledge-based AI system by grounding responses in retrieved evidence
- Integrating external or enterprise knowledge sources (documents, databases, APIs) into AI-generated responses
- Evaluating retrieval accuracy, ranking quality, or end-to-end answer correctness of a RAG pipeline
- Optimizing context window usage, retrieval speed, or embedding efficiency in a live RAG deployment
- Migrating a naive "stuff all documents into the prompt" approach to a scalable retrieval-based architecture

## Instructions

### Phase 1 — Problem and Knowledge Understanding

1. **Define the system's purpose.** Write a single sentence that states what question or task the RAG system must answer or perform. Example: "Answer customer support questions using the product knowledge base."

2. **Profile the end users.** List who will query the system, what language they use, their expertise level, and whether queries will be short keyword searches, full natural-language questions, or multi-turn conversations.

3. **Catalog expected query patterns.** Create a representative list of at least 20 example queries spanning simple factual lookups, comparative questions, procedural how-to requests, and ambiguous or under-specified questions.

4. **Define expected answer characteristics.** For each query category, specify the ideal answer length, whether citations are required, whether the answer should be extractive (verbatim from source) or abstractive (synthesized), and acceptable confidence thresholds.

5. **Identify hard constraints.** Document maximum acceptable latency (e.g., < 2 seconds), data privacy requirements, deployment environment (cloud, on-premise, edge), budget limits, and any compliance or regulatory restrictions on data handling.

---

### Phase 2 — Knowledge Source Planning

6. **Inventory all knowledge sources.** Create a table with columns: Source Name, Type (structured / semi-structured / unstructured), Format (PDF, HTML, DOCX, CSV, SQL database, REST API, wiki, etc.), Estimated Size, Update Frequency, Access Method, and Sensitivity Level.

7. **Classify sources by authority and freshness.** Assign each source a priority tier:
   - **Tier 1 — Authoritative & frequently updated:** official docs, product databases, policy documents.
   - **Tier 2 — Supplementary & moderately updated:** blog posts, FAQs, internal wikis.
   - **Tier 3 — Archival & rarely updated:** legacy manuals, historical reports.

8. **Design the data ingestion workflow for each source.**
   - For file-based sources: define a file-watch or scheduled-pull mechanism, specify parsers (e.g., Apache Tika for PDFs, Unstructured.io, LlamaParse, or custom parsers).
   - For database sources: define SQL queries or ORM extractions, schedule refresh intervals.
   - For API sources: define endpoint calls, pagination handling, authentication, rate-limit management, and response-to-document transformation logic.
   - For web sources: define crawling scope, robots.txt compliance, and HTML-to-text extraction.

9. **Plan incremental ingestion.** Implement change-detection logic (file hash comparison, database CDC, API pagination cursors, or last-modified timestamps) so only new or modified content is re-processed on each run.

---

### Phase 3 — Document Processing

10. **Extract raw text.** For each document format, apply the appropriate parser:
    - PDF → use a layout-aware parser (e.g., PyMuPDF, pdfplumber, or LlamaParse) that preserves tables, headers, and reading order.
    - HTML → strip tags, retain semantic structure (headings, lists, tables).
    - DOCX → extract text, tables, and metadata via python-docx or equivalent.
    - Markdown → preserve heading hierarchy.
    - Images/scanned PDFs → apply OCR (Tesseract, Amazon Textract, or Azure Document Intelligence).

11. **Clean and normalize text.**
    - Remove headers, footers, page numbers, watermarks, and boilerplate repeated across pages.
    - Normalize Unicode characters, collapse excessive whitespace, and fix encoding issues.
    - Standardize date formats, units, and abbreviations relevant to the domain.
    - Retain meaningful formatting cues: convert tables to Markdown tables or structured JSON; preserve bullet/numbered lists.

12. **Enrich documents with metadata.** For every document, attach metadata fields: `source_id`, `source_name`, `document_title`, `section_heading`, `page_number`, `author`, `created_date`, `last_modified_date`, `language`, `tier` (from Step 7), and any domain-specific tags (product name, category, version).

13. **Choose a chunking strategy.** Select one or a combination of the following based on document structure:

    | Strategy | When to Use | Typical Chunk Size |
    |---|---|---|
    | **Fixed-size with overlap** | Homogeneous plain-text documents | 256–512 tokens, 10–20 % overlap |
    | **Recursive character splitting** | General-purpose fallback | 500–1000 chars, split on `\n\n` → `\n` → `. ` → ` ` |
    | **Semantic / paragraph-based** | Well-structured documents with clear paragraphs | Variable, one semantic unit per chunk |
    | **Section / heading-based** | Documents with hierarchical headings (Markdown, HTML, DOCX) | One section per chunk, split further if section exceeds 512 tokens |
    | **Sentence-window** | When surrounding context is needed at retrieval time | Central sentence as retrieval unit; expand to surrounding window at context-construction time |
    | **Parent-child / hierarchical** | Long documents where a small chunk may lack context | Small child chunks for retrieval, linked to larger parent chunks for context |
    | **Table-aware** | Documents containing data tables | Each table as a standalone chunk with caption and column headers |

14. **Implement chunking.**
    - Apply the chosen strategy using a framework (LangChain TextSplitters, LlamaIndex NodeParsers, or custom code).
    - Preserve chunk-to-document lineage: each chunk must carry `chunk_id`, `document_id`, `chunk_index`, `parent_chunk_id` (if hierarchical), and all document-level metadata from Step 12.
    - Prepend contextual headers to each chunk: include the document title and section heading at the top of the chunk text so the embedding captures topical context. Example: `"Document: Product Manual v3.2 | Section: Troubleshooting Wi-Fi Issues\n\n<chunk text>"`.

15. **Validate chunks.** Scan all chunks and verify:
    - No chunk exceeds the embedding model's maximum token input.
    - No chunk is shorter than 50 tokens (merge very short chunks with neighbors).
    - Tables and code blocks are not split mid-row or mid-block.
    - Overlap regions do not start or end mid-sentence.

---

### Phase 4 — Embedding Strategy

16. **Select an embedding model.** Use the following decision guide:

    | Criterion | Recommendation |
    |---|---|
    | General English text, cloud OK | `text-embedding-3-large` (OpenAI) or `voyage-3-large` (Voyage AI) |
    | Multilingual content | `multilingual-e5-large-instruct` or `Cohere embed-multilingual-v3.0` |
    | On-premise / open-source required | `BAAI/bge-large-en-v1.5`, `nomic-embed-text-v1.5`, or `e5-mistral-7b-instruct` |
    | Code or technical documentation | `voyage-code-3` or `text-embedding-3-large` fine-tuned on code |
    | Extremely low latency required | `text-embedding-3-small` (OpenAI) or a distilled model like `bge-small-en-v1.5` |
    | Domain-specific (legal, medical, finance) | Fine-tune `bge-large` or `e5-large` on domain Q&A pairs |

    Record the model name, dimensionality, max token input, and normalization requirements.

17. **Generate embeddings.**
    - Batch chunks (typically 64–256 per batch) and call the embedding model API or run local inference.
    - Normalize embedding vectors to unit length if the model does not do so by default and cosine similarity will be used.
    - Store raw chunk text alongside its embedding vector and all metadata.

18. **Generate query embeddings consistently.** Use the same embedding model and any query-specific prefixes or instructions (e.g., `"query: "` prefix for E5 models, `"search_query: "` for Nomic) to ensure the query embedding lives in the same vector space as document embeddings.

---

### Phase 5 — Indexing and Storage

19. **Choose a vector database.** Use the following decision guide:

    | Criterion | Recommended System |
    |---|---|
    | Managed cloud, minimal ops | Pinecone, Weaviate Cloud, Zilliz Cloud |
    | Open-source, self-hosted | Qdrant, Milvus, Weaviate, Chroma, pgvector (PostgreSQL) |
    | Already using PostgreSQL | pgvector extension or pgvecto.rs |
    | Serverless / low-volume prototyping | Chroma (in-process), LanceDB, FAISS (flat file) |
    | Hybrid search (vector + keyword) required | Weaviate, Qdrant, Elasticsearch with dense-vector, OpenSearch |
    | Multi-tenant enterprise | Pinecone with namespaces, Qdrant with collection aliases, Weaviate with tenants |

20. **Design the index schema.** Define:
    - **Collection / index name**: one per knowledge domain or tenant.
    - **Vector field**: dimensionality matching the embedding model output.
    - **Metadata fields**: all fields from Step 12 plus `chunk_id`, `chunk_index`, `parent_chunk_id`, `chunk_text` (or store text in a sidecar document store if the vector DB has payload size limits).
    - **Distance metric**: cosine similarity (most common), dot product (if embeddings are normalized), or L2 (Euclidean) for specific models.

21. **Configure the index type.**
    - For < 100 K vectors: flat (brute-force) index is acceptable.
    - For 100 K – 10 M vectors: HNSW index with `ef_construction` = 200, `M` = 16 as starting parameters.
    - For > 10 M vectors: IVF-PQ or SCANN for memory efficiency; benchmark recall vs. latency.

22. **Upsert embeddings.** Load all chunk embeddings and metadata into the vector database. Use batch upsert operations. Record the total vector count and index build time.

23. **Plan index maintenance.**
    - Define a pipeline that triggers on new/updated documents: re-chunk → re-embed → upsert new vectors → delete vectors for removed/replaced chunks.
    - Schedule periodic full re-indexing (e.g., weekly) to catch drift and ensure consistency.
    - Implement vector ID generation that is deterministic from `document_id + chunk_index` so upserts are idempotent.

---

### Phase 6 — Retrieval Design

24. **Implement semantic (dense) retrieval.** Build the baseline retrieval path:
    - Accept user query → embed with query embedding model (Step 18) → search vector DB → return top-k results with scores and metadata.
    - Set initial `k` = 20 (retrieve more than needed; downstream re-ranking will narrow).

25. **Implement keyword (sparse) retrieval.** Set up a parallel retrieval path:
    - Index chunk text in a full-text search engine (Elasticsearch, OpenSearch, or the vector DB's built-in BM25 capability).
    - Execute BM25 search on the same query → return top-k results.

26. **Implement hybrid retrieval.** Combine dense and sparse results:
    - Use Reciprocal Rank Fusion (RRF): for each chunk, compute `RRF_score = Σ 1 / (k_constant + rank_in_list)` across both lists. Use `k_constant` = 60 as default.
    - Alternatively, use a weighted linear combination of normalized dense and sparse scores: `hybrid_score = α * dense_score + (1 - α) * sparse_score`. Start with `α` = 0.7.
    - Return the top-N fused results (N = 10–20).

27. **Implement query preprocessing.**
    - **Query cleaning**: strip special characters, fix typos (optional spell-check), normalize whitespace.
    - **Query expansion**: use the LLM to generate 2–3 alternative phrasings of the user query; embed each and retrieve separately, then merge result sets before fusion. Prompt: `"Rewrite the following question in 3 different ways while preserving the original meaning:\nQuestion: {query}"`.
    - **Query decomposition** (for complex multi-part questions): use the LLM to break the query into sub-questions; retrieve for each sub-question independently, then merge context. Prompt: `"Break the following complex question into independent sub-questions:\nQuestion: {query}"`.
    - **Query classification**: classify the query intent (factual lookup, comparison, procedural, opinion, out-of-scope) to route to appropriate retrieval strategies or to reject out-of-scope queries early.

28. **Implement metadata filtering.** Before or during vector search, apply metadata filters when the query contains explicit constraints:
    - Date filters: "after January 2024" → filter `last_modified_date >= 2024-01-01`.
    - Source filters: "from the admin guide" → filter `source_name == "Admin Guide"`.
    - Category filters: use an LLM or rule-based classifier to extract filter parameters from the query.

---

### Phase 7 — Ranking and Filtering

29. **Apply cross-encoder re-ranking.** Take the top-N candidates from hybrid retrieval and re-score each using a cross-encoder model:
    - Recommended models: `cross-encoder/ms-marco-MiniLM-L-12-v2` (fast), `BAAI/bge-reranker-v2-m3` (accurate, multilingual), or Cohere Rerank API.
    - Input: `(query, chunk_text)` pairs → output: relevance score.
    - Sort by cross-encoder score descending.

30. **Apply score thresholding.** Remove any chunk whose re-ranker score falls below a minimum relevance threshold. Determine the threshold empirically: start at the 30th percentile score across a test set and adjust based on evaluation.

31. **Remove redundant chunks.** Deduplicate near-identical chunks:
    - Compute pairwise cosine similarity among the remaining chunks.
    - If two chunks have cosine similarity > 0.92, keep only the one with the higher re-ranker score.
    - Alternatively, apply Maximal Marginal Relevance (MMR) with `λ` = 0.7 to balance relevance and diversity.

32. **Select final context chunks.** From the re-ranked, filtered, deduplicated list, select the top-K chunks that will be passed to the LLM. Determine K by token budget:
    - Calculate the total token budget for context = (model max context window) – (system prompt tokens) – (query tokens) – (reserved output tokens).
    - Greedily add chunks in re-ranker-score order until the token budget is reached.
    - Typical final K: 3–8 chunks for most use cases.

---

### Phase 8 — Context Construction

33. **Format retrieved chunks into a structured context block.** Use a consistent template:

    ```
    [Source 1]
    Title: {document_title}
    Section: {section_heading}
    Source: {source_name}
    Date: {last_modified_date}
    Content:
    {chunk_text}

    [Source 2]
    Title: {document_title}
    Section: {section_heading}
    Source: {source_name}
    Date: {last_modified_date}
    Content:
    {chunk_text}

    ...
    ```

    Number each source sequentially so the LLM can reference them by number in citations.

34. **Order chunks strategically.** Place the most relevant chunk first, then alternate if there are chunks from different sources to provide balanced perspective. If the LLM is known to exhibit "lost in the middle" attention bias, place the most critical chunks at the beginning and end of the context block.

35. **Expand context if using sentence-window or parent-child chunking.** Replace retrieved child/sentence chunks with their parent/window chunks to give the LLM full surrounding context. Re-check token budget after expansion.

36. **Handle insufficient retrieval.** If fewer than 2 chunks pass the relevance threshold, or all re-ranker scores are very low:
    - Flag the query as "low-confidence retrieval."
    - Include a metadata signal in the prompt telling the LLM that retrieved evidence is weak.
    - Instruct the LLM to state that it could not find sufficient information rather than guessing.

---

### Phase 9 — Prompt Construction

37. **Design the system prompt.** The system prompt must contain:
    - **Role definition**: "You are a [domain] assistant that answers questions using ONLY the provided reference sources."
    - **Grounding instruction**: "Base your answer strictly on the information in the sources below. Do not use prior knowledge. If the sources do not contain the answer, say 'I don't have enough information to answer this question.'"
    - **Citation instruction**: "Cite your sources by referencing [Source N] after each claim."
    - **Formatting instruction**: specify desired answer format (paragraph, bullet list, table, step-by-step).
    - **Hallucination guard**: "Do not invent facts, statistics, URLs, or quotes not present in the sources."
    - **Tone and length guidance**: match the user profile from Step 2.

38. **Construct the full prompt.** Assemble in this order:
    1. System prompt (Step 37).
    2. Context block (Step 33): prefixed with `"### Reference Sources"`.
    3. User query: prefixed with `"### User Question"`.
    4. Answer instruction: `"### Answer\nProvide a clear, evidence-based answer with citations."`.

39. **Manage multi-turn conversations.** If the RAG system supports dialogue:
    - Maintain a conversation history buffer (last 5–10 turns).
    - Before retrieval, use the LLM to generate a standalone query from the latest user message + conversation history. Prompt: `"Given the conversation history below, rewrite the user's latest message as a standalone question.\n\nHistory:\n{history}\n\nLatest message: {message}\n\nStandalone question:"`.
    - Use the standalone question for retrieval; include conversation history in the prompt only if token budget allows.

---

### Phase 10 — Response Generation

40. **Call the LLM.** Send the assembled prompt to the generation model. Recommended settings:
    - `temperature` = 0.0–0.2 (low, for factual grounding).
    - `max_tokens` = set to expected answer length + 20 % buffer.
    - `top_p` = 0.9.
    - Select a model appropriate for the task: GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B, Mistral Large, or domain-fine-tuned model.

41. **Post-process the response.**
    - Verify that citations (e.g., `[Source 1]`) reference valid source numbers from the context block.
    - Remove any hallucinated source references (references to source numbers not in the context).
    - If the answer contains "I don't have enough information," return the response with a flag indicating low confidence so the application layer can offer fallback options (e.g., escalate to a human).

42. **Attach source metadata to the response.** Return a structured response object:
    ```json
    {
      "answer": "...",
      "citations": [
        {
          "source_number": 1,
          "document_title": "...",
          "section": "...",
          "source_name": "...",
          "url_or_path": "...",
          "relevance_score": 0.93
        }
      ],
      "confidence": "high | medium | low",
      "retrieval_metadata": {
        "chunks_retrieved": 15,
        "chunks_after_rerank": 5,
        "retrieval_latency_ms": 120
      }
    }
    ```

---

### Phase 11 — Evaluation and Improvement

43. **Build an evaluation dataset.** Create or curate at minimum 50 question-answer-context triples:
    - **Question**: representative user query.
    - **Gold answer**: the correct answer written by a domain expert.
    - **Gold context**: the document passages that contain the answer.

44. **Evaluate retrieval quality.** For each test question, run the retrieval pipeline and measure:
    - **Recall@K**: fraction of gold context chunks present in the top-K retrieved chunks. Target ≥ 0.90.
    - **MRR (Mean Reciprocal Rank)**: average of `1 / rank_of_first_relevant_chunk`. Target ≥ 0.80.
    - **Precision@K**: fraction of top-K chunks that are relevant. Track to ensure re-ranking is effective.

45. **Evaluate answer quality.** For each test question, generate an answer and measure:
    - **Faithfulness**: does the answer contain only claims supported by the retrieved context? Use an LLM-as-judge prompt: `"Given the context and the answer, list any claims in the answer not supported by the context."` Target: 0 unsupported claims.
    - **Answer relevance**: does the answer address the question? Use an LLM-as-judge or compute semantic similarity between answer and gold answer.
    - **Correctness**: compare generated answer to gold answer using ROUGE-L, BERTScore, or LLM-as-judge. Target depends on domain.

46. **Detect hallucinations systematically.**
    - Run faithfulness evaluation (Step 45) on all test queries.
    - Flag any answer where the LLM introduces entities, numbers, dates, or claims absent from the retrieved context.
    - Categorize hallucination types: fabricated facts, wrong attribution, over-generalization, invented URLs/references.

47. **Diagnose and fix failures.** For each failed test case, trace the root cause:

    | Symptom | Likely Root Cause | Fix |
    |---|---|---|
    | Correct passage not retrieved | Poor chunking or embedding mismatch | Re-chunk with better boundaries; try a different embedding model; add query expansion |
    | Correct passage retrieved but ranked low | Weak re-ranking | Switch to a stronger cross-encoder; adjust hybrid search weights |
    | Correct passage in context but LLM ignores it | Prompt issue or context too long | Move passage higher in context; shorten total context; strengthen grounding instruction |
    | LLM fabricates an answer | No relevant passage exists or grounding instruction too weak | Add explicit "say I don't know" instruction; lower temperature; add a faithfulness check step |
    | Answer is correct but lacks citation | Citation instruction unclear | Make citation format more explicit in system prompt; provide a one-shot example |

48. **Iterate.** After applying fixes, re-run the full evaluation suite. Repeat until retrieval recall ≥ 0.90 and faithfulness = 100 % on the test set.

---

### Phase 12 — System Optimization

49. **Optimize retrieval latency.**
    - Benchmark end-to-end latency (query embedding time + vector search time + re-ranking time).
    - If embedding latency is high: use a smaller/distilled embedding model or cache frequent query embeddings.
    - If vector search is slow: tune HNSW `ef_search` parameter (lower = faster but less accurate), add metadata pre-filters to reduce search scope, or shard the index.
    - If re-ranking is slow: reduce the number of candidates passed to the cross-encoder (e.g., from 20 to 10), or use a smaller cross-encoder model.

50. **Optimize context size.**
    - Measure answer quality at different context sizes (3, 5, 8, 10 chunks).
    - Find the point of diminishing returns where adding more chunks no longer improves answer quality.
    - Set K to that optimal value to minimize token cost and latency without sacrificing quality.

51. **Optimize embedding and storage costs.**
    - If using a high-dimensional model (e.g., 3072-d), test whether reducing dimensionality (e.g., via Matryoshka embeddings or PCA to 1024-d or 512-d) preserves retrieval quality.
    - Enable scalar quantization in the vector DB if supported (e.g., Qdrant, Milvus) to reduce memory footprint with minimal recall loss.

52. **Implement caching.**
    - Cache embedding vectors for repeated or near-identical queries using a semantic cache (hash of query or nearest-neighbor lookup in a small query cache index).
    - Cache full responses for identical queries with a TTL matching the knowledge update frequency.

53. **Set up monitoring and alerting.**
    - Log every query, retrieved chunks, re-ranker scores, final answer, and latency.
    - Track retrieval score distributions over time; alert if average top-1 similarity drops below a threshold (indicates index staleness or query distribution shift).
    - Track user feedback (thumbs up/down, escalation rate) as a proxy for answer quality.
    - Schedule weekly automated evaluation runs on the test set to detect regressions.

54. **Plan for scale.**
    - If query volume exceeds single-node capacity: deploy the vector DB in clustered/sharded mode.
    - If knowledge base grows beyond 10 M chunks: benchmark IVF-PQ or SCANN indexes for memory-efficient search.
    - If multi-tenancy is required: use per-tenant namespaces or collections with row-level metadata filtering.
    - If real-time knowledge is needed: integrate a streaming ingestion pipeline (e.g., Kafka → chunker → embedder → vector DB upsert) with sub-minute latency.

---

### Quick-Start Checklist

Use this checklist to verify completeness before deploying the RAG system:

- [ ] Problem statement and user query patterns documented (Steps 1–4)
- [ ] All knowledge sources inventoried and ingestion pipelines built (Steps 6–9)
- [ ] Documents parsed, cleaned, chunked, and enriched with metadata (Steps 10–15)
- [ ] Embedding model selected, embeddings generated and stored (Steps 16–18)
- [ ] Vector database configured, indexed, and upserted (Steps 19–23)
- [ ] Hybrid retrieval (dense + sparse + fusion) implemented (Steps 24–26)
- [ ] Query preprocessing (expansion, decomposition, filtering) implemented (Steps 27–28)
- [ ] Cross-encoder re-ranking and deduplication active (Steps 29–32)
- [ ] Context construction with source attribution working (Steps 33–36)
- [ ] Grounded prompt with hallucination guards designed (Steps 37–39)
- [ ] Response generation with citations and confidence signals live (Steps 40–42)
- [ ] Evaluation dataset built and baseline metrics recorded (Steps 43–46)
- [ ] Failure analysis completed and fixes applied (Steps 47–48)
- [ ] Latency, cost, and caching optimizations applied (Steps 49–52)
- [ ] Monitoring, logging, and alerting configured (Step 53)
- [ ] Scalability plan documented (Step 54)
