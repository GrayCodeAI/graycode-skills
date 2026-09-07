---
name: systematic-review-protocol
description: "Set up, run, and query systematic literature reviews with protocol intake, PRISMA screening, and provenance queries."
license: Apache-2.0
tags:
- research
- literature-review
- scientific
---

# SynthScholar Review Skills

Three capabilities for working with systematic reviews produced by SynthScholar:

1. **Guided protocol intake** — before a review runs, guide the user through
   *every* input the agent supports and validate the protocol is complete.
2. **Provenance queries** — after a review runs, answer *which included
   publications have full text, which are abstract-only, what the content is,
   and where it came from*.
3. **Bring-your-own-corpus review** — the user hands over PDFs they collected
   themselves; produce the full review over them and export Markdown + Turtle.

Pick the mode from the request: setting up / scoping a review → intake; the
user has PDFs → BYO corpus; inspecting a finished review → queries. Modes
compose — a BYO review starts with the Mode 1 intake and its output is
queryable with Mode 2.

---

## Mode 1 — Guided protocol intake

The `ReviewProtocol` has ~40 fields. **Do not interrogate the user field by
field** — that is the wrong interaction. A user often gives only a title
("a systematic review of vocal biomarkers for depression"). From that, you can
draft a *complete, sensible* protocol yourself. The intake's job is to **draft,
lock the few decisions that genuinely change the outcome, and confirm** — not
to collect 40 answers.

### The interaction pattern (do this)

1. **Draft the whole protocol from whatever the user gave you.** Infer objective,
   full PICO, inclusion/exclusion criteria, databases, and domain features
   (charting questions, `grouping_dimension`, appraisal domains) with
   domain-appropriate defaults. Use
   references/protocol_intake.md as the field
   catalog — every field's default and validation is there.

2. **Identify the 2–4 *pivotal* decisions** — the ones where a wrong default is
   costly to run on, and ask **only those**, as structured questions with a
   **recommended** option pre-selected. Everything else stays a silent default.
   The usual pivots (not fixed — judge per topic):
   - **Scope of the key concept** — how broadly to read the intervention/exposure
     for inclusion (narrow vs. include adjacent methods). Drives recall.
   - **Appraisal instrument** (`rob_tool`) — the default `RoB 2` assumes RCTs;
     most observational/diagnostic corpora need `ROBINS-I`, `QUADAS-2`, etc.
   - **Publication date window** — unbounded vs. a cutoff.
   - Occasionally: primary **outcome** framing, or the **cohort/grouping**
     dimension for per-group analysis.

   Surface these through the host's structured-question UI — **`AskUserQuestion`
   in Claude Code**, or the decision-card UI in the web app — one question each,
   each with a recommended answer and 2–4 concrete options. Ask the pivots
   together in one batch, not one message at a time.

3. **Show the full drafted protocol back** (all fields, not just the answered
   ones) and get a single confirm before running. Make clear which values were
   the user's explicit answers vs. your defaults.

4. **Record provenance** — each *asked* decision becomes a `slr:UserInput`
   (`question_asked`, `input_value`, `options_presented`) inside a
   `slr:PreWorkflowSession`; defaults you filled are attributed to the agent.
   See references/data_model.md.

5. **Validate before running:**

   ```bash
   python scripts/validate_protocol.py --print-template > protocol.json  # scaffold
   # …write the drafted + confirmed values in…
   python scripts/validate_protocol.py protocol.json                     # gate
   ```

   Exits non-zero if a required field is missing; warns on missing recommended
   fields / invalid enums. Only run the review once it passes.

### Anti-patterns (don't do these)

- ❌ Asking the user to fill every field, or pasting the whole checklist at them.
- ❌ Asking about advanced features (batch size, cache TTL, section formats)
  unless the user raised them — default silently.
- ❌ Running without showing the drafted protocol and getting a confirm.
- ❌ Free-text-prompting the pivotal decisions when the host has a structured
  question UI — use the cards so the recommended option is one click.

### Worked example

User: *"a systematic review of vocal biomarkers for depression."*

You draft the full protocol (objective, PICO, inclusion/exclusion, databases,
charting questions, `grouping_dimension`, etc.) from that one line, then ask
**only** the pivots as structured cards, each with a recommended answer:

- **Scope of "vocal biomarkers" for inclusion?** → *Any speech-derived signal
  (incl. ASR & deep embeddings)* / Acoustic-prosodic features only / Clinician-rated only
- **Appraisal instrument?** (RoB 2 assumes RCTs; this corpus is
  diagnostic/observational) → *ROBINS-I* / QUADAS-2 / Newcastle-Ottawa
- **Publication date window?** → *Unbounded* / 2015+ / last 10 years

Then show the complete drafted protocol and get one confirm before running.
The three answers are recorded as `slr:UserInput`; every defaulted field is
attributed to the agent.

---

## Mode 3 — Bring-your-own-corpus review (user-supplied PDFs)

> *"Here are 40 PDFs I collected — write the review."*

Same review as the hosted application: screening → evidence extraction → risk
of bias → data charting (sections A–G) → critical appraisal → narrative rows →
synthesis + GRADE → per-group analysis → grounding validation → assembled
report, exported to **Markdown** and **SLR-ontology Turtle**. The only
difference is that discovery and full-text retrieval already happened — the
user did them — so the search strategy has to be *collected* rather than
generated.

Full workflow, schemas, and the PRISMA-flow accounting rules:
**references/byo_corpus_review.md** — read
it before running this mode.

### The five steps

```bash
# 1. Protocol — the Mode 1 intake, unchanged, then gate it
python scripts/validate_protocol.py protocol.json

# 2. Corpus — PDFs in, full text + hashes + provenance out
python scripts/build_corpus.py --dir ./pdfs --out corpus.json
#    …then YOU complete each entry's metadata by reading its `_head_text`…
python scripts/build_corpus.py --check corpus.json          # exit 1 until complete

# 2b. Papers the user has a DOI but no PDF for — open access, then institutional
python scripts/fetch_ezproxy.py --status
python scripts/fetch_ezproxy.py --corpus corpus.json --oa-only        # free, no setup
python scripts/fetch_ezproxy.py --corpus corpus.json --pdf-dir ./pdfs # + paywalled

# 3. Search provenance — ask the user (one batch of structured questions)
python scripts/run_local_review.py --print-provenance-template > search_provenance.json

# 4. Run
python scripts/run_local_review.py --protocol protocol.json --corpus corpus.json \
    --provenance search_provenance.json --outdir out/ \
    --formats md ttl json charting appraisal per-group

# 5. Provenance added late (if the user didn't have it in step 3)
python scripts/update_provenance.py out/review.json \
    --provenance search_provenance.json --outdir out/
```

Step 4 needs `OPENROUTER_API_KEY` and the `synthscholar` package — it drives
the app's real pipeline. **Without a key**, author the review yourself and
serialise it through the same exporters:

```bash
python scripts/export_review.py --print-template > review.json   # valid example
# …perform the stages, fill it in (see references/byo_corpus_review.md § 4b)…
python scripts/export_review.py review.json --check
python scripts/export_review.py review.json --outdir out/ --formats md ttl json
```

### Rules for this mode

- **Complete the corpus metadata yourself** from each entry's `_head_text` —
  don't hand the user a list of fields to fill. Never invent a DOI or year;
  leave it empty instead.
- **Ask for the search strategy, but never block on it.** Databases, exact
  query strings, dates searched, filters, records identified, duplicates
  removed — ask as one batch of structured questions. If the user doesn't have
  the numbers, run anyway and patch them in with `update_provenance.py`.
- **Keep the flow honest.** Identification counts are the user's; the screening
  this mode performs is a *second pass over already-retrieved reports*, not a
  re-run of their title/abstract screening. Say so when summarising.
- **Never drop full-text provenance** — `full_text_source`,
  `content_sha256`, `full_text_retrieved_at` are what make the corpus
  auditable, and they carry into the Turtle.
- **Screen on the full text, and record the basis.** Eligibility decisions are
  made on the retrieved report (methods and results), not a re-read of the
  abstract. Articles whose full text couldn't be obtained are still assessed —
  on the abstract, marked `assessed_on="abstract_only"` — never auto-included.
- **Extract only each paper's own evidence.** A number a paper cites from
  another study is not that paper's finding; excluding those is what makes the
  synthesis attributable.
- **Try open access before asking for a library session.** `fetch_ezproxy.py`
  resolves DOIs through Unpaywall → OpenAlex → Semantic Scholar first, which
  needs no setup; only what's left behind a paywall needs the user's own
  EZproxy cookies. Don't ask for credentials until `--oa-only` has run and
  something is still missing. Then keep within their licence: one paper at a
  time, delayed, capped, and never raise the ceiling on their behalf.
- **Report the reading basis when you summarise.** "23 of 25 read in full text,
  2 included on abstract alone" is different evidence from "25 included".
- **Always offer both exports.** `.md` to read, `.ttl` to ingest.
- **Ingesting into BrainKB is the `brainkb` skill's job — hand off, don't
  improvise.** Its *"Ingest a SynthScholar review"* section owns the graph IRI
  (`https://brainkb.org/synthscholar/reviews/<review_id>/`, registered to a
  space), the upload path, and the once-per-review rule. Print the export's
  triple count when you hand the file over; that number is what the ingest is
  reconciled against.

## Mode 2 — Provenance queries

> *Which included publications have full text, which are abstract-only, what is
> the full-text content, and where did it come from?*

The same review is materialised in **two places**, and this mode covers both:

| Representation | Where | Query language | Full-text signal |
| --- | --- | --- | --- |
| RDF graph (SLR ontology) | exported `.ttl` / `.jsonld` | **SPARQL** | `slr:full_text_artifact` node |
| PostgreSQL article store | `article_store` + `article_full_text` | **SQL** | row in `article_full_text` |

Pick the surface that matches what the user has in hand. If they exported RDF,
use SPARQL. If they have the live database, use SQL. The two are kept in
parity: `slr:content_hash` in RDF equals `article_full_text.content_sha256`.

## When to invoke this skill

**Intake (Mode 1)** — when the user asks to:

- **Start / scope a new review** or "set up a protocol".
- **Gather the review inputs** — research question, PICO, inclusion/exclusion.
- **Check a protocol is complete** before running.
- Configure **domain features**: charting questions, per-group / cohort
  analysis, custom appraisal domains, output formatting, PRISMA registration.

**BYO corpus (Mode 3)** — when the user:

- Provides **PDFs / a folder of papers** and wants a review, synthesis, or
  evidence table built from them.
- Has **DOIs for paywalled papers** and institutional access, and wants the full
  texts retrieved so the review reads the papers rather than their abstracts.
- Says they **already did the search** (or exported records from Scopus / Web of
  Science / Embase / a reference manager) and wants the review run on that set.
- Wants an existing review **exported to Markdown or Turtle**, or the **TTL
  ingested** into a triple store / BrainKB.
- Wants to **add or correct the search strategy** on a review that already ran.

**Queries (Mode 2)** — when the user asks to:

- **List included publications that have full text** (vs. everything included).
- **Distinguish full-text-included from abstract-only** inclusions.
- **Retrieve the full-text content** of included sources.
- **Audit provenance** — which resolver produced each full text (`pmc_oa`,
  `europe_pmc_oa`, `unpaywall_pdf`, `biorxiv_pdf`, `openalex_pdf`,
  `semanticscholar_pdf`, `ezproxy_pdf` — institutional subscription access —
  `user_supplied_pdf`, `article_store`, `cache`) and when.
- **Ask what the review actually read** — how many reports were retrieved vs
  not, how many eligibility decisions were made on full text vs abstract only,
  which studies were included without their full text, which papers came via
  institutional access, and why reports were excluded at each stage. Recipes:
  `reading-basis`, `retrieval-routes`, `ezproxy-articles`, `exclusion-reasons`,
  `screening-decisions`, `abstract-only-inclusions`.
- **Verify or backfill** the `article_full_text` provenance table.

Mode 2 covers full-text availability, content and provenance of *included*
sources, plus the screening-decision audit trail (stage, basis, reason) — not
full charting extraction.

## The core model

An **included** publication is a `slr:IncludedSource` (SPARQL) / a row in
`article_store` that survived screening (SQL). Among included publications:

- **full-text-included** → full text was retrieved. In RDF it carries a
  `slr:full_text_artifact` → `slr:StoredArtifact` (kind `source_text_extract`)
  with `slr:content_text`, `slr:content_hash`, `slr:content_size_bytes`. In SQL
  it has a matching row in `article_full_text`.
- **abstract-only** → included but no full text. It has `dcterms:abstract`
  (RDF) / a non-empty `abstract` in `article_store`, but **no**
  `slr:full_text_artifact` / **no** `article_full_text` row.

Presence of the artifact / row **is** the distinguishing signal — never infer
full-text availability from the length of an abstract.

## How to answer a request

1. **Determine the surface.** Ask (or infer from the artifacts present)
   whether the user has an RDF export (`.ttl`/`.jsonld`) or DB access (a DSN).
2. **Pick the query.** Match the request to a named recipe in
   references/sparql_queries.md or
   references/sql_queries.md.
3. **Run it** with the matching helper script, or hand the user the query.
4. **Report** the distinction plainly: N included, of which M have full text
   and (N−M) are abstract-only; include provenance/source breakdown if asked.

## Helper scripts

All live in scripts/. Run them from an environment where the
project's deps are importable (`rdflib` for SPARQL, `psycopg[binary]>=3.1` for
SQL; the backfill also needs the `synthscholar` package on `PYTHONPATH`). The
Mode 3 scripts need `synthscholar` importable too — plus `pymupdf` for PDF text
and `OPENROUTER_API_KEY` for `run_local_review.py`.

**`export_review.py` and `run_local_review.py` need the development checkout,
not the released package** — `pip install -e /path/to/prisma-review-agent`. The
PyPI build predates the whole-document reading and screening-basis provenance,
and they refuse to run on it rather than silently dropping those fields.
`fetch_ezproxy.py` works anywhere — it needs only `httpx`, since the skill
vendors both `scripts/oa_client.py` (the open-access DOI chain) and
`scripts/ezproxy_client.py` (`synthscholar.ezproxy` ships only in the checkout).

```bash
# Intake: blank template → fill from answers → validate before running
python scripts/validate_protocol.py --print-template > protocol.json
python scripts/validate_protocol.py protocol.json

# BYO corpus: PDFs → corpus → review → md/ttl (see Mode 3)
python scripts/build_corpus.py --dir ./pdfs --out corpus.json
python scripts/build_corpus.py --check corpus.json
python scripts/fetch_ezproxy.py --corpus corpus.json --pdf-dir ./pdfs   # OA, then paywalled
python scripts/run_local_review.py --protocol protocol.json --corpus corpus.json \
    --provenance search_provenance.json --outdir out/
python scripts/run_local_review.py --protocol protocol.json --corpus corpus.json --dry-run
python scripts/export_review.py out/review.json --outdir out/ --formats md ttl
python scripts/update_provenance.py out/review.json --provenance search_provenance.json

# SPARQL over an RDF export — named recipe or your own query
python scripts/query_sparql.py review.ttl --query included-full-text
python scripts/query_sparql.py review.ttl --query status-all --format csv
python scripts/query_sparql.py review.ttl --sparql ./my_query.rq

# SQL over the Postgres article store (DSN via --dsn or $PRISMA_PG_DSN)
python scripts/query_postgres.py included-full-text
python scripts/query_postgres.py source-breakdown
python scripts/query_postgres.py get-content --pmid 39012345

# Backfill article_full_text from legacy article_store.full_text rows
python scripts/backfill_full_text.py            # needs migration 006 applied
```

Run any script with `-h` for its full option list, and `--list` (query
scripts) to see every named recipe.

## References

- references/protocol_intake.md — complete
  guided-intake checklist: every `ReviewProtocol` input with question, example,
  validation, default, and tier.
- references/byo_corpus_review.md —
  bring-your-own-corpus workflow: corpus schema, search-provenance intake,
  PRISMA-flow accounting, the two execution paths, exports and ingestion.
- references/sparql_queries.md — SPARQL recipe catalog.
- references/sql_queries.md — SQL recipe catalog.
- references/data_model.md — the SLR-ontology terms
  and the `article_store` / `article_full_text` schema this skill relies on,
  plus how provenance is captured in the pipeline.

## Caveats

- Both signals are written **going forward**. Reviews exported/run before the
  full-text-provenance change won't have `slr:full_text_artifact` triples or
  `article_full_text` rows until re-exported or backfilled
  (`scripts/backfill_full_text.py`).
- `full_text_source` is empty for backfilled historical rows — their provenance
  was never recorded.
- Full-text bodies can be large; the SQL `get-content` recipe streams a single
  PMID. Avoid `SELECT content` across the whole table in interactive use.
- Mode 3 reads a PDF's text layer — scanned PDFs need OCR first. Each paper is
  read **in full** (evidence extraction processes every chunk), so a long corpus
  costs real tokens; `run_local_review.py` prints the call estimate before
  spending, and `protocol.evidence_max_chars` bounds it. It never deduplicates
  the supplied corpus; that stays the user's responsibility.
- Open-access retrieval reaches only what has been deposited somewhere; a
  paywalled paper with no repository copy misses on all three providers.
  Unpaywall additionally needs `SYNTHSCHOLAR_EMAIL` (their ToS) and is skipped
  without it.
- Institutional access (EZproxy) needs a live browser-exported session cookie
  and only reaches what the institution licenses. Credentials go in
  `EZPROXY_*` env vars, never on a command line — the CLI invocation is stored
  verbatim in provenance.
