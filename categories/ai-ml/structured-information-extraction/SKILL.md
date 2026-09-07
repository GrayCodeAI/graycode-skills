---
name: structured-information-extraction
description: "Extract named entities, resources, or schema-conformant JSON from text and PDFs, with ontology grounding and quality scoring."
license: Apache-2.0
tags:
- ner
- nlp
- extraction
- ontology
---

> **Skill version 0.6.1.** Two things carry across every mode. **Concept mapping is mandatory and tool-only**: the pipeline cascades local hybrid → BioPortal → ask the user for an alternate URL → hard-stop, and items carrying `concept_mapping_provenance: "llm_knowledge"` are demoted to `unmapped`, because a hallucinated IRI is worse than an honest gap. **ABCD/HBCD mode** (rule 16) maps a paper's own wording to the NBDC/NDA dictionary using the instrument, respondent, metric and release it states, keeps only what that study did itself, and emits a cross-paper synthesis whose every row carries its provenance. Legacy outputs can be brought up to spec via `python -m scripts.normalize_result <file> --input <text> --llm-model <model>` (idempotent). See CHANGELOG.md.



# StructSense Skills — structured information extraction

A reusable methodology for turning unstructured text and PDFs into clean, schema-conformant JSON, with optional ontology grounding and quality scoring. The patterns here are model-agnostic: they work with Claude, GPT, Gemini, Pi, or any local model.

## When to invoke this skill

Trigger when the user asks to:

- Extract **named entities + key terms** (NER) from biomedical, neuroscience, or scientific text.
- Pull **resources** out of papers — tools, datasets, models, benchmarks, leaderboards.
- Convert a document into a **target JSON schema** (e.g. ReproSchema, Croissant, a custom schema the user supplies).
- **Map extracted terms to ontologies** (BioPortal, OLS, OBO, BTO, CL, UBERON, NCBITaxon, MESH, …).
- **Score or judge** the quality of an existing extraction.
- Process a **long document** that needs chunking and parallel runs.
- Extract **ABCD / HBCD study content** from publications — which variables a study used, the constructs behind them, the models specified, the findings reported — and **compare across papers**: where is there consensus, where divergence, which variables are consistently mediators or moderators. → `references/abcd-extraction.md`.

## The core pattern

Four cooperating roles, run sequentially. Each role's output is the next role's input. Any role can use a different model.

```
┌───────────┐   raw text     ┌────────────┐   extracted   ┌───────┐   aligned   ┌──────────────┐
│ EXTRACTOR │ ──────────────►│ ALIGNMENT  │──────────────►│ JUDGE │────────────►│ HUMAN FB     │
│ (LLM)     │                │ (LLM+tool) │               │ (LLM) │             │ (optional)   │
└───────────┘                └────────────┘               └───────┘             └──────────────┘
   strict JSON                 + ontology fields           + judge_score          + corrections
                               + provenance                + remarks              + revised JSON
```

| Stage | Job | Reads | Writes |
|---|---|---|---|
| **Extractor** | Find entities/resources/fields. Output strict JSON. | raw text | items with `entity`/`name`, `label`/`type`, `sentence`, `start`, `end` (etc.) |
| **Alignment** | Map each item to an ontology IRI. | extractor output | adds `ontology_id`, `ontology_label`, `ontology`, `concept_mapping_provenance` (`tool` or `llm_knowledge`) |
| **Judge** | Score quality of each item (0–1). | alignment output | adds `judge_score`, `remarks` |
| **Human feedback** | Apply corrections from a human reviewer. | judge output + user feedback | revised JSON |

You can run any subset — see `references/pipeline-pattern.md`.

## Who runs the LLM stages — read this before asking for an API key

The four roles above say *what* runs, not *who* runs it. There are two modes, and
picking the wrong one is the most common way a run stalls before it starts.

| | **Host-model mode** (the default when an agent is reading this) | **Framework mode** |
|---|---|---|
| Who is the extractor / judge | **you**, the model reading this file | `scripts/pipeline.py`, calling out over HTTP |
| Where it applies | Claude Code, Codex CLI, Claude Desktop, Pi, any agent session | batch jobs, cron, CI, an MCP server, a script |
| LLM API key | **none — there is no API to call** | required (`OPENROUTER_API_KEY` / `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`) |
| `--extractor` / `--judge` (pipeline.py) | **do not pass them** — nothing to point at | required |
| `--llm-model` (normalize_result.py) | **do pass it**, set to your own model id — it is a provenance label, not a call | pass the extractor model |
| How the prompt is used | read `prompts/<variant>.md` and follow it yourself | passed to the provider by `llm_client.py` |

**If you are an agent reading this, you are in host-model mode.** Read the extractor
prompt and produce the JSON yourself, then use the scripts for the deterministic work
— `mask_pass.py`, `group_by_entity.py`, `normalize_result.py`, `stats.py`,
`iri_validation.py`. None of those call an LLM. So the whole pipeline runs with **no
LLM API key at all**, and asking the user for one is a bug, not diligence.

Switch to framework mode only when the user explicitly wants it: a headless/scheduled
run, or a *different* model than the host (cheaper extraction, a local Ollama, a
model you can't be). Then `--extractor` and a key are genuinely required.

**Two keys that are not LLM keys, and are needed in either mode:**

- `BIOPORTAL_API_KEY` — the concept-mapping **tool** (rule 15's cascade). Free, and
  the only key that ever matters for a host-model run. If mapping falls through to
  BioPortal and this is unset, ask for *this* by name — never as "an API key".
- `SEMANTIC_SCHOLAR_API_KEY`, and similar service keys — optional rate-limit lifts.

When you do need to ask, name the exact variable and what breaks without it. "This
needs an API key" is the ambiguous phrasing that sends users hunting for an
OpenRouter account they don't need.

## Quick decision flow

1. **What kind of extraction?**
   - Entities + key terms (NER) → load `references/ner-extraction.md`, then pick the extractor prompt by domain:
     - General-domain text (news, finance, biographies, generic web pages, mixed text) → `prompts/extractor-ner-general.md`.
     - Neuroscience text — broad (behavior + systems + cellular + molecular + computational) → `prompts/extractor-ner-neuroscience.md`.
     - CNS-cell-focused text (cell atlases, patch-seq, scRNA-seq cell typing, BICCN-style cell census — anything where cell types + markers + morphology + ephys are the subject) → `prompts/extractor-ner-cns-cells.md`, **plus `references/cell-annotation-conventions.md`** if the output will be scored against a human gold standard (specificity types, nested spans, coordinated ids — the conventions that make the difference between a real error and a format mismatch).
   - Tools / datasets / models / benchmarks → load `references/resource-extraction.md` and `prompts/extractor-resource.md`.
   - User has a target JSON schema → load `references/structured-extraction.md` and `prompts/extractor-structured.md`.
   - **ABCD / HBCD variables, models, findings, or cross-paper synthesis** → load `references/abcd-extraction.md` and `prompts/extractor-abcd.md`. This mode has its own verifier and its own hard rules (see rule 16); it is not a variant of NER. Single PDF or a directory in bulk; every run emits JSON + Markdown + Turtle.
2. **Want exhaustive recall? (almost always yes for NER)** → after pass-1 extraction, run the **mask-recall pass** with `prompts/mask-recall-pass.md` + `scripts/mask_pass.py`. Optionally also run **mask-verify** (`prompts/mask-verify-pass.md`) for per-item label sanity. See `references/ner-extraction.md` → "Two-pass strategy: mask-mode".
2b. **Biomedical text? Enable the HuggingFace NER ensemble.** Pass `--ner-profile biomedical_broad` (or `cns_cells` / `pharmacology` / `genetic` / `clinical` / `minimal` / `all`) to run specialist models alongside the LLM extractor. Every mention carries a `source_model` field; the grouped view records `consensus_count` (how many models agreed). See `references/ner-models.md`. Skip the ensemble for non-biomedical text or when `transformers` isn't installed.
3. **Need ontology mapping?** → load `references/ontology-mapping.md`. Default cascade: **local hybrid** at `http://localhost:8000` (verify at `/docs`) → **BioPortal** → **ask the user** for an alternative URL → skip alignment only if declined. Don't hardcode the URL; the port and host vary across deployments.
4. **Long document (>10 pages or > model context)?** → load `references/chunking-strategy.md`. Chunk → run extractor in parallel → merge → run downstream stages.
5. **Need quality scoring?** → load `prompts/judge.md`.
6. **Multiple models for cost?** Use the cheapest capable model for extraction (often a small open model), a stronger model for alignment if you don't have a mapping tool, and a fast model for judging. See `references/model-selection.md`.

## Hard rules

These prevent the most common failures.

1. **Strict JSON output, no markdown fences.** Every prompt must include `"Output strict JSON only. No prose. No markdown fences."` in the system message. Set `temperature: 0` for extraction and alignment.
2. **Extract EXHAUSTIVELY.** For NER, emit every occurrence of every mention as a distinct item with its own `start`/`end`. Never deduplicate by surface form. A multi-page neuroscience paper should yield hundreds to thousands of entity items, not a few hundred. If yield feels low, run the mask-recall pass (`prompts/mask-recall-pass.md` + `scripts/mask_pass.py`) — typical recovery is +30–80%.
3. **Preserve fields downstream.** Alignment, judge, and human-feedback stages **add** fields. They never remove existing fields and never re-key existing items.
4. **Record provenance.** Every mapped item carries `concept_mapping_provenance: "tool" | "llm_knowledge"`. Never hide where a mapping came from.
5. **Chunk and merge** for inputs longer than the model's context window (or `> 25,000` chars for safety on 128k models). Always re-merge by stable identifiers (sentence + char span, or item `id`).
6. **Don't invent placeholders.** The agent communication contract is: extractor input is the raw text; alignment input is the extractor's JSON; judge input is the alignment's JSON. Pipe outputs cleanly — don't re-wrap or paraphrase between stages.
7. **Validate before returning.** Parse the JSON; if parsing fails, repair-then-retry (see `references/json-output-discipline.md`). Validate against the task's JSON schema in `schemas/`.
8. **Always emit a `stats` block.** Every final result must embed a `stats` block at the top level (totals, label histogram, alignment provenance, judge score buckets, per-stage elapsed times) and print a human-readable summary to stderr. Use `scripts/stats.py`. This is the answer to "did the run do what it was supposed to?" — a healthy NER run on a paper has hundreds-to-thousands of entity mentions and `mentions_per_unique > 1`. A summary with 230 mentions and `mentions_per_unique ≈ 1` is the symptom of surface-form deduplication; re-run with the mask-recall pass and double-check no upstream step is collapsing duplicates.
9. **Final-result filename convention.** When writing the result to disk, name it **`<input_stem>_final.json`** (e.g. `paper.pdf` → `paper_final.json`, `note.txt` → `note_final.json`). Honor an explicit `--out` only when the user provides one. The reference helper is `scripts/pipeline.py::default_output_path`.
9b. **More than one document? Deliver the corpus view too, not just N per-paper files.** In framework mode this is **automatic**: `pipeline.py --input <dir>` (or a repeated `--input`) runs each paper, writes each `<stem>_final.json`, and then merges them into `corpus_synthesis.{json,md}` — auto-detected from the input count, exactly as `abcd_extract` decides on its synthesis, with `--no-synthesize` / `--synthesize` to override. In **host-model mode you are the loop**, so nothing runs it for you: after the last paper, run `python -m scripts.merge_corpus <out-dir> --out <out-dir>/corpus_synthesis` yourself — a directory works, no glob needed, and it skips anything that looks like a previous roll-up so a re-run cannot fold its own output back in. Per-paper `<stem>_final.json` stays the authoritative record of raw mentions; the roll-up adds one canonical row per entity across every paper, which documents it appears in, and where papers disagree about its ontology id. Handing back a directory of per-paper JSON and leaving the user to reconcile it is an unfinished deliverable: the questions a corpus is *for* ("which cell types does this collection talk about", "which mappings conflict") cannot be answered from any single file. The index is grouped, not concatenated — pass `--include-mentions` only if the raw union is genuinely wanted.
10. **Concept-mapping cascade — and you MUST probe before declaring unavailable.**
    Default mapper is the local hybrid service at **`http://localhost:8000`**. Before saying "no mapper available" you MUST run at least one probe in your current runtime:
    ```bash
    curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/docs
    ```
    If the probe returns 200, USE the mapper. The real API schema is **`{ "max_results": N, "text": [{"text": "...", "context": "..."}] }`** — NOT `terms:[...]`. See `prompts/alignment-via-http.md` for a turnkey curl + jq pipeline.
    - On connection refused: try BioPortal (`BIOPORTAL_API_KEY`).
    - On further failure: **ask the user** for an alternative URL (ports 8001 / 8080 / 9000 / reverse-proxied paths are common) — do not give up silently.
    - Only after the user declines should you skip alignment (`concept_mapping_provenance: "skipped"`).
    - **If your runtime can't reach the user's `localhost`** (claude.ai web app, Anthropic Skills hosted, ChatGPT cloud), say so explicitly and direct the user to the MCP bridge or tunnel options in `connecting/mcp-server.md`. Don't pretend the service is unreachable when the user has it running — be explicit that the runtime is the constraint.
11. **Always tag `source_model` provenance.** Every entity item carries `source_model` (HF model id like `d4data/biomedical-ner-all`, or `llm_ner:<model>` for LLM-extracted items). The grouped view (`entities_grouped[]`) lists all contributing models per entity and the `consensus_count`. Never strip or merge these fields. See `references/ner-models.md`.
12. **Document metadata lives at the top, not on every entity.** `paper_title` / `doi` / `source_path` go into a top-level **`source_metadata`** block — ONCE per run. `paper_location` (section / page / paragraph) stays per-entity because it varies. Never repeat document-level metadata on hundreds of items.
13. **Always emit both `entities[]` (raw, one per occurrence) and `entities_grouped[]` (canonical, with merged sentences from every location).** The raw list is the authoritative record for exhaustive extraction; the grouped list is what downstream consumers navigate by. Use `scripts/group_by_entity.py:attach_grouped_views` — it's automatic in `pipeline.run()`.
14. **Canonical-shape guarantee via normalizer.** `scripts/normalize_result.py` runs automatically before every save and produces the canonical shape regardless of what the LLM emitted: top-level `source_metadata`, stripped per-entity `paper_title`/`doi`, tagged `source_model` on every item, `entities_grouped` attached, `stats` embedded. **Idempotent** — safe to run on already-canonical results. It's also exposed as a CLI to fix legacy result files in place. If you ever see legacy output, do not panic and do not edit by hand — run `python -m scripts.normalize_result <file>` and the file is brought up to spec.
15. **Concept mapping is MANDATORY and TOOL-ONLY. Zero hallucination.**
    - The pipeline **never silently skips** alignment. Default cascade: **local hybrid** (`http://localhost:8000`, verify at `/docs`) → **BioPortal** (`BIOPORTAL_API_KEY`) → **ask the user** for an alternate URL → **hard-stop with a clear error**. OLS is no longer in the auto-cascade (it has no gene coverage); the user must opt in explicitly via `--allow-ols-fallback`.
    - `concept_mapping_provenance: "llm_knowledge"` is **strictly forbidden** in canonical output. Any item carrying it is automatically demoted to `unmapped` by `scripts/iri_validation.py` and marked `alignment_method: "validation_failed"`. The item itself is preserved (exhaustive extraction is not compromised); only the fabricated mapping is dropped.
    - Every `ontology_id` is **structurally validated** against known IRI patterns (OBO PURLs, identifiers.org, BioPortal PURLs, EBI OLS, semanticweb.org, generic `<NS>_<NUM>` OWL IRIs). Malformed strings get demoted too.
    - The output's `stats.validation` block reports `passed` / `demoted` counts and the breakdown by failure reason — so you can tell at a glance whether the LLM tried to hallucinate.
    - If you cannot reach a real mapping tool, **say so to the user** and let them decide. Never invent IRIs to make the run "look complete."

16. **ABCD/HBCD mode: verification is the feature, not a formality.**
    - **Who runs the model depends on where you are.** In Claude Code / Codex **you** are the model: run `--prepare`, do the extraction yourself against `prompts/extractor-abcd.md`, write `<stem>.payload.json`, then `--payload <dir>`. Do **not** pass `--llm-model` there — there is no API to call. Only pass it when a framework (Pi, batch, cron) should call an API. Verification and every output are identical on both paths, and `provenance.extraction_path` records which was used.
    - **The paper is the only source of what a study used.** Never add a variable because ABCD papers usually include it, and never enumerate the data dictionary into the output. The dictionary and the Cognitive Atlas exist only to *verify and join* what the paper says.
    - **Every item needs a verbatim `evidence.quote` (>= 25 chars) that is findable in that paper.** `scripts/abcd_verify.py` deletes items whose quote is not there and records why in `rejected[]`. The requirement is per-section: a **variable** name must appear literally in its quote; a **construct** need not (it is a reading of the prose, and `label_in_quote` records which case it was); a **finding/model** must name at least one variable that appears in its quote.
    - **Results never land among the papers.** Everything goes to `<input>/abcd_results/` (override with `--out-dir`), including `--prepare`'s extracted text (`text/`) and the agent's payloads (`payloads/`). That directory is excluded from input scanning, which is load-bearing: it holds a `.txt` of every paper, and a rerun would otherwise extract each study twice — once from the PDF, once from its own extracted text — and checksum dedupe cannot catch that, since a PDF and its text layer are genuinely different files.
    - **One paper per distinct file.** Inputs are deduplicated by content checksum *before* any PDF is parsed, so `paper.pdf` and `paper(1).pdf` are one paper. This is a correctness rule, not tidiness: the synthesis counts by paper, so a duplicate doubles one study's weight in every consensus and turns "two papers agree" into a fact about one. The clean filename wins over the `(1)` copy, and the drop is reported in `input_duplicates_dropped`.
    - **One entry per variable per timepoint.** A paper writing "internalizing behaviors" in its Methods and "internalizing behavior" in its Results gets one merged entry (`also_written_as`, `merged_from` keep every wording and quote). Left separate, one resolves to a table and the other does not. Timepoint stays part of the key — conflict at year 1 and year 2 *are* different quantities.
    - **Cover the release the paper used.** All seven releases ship with the skill in `data/dictionaries/` (ABCD `nda-legacy`/4.x-5.x, `6.0`, `6.1`, `7.0`; HBCD `1.0`, `1.1`, `2.0`) — no workbook or network needed. Rebuild for a newer release with `--from-xlsx --all-sheets --minimal --gzip`; a local snapshot beats a bundled one. They matter together because ABCD 6.x renamed variables wholesale and the alternate namings (`name_nda`, `name_deap`, …) are what let a 2021 paper's `nihtbx_flanker_uncorrected` resolve to 6.1's `nc_y_nihtb__flnkr__uncor_score`.
    - **Only what THIS study did.** A paper's introduction and discussion are largely other people's work. A variable counts only if this paper measured it; a finding counts only if this paper's own analysis produced it. `gate_scope` in `scripts/abcd_verify.py` enforces it independently of the extractor and rejects the rest as `finding_attributed_to_cited_work` / `measure_only_mentioned_in_cited_work`. This is not tidiness: without it, paper A's summary of paper B arrives in the synthesis as independent evidence and the literature gets double-counted.
    - **A string is only called an ABCD variable when a real dictionary release contains it.** Two routes get there. `dictionary_status: "verified"` means the paper printed a real dictionary name. `context_variable` means the paper's *wording* resolved to one variable through `scripts/abcd_context.py`, using what the paper itself stated — instrument, respondent, metric, release. Everything else stays visible as `unverified_variable` / `not_a_variable_name`.
    - **Most papers name no variable at all, so context mapping is the difference between a filled and an empty `nda_or_nbdc_table`.** On a three-paper sample it went from 1 of 57 variables carrying a table to 29. Four signals do the work, all of them the paper's own words: the **instrument** scopes candidates to one table (`externalizing` exists in the CBCL, ABCL, YSR and BPM — the paper naming the CBCL settles it); the **respondent** filters rather than merely penalises (`fes_y_ss_fc` vs `fes_p_ss_fc` are different measures, not near misses); the **metric** picks `_t` over `_r`; the **release** decides which snapshot is even eligible. That last one matters most — a 5.0 paper matched against 6.1 turns one clear measure into rival candidates in two tables.
    - **Never name a variable the paper did not name.** When several variables in one table fit equally well — 68 Desikan-Killiany thickness ROIs for "cortical thickness" — the result is `context_family`: table and domain reported, variable `null`, family prefix and candidate list attached. When tables disagree but the domain does not, `context_domain`. When the paper named an instrument rather than a variable, `instrument_table`. Each of those is more useful than a guess and more honest than a blank.
    - **Every mapping carries its own audit.** `context_mapping` records the cues that fired, the ranked candidates with scores, the thresholds applied, and why one variable was or was not named. A reader disagreeing with a mapping can see exactly which step to reject.
    - **The NDA element API confirms names; it does not map wordings.** `scripts/abcd_nda_api.py` looks up a printed name (giving `verified_via_nda_api` for a release we do not have) and can full-text search element descriptions — but a search hit is recorded as `nda_api_suggestions`, never as a mapping. Every table NDA can return is already in the snapshots, so a search hit is something the offline matcher already rejected, and NDA ranks over the whole archive: it offered an *Adult* Behavior Checklist score for "internalizing behaviors" and an SST series timestamp for "age at time of scan". Suggestions for a human, not evidence.
    - **Release membership is checked where it can be.** The `nda-legacy` snapshot is the union of NDA releases 2.0, 3.0 and 4.0 (116,353 variables, of which 87,682 existed in 3.0), and each row carries the releases its structure shipped in. A paper naming 2.0/3.0/4.0 is matched only against that release's rows; a literal name that resolves outside it gets `nda_release_conflict` — a warning, never a rejection, because the check is structure-level and papers do misstate their release. NDA labels nothing as 5.x, so 5.0/5.1 papers search the union.
    - **A local snapshot shadows a bundled one, and now says so.** Local wins by design, but a stale local build wins *silently*: an 85,984-variable `dd-abcd-nda-legacy.json` built before structure discovery was fixed shadowed the corrected 116,353-row bundle, so the fix appeared to do nothing. Shadowing now prints both counts.
    - **Build snapshots first if you need a newer release**: `python -m scripts.abcd_dictionary build --study abcd --release latest`. Load two or more releases so renames surface as `dd_release_gap`.
    - **Report the mention AND the mapping.** Keep `mention_as_written` (how the paper wrote it — prose label or id) alongside the resolved `dictionary_match.variable`, `nda_or_nbdc_table` and `nbdc_domain`. A reader must be able to see both sides of the join.
    - **Construct ids are tool-only.** A `trm_`/`tsk_` id is attached only when `scripts/cognitive_atlas.py` returned it; a model-supplied id is demoted into `demoted_claim`. Unmapped is an acceptable answer — run `cognitive_atlas search` and offer candidates to the user rather than auto-picking.
    - **Provenance includes where in the paper**: `section`, `page`, char offsets into the original text, and `used_context` (the surrounding sentences). Per run, record every dictionary snapshot consulted (release, source, sha256, retrieval time) and the Atlas vocabulary versions.
    - **Extract every variable the study used, not just the ones in the Measures section.** Table 1 rows, the covariate list, per-wave instances and self-computed composites are all variables. The verifier reports every string that a model or finding names but `variables[]` never declared (`coverage.referenced_but_not_declared`); those reach the synthesis with no quote, no table and no domain, which is a hole in the extraction rather than a detail.
    - **Synthesis counts by PAPER, never by finding**, so one verbose paper cannot outvote several others. `divergent` means opposing signs, not differing magnitudes. A contested mediator/moderator role is reported as contested, never resolved by majority vote — which is why the extractor must emit `unspecified` when a paper is ambiguous.
    - **Agreement is measured over paper-direction claims, and role consistency needs exclusivity.** Papers as the agreement denominator let a row print `1.00` agreement and a `divergent` verdict at once. And a variable that is a mediator in every paper *and* an outcome in every paper is contested: `role_exclusivity` is the share of papers where the dominant role is the only one, and both it and the share must clear the threshold.
    - **Two papers are the same variable only when they resolve to the same dictionary variable, share a paper-declared alias, or share a normalised mention.** Never on similarity: parent-report and youth-report versions of a scale stay separate rows, and when two wordings do resolve differently the row carries `mapping_disagreement` rather than silently picking one.
    - **The synthesis must say where every number came from.** Each variable row carries `paper_evidence` (per paper: wording used, instrument, respondent, metric, roles, timepoints, resolved variable, table, dd release, quotes); each construct row carries the variables that measured it — declared measures kept separate from variables that merely appear in its findings; each paper row carries its dataset (release, sample, analytic sample, waves, cohort, source). `claims[]` states what the corpus supports, the evidence paper by paper with a strength rating derived only from reported facts, and — separately — the contradictions and caveats, including "these papers report the same sample size, so their agreement is not independent".
    - **Bulk is first-class**: `--bulk` over a directory keeps going when one paper fails, writes one output set per paper, and `--synthesize` adds the cross-paper pass. Per-paper evidence stays inspectable; the synthesis never becomes the only record.
17. **Never ask for an LLM API key in host-model mode.** If you are an agent reading this file, you *are* the extractor and the judge — there is no API to call, so `OPENROUTER_API_KEY` / `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` are irrelevant and `pipeline.py`'s `--extractor` / `--judge` have nothing to point at. (`--llm-model` on `normalize_result.py` is the exception that proves the rule: it is a provenance *label*, makes no call, and you SHOULD pass your own model id or every item lands as `llm_ner:unknown`.) Read the prompt, produce the JSON, and use the scripts for the deterministic stages (`mask_pass.py`, `group_by_entity.py`, `normalize_result.py`, `stats.py`, `iri_validation.py` — none of them call an LLM). A key is required only when the *user* asks for a headless run or a different model than you. The one key a host-model run can legitimately need is `BIOPORTAL_API_KEY`, which is a concept-mapping **tool** credential, not an LLM one — ask for it by name, and only after the local mapper has actually failed (rule 15). Blocking a run on "please provide an API key" when none is needed is a defect. See "Who runs the LLM stages".

## Install

```bash
pip install -r requirements.txt          # core: HTTP, schema validation, PDF, xlsx
pip install -r requirements-llm.txt      # ONLY if a framework calls an API (--llm-model)
pip install -r requirements-ner.txt      # ONLY for the HuggingFace NER ensemble (heavy: torch)
```

`requirements.txt` is enough to run every mode with the calling agent as the model,
including ABCD/HBCD — **the ABCD dictionaries ship inside the skill**
(`data/dictionaries/`, all seven releases, 8.6 MB gzipped), so nothing external is
needed to verify a variable. A missing PDF backend is the most common first-run failure
("all PDF extractors failed"), so install it before blaming a paper.

## File map (load on demand)

The files below are intentionally separated so you only load what the current task needs.

### `references/`
- `pipeline-pattern.md` — multi-stage agent pattern, how to chain stages, when to skip, resume from a saved stage.
- `ner-extraction.md` — NER methodology: entity types, output keys, edge cases, exhaustive extraction, mask-recall pass, grouped view.
- `ner-models.md` — HuggingFace + LLM ensemble: model roster, profiles by domain, `source_model` provenance, consensus count, when to skip.
- `resource-extraction.md` — resource extraction methodology (tools/datasets/models/benchmarks/leaderboards).
- `structured-extraction.md` — generic schema-driven extraction (PDF → user-supplied JSON schema).
- `ontology-mapping.md` — BioPortal REST API, OLS REST API, embedding-based hybrid retrieval, LLM-only fallback. Picking and combining backends.
- `chunking-strategy.md` — sentence-aligned chunking, parallel extraction, merge by stable key, context window math.
- `json-output-discipline.md` — schema-locked prompting, JSON repair, validation.
- `cell-annotation-conventions.md` — how a human annotator marks up cell mentions: the `cell_phenotype` / `cell_vague` / `cell_hetero` specificity axis, nested hedge-plus-head spans, one ontology id per coordinated element (`;` positional, `-` for a gap), `skos:exact` vs `skos:related`, BioC `(offset, length)` conversion, and a validation checklist. Load this whenever cell extraction will be **scored**, and note it overrides the older non-CNS exclusion in the cns-cells prompt.
- `model-selection.md` — picking models per stage; OpenRouter / Ollama / vLLM / Claude / GPT / Gemini configuration.
- `human-feedback.md` — designing the human-in-the-loop review step.
- `abcd-extraction.md` — **ABCD/HBCD mode**: extracting variables/constructs/models/findings from publications, the three hard rules (strict verification, complete provenance, single-or-bulk), building dictionary snapshots from NBDCtools, Cognitive Atlas construct mapping, and how to read the cross-paper synthesis verdicts.

### `prompts/`
- `extractor-ner-general.md` — general-domain NER (Person, Org, Location, Product, Event, Date, …).
- `extractor-ner-neuroscience.md` — broad neuroscience NER (BrainRegion, CellType, Gene, Protein, Drug, Behavior, Disease, Method, Stimulus, Measurement, …).
- `extractor-ner-cns-cells.md` — CNS-cell-focused NER (CellClass / CellType / CellSubtype with lineage markers, morphology, ephys, layer, projection, atlas references, profiling method).
- `mask-recall-pass.md` — **pass-2** that surfaces mentions pass-1 missed. Run on any of the three NER prompts above. Big recall booster (typical +30–80%).
- `mask-verify-pass.md` — per-item label sanity check via cloze (mask one entity, predict label from context). Optional precision booster.
- `extractor-resource.md` — research resource extractor (one primary Model/Dataset/Tool/Benchmark per source, with `mentions` for secondaries).
- `extractor-structured.md` — schema-driven extractor (PDF → user-supplied JSON Schema).
- `alignment.md` — ontology alignment (LLM + concept-mapping tool).
- `alignment-via-http.md` — turnkey curl + jq pipeline for calling the local hybrid `/map/batch` endpoint directly. Use when you have Bash + network access but no Python client (Claude Code is the common case).
- `judge.md` — per-item quality judge.
- `humanfeedback.md` — apply human reviewer edits.
- `extractor-abcd.md` — ABCD/HBCD extractor: variables (as mentioned), constructs, models, findings with roles/directions, each with a verbatim quote + section/page.

### `schemas/`
- `ner-output.schema.json` — JSON Schema for NER output. **Task-agnostic — keep it that way**; cell-specific constraints live in the two files below.
- `cell-ner-output.schema.json` — per-paper CNS cell NER output. Superset of the generic NER schema: the closed cns-cells label taxonomy (enforced for LLM-extracted items only, since the HF ensemble legitimately emits `Anatomy`/`Gene`/`CellLine`), the `cell_context` block, `specificity`, `coordinated_elements`, and a rule that a `cell_vague` item **must** carry a null `ontology_id`.
- `cell-ner-corpus.schema.json` — the corpus roll-up written by `scripts/merge_corpus.py`.
- `resource-output.schema.json` — JSON Schema for resource output.
- `aligned-item.schema.json` — fragment schema for any aligned item (adds ontology + provenance fields).
- `judged-item.schema.json` — fragment schema for any judged item (adds judge_score + remarks).
- `abcd-paper.schema.json` — ABCD/HBCD per-paper result: variables (with `mention_as_written`, `dictionary_status`, `nda_or_nbdc_table`, `nbdc_domain`), constructs, models, findings, `rejected[]`, `verification`, and provenance including every dictionary snapshot consulted.
- `abcd-synthesis.schema.json` — cross-paper synthesis: per-construct consensus/divergence verdicts, per-variable role consistency, variable↔construct links, and the `method` block recording the thresholds a verdict was reached under.

### `scripts/` (runnable helpers)
- `chunking.py` — sentence-aligned chunking, span re-anchoring, deduplication.
- `json_repair.py` — four-tier JSON repair (strict → fences → json-repair → truncate-to-balanced) + schema-driven LLM repair.
- `span_validator.py` — validate `text[start:end] == entity`, repair from sentence context.
- `mask_pass.py` — build masked text for the mask-recall pass (offset-preserving placeholders), translate offsets back, and mask single items for the mask-verify pass.
- `stats.py` — compute the `stats` block (totals, label histogram, by-source-model histogram, alignment provenance, judge score buckets, per-stage timings) and a human-readable summary.
- `group_by_entity.py` — collapse raw mentions into `entities_grouped[]` keyed by canonical `(entity, label)`: collects all `mentions`, deduplicates `sentences` across locations, lists every contributing `source_model`, and reports `consensus_count`. Also exposes `unify_ontology_across_entities()` — when the same surface form gets different ontology IDs from different chunks/models, pick the best one (tool-mapped > LLM > unmapped) and apply it to every occurrence. Both run automatically in `attach_grouped_views()`.
- `ner_models.py` — HuggingFace NER ensemble (biomedical + clinical specialists). Default roster: d4data, BC5CDR-chem, NCBI-disease, BioBERT-genetic, plus the BENT-PubMedBERT family (Gene / Chemical / Disease / Anatomical / Cell-Type / Cell-Line / Organism / Bioprocess). Picked by profile: `biomedical_broad` / `cns_cells` / `pharmacology` / `genetic` / `clinical` / `minimal` / `all`. Every emitted item carries a `source_model` provenance field.
- `normalize_result.py` — **idempotent post-processor**. Lifts per-entity `paper_title`/`doi` into top-level `source_metadata`, strips the per-entity dupes, tags missing `source_model` + `alignment_method`, infers `task_type`, runs **strict IRI validation** (demotes `llm_knowledge` and malformed IRIs), attaches `entities_grouped[]`, and computes `stats` (with prominent `totals` block at the top). **Runs automatically** in `pipeline.py` before saving. Also exposed as a CLI: `python -m scripts.normalize_result legacy.json --input paper.txt --llm-model …`. This is the safety net that guarantees the canonical shape even when the LLM ignores the prompt.
- `iri_validation.py` — **strict IRI validator**. Per-ontology regex patterns + permissive structural fallback. Rejects `concept_mapping_provenance: "llm_knowledge"` outright (zero hallucination policy), demotes malformed IRIs to `unmapped`, accepts legitimate cross-ontology mappings (e.g. CIDO results that reuse HP IRIs). Adds `result["validation"]` with `passed` / `demoted` counts and `demoted_by_reason` breakdown.
- `input_loader.py` — **PDF / CSV / TXT / MD** ingestion. PDF backends in order: GROBID (if reachable) → PyMuPDF (`fitz`) → pdfminer.six. Graceful fallback so it works with whichever library is installed. Also writes a sibling `<stem>.txt` so subsequent NER stages have stable character offsets. CLI: `python -m scripts.input_loader paper.pdf [--no-grobid] [--grobid-url …]`.
  Captions and tables are the thing to watch: the GROBID path used to drop them entirely, and `caption_coverage()` / `warn_if_captions_missing()` now report it on every backend. Cascade is GROBID → pymupdf4llm → PyMuPDF → pdfminer.
- `task_detection.py` — **auto-detect task type** from a free-text task description: heuristic regex first (fast, no LLM), then LLM fallback via `llm_client`. Returns a `TaskDetection` with `task_type` (`ner`/`resource`/`structured_extraction`/`relation_extraction`/`keyphrase_extraction`/…), `confidence`, `labels`, `rationale`.
- `model_context.py` — **model context-window registry** (~50 model families, longest-match wins) + token-aware `compute_downstream_chunk_size(...)` for sizing alignment/judge/humanfeedback chunks. CLI: `python -m scripts.model_context openrouter/anthropic/claude-sonnet-4-6 --items 2000 --workers 8`.
- `bioportal_map.py` — throttled + LRU-cached BioPortal client.
- `merge_corpus.py` — **corpus roll-up (rule 9b)**. Merges per-paper `*_final.json` into `<stem>.json` + `<stem>.md` (`--out`, default `corpus_synthesis`, mirroring `abcd_synthesize.py`): one canonical row per entity across all papers, per-document counts, cross-paper ontology conflicts, and specificity totals. Groups with the same `_canonical_key` as per-paper `entities_grouped`, so corpus counts reconcile against per-paper counts. Recomputes totals from the items rather than summing each file's `stats`, so one stale block can't corrupt the total. No LLM call. `--include-mentions` embeds the raw union, `--no-index` gives roll-up only.
- `fetch_fulltext.py` — **structured full text without a PDF or GROBID**. PMCID/PMID → publisher XML (NCBI BioC → Europe PMC JATS → NCBI efetch), keeping figure captions and table cells as first-class content. Open-access only, and it says so rather than falling back to a caption-less parse. Via the BioC source the passage segmentation matches a BioC gold standard exactly. No key, no server; `NCBI_API_KEY` only raises a rate limit.
- `ols_map.py` — EBI OLS client (no API key).
- `local_hybrid_map.py` — client for a self-hosted BM25+dense mapping service (one POST, many terms).
- `llm_client.py` — provider-agnostic LLM call (OpenAI / OpenRouter / Anthropic / Ollama / Gemini).
- `pipeline.py` — reference end-to-end pipeline (extract → align → judge) wiring the helpers together. `--input` takes a file **or a directory** and is repeatable; several inputs run in turn, one failure does not abort the batch (exit 2 = partial, 1 = none succeeded), and the corpus roll-up runs at the end (rule 9b).
- `abcd_context.py` — **context-aware mapping from a paper's wording to a dictionary variable**. `Dictionary.resolve()` answers "is this string a variable name?", which most papers never satisfy; this answers "which variable did this sentence mean?" by matching against dictionary *labels* with the instrument, respondent, metric and release the paper stated. Returns one variable, a family, a domain or an instrument table — never a guess — with the candidate list and thresholds attached. CLI: `match` / `instrument` / `stats`.

- `abcd_nda_api.py` — **NDA data-element API**: confirm a printed element name (with its structures and aliases), or full-text search element descriptions. Hits are intersected with the loaded dictionary's tables, and search results are suggestions rather than mappings. Cached under `~/.cache/structsense/nda_api`. CLI: `element` / `search`.

- `abcd_dictionary.py` — **ABCD/HBCD variable dictionary**. Builds release snapshots from NBDCtools (`nbdctools` on PyPI reads `lst_dds` without R) or from your own CSV export, with provenance (source, sha256, retrieval time). `Dictionary.resolve()` decides whether a string from a paper IS a real variable — exact name → normalised name → full label/description, never fuzzy — and `releases_for()` surfaces renames across releases. CLI: `build` / `info` / `lookup` / `search`.
- `cognitive_atlas.py` — Cognitive Atlas client (~918 concepts, ~856 tasks), cached to disk after one fetch. Exact/singular/alias matching only; an unmatched construct stays unmapped rather than being guessed. CLI: `refresh` / `map` / `search`.
- `abcd_verify.py` — **the ABCD verifier**. Anchors every `evidence.quote` in the paper's own text (whitespace/ligature-normalised, re-anchoring offsets but never inventing quotes), applies the per-section surface rules, gates variables against the dictionary and constructs against the Atlas, and returns `rejected[]` + a `verification` summary.
- `abcd_extract.py` — driver taking **one argument, auto-detected**: a PDF, a directory, a CSV/TSV/XLSX of DOIs, a DOI list, or a bare DOI. load → chunk → LLM extract → merge → verify → write `<stem>_abcd.{json,md,ttl}`. More than one paper implies a synthesis (`--no-synthesize` to skip); `--reverify` re-checks an existing extraction with no LLM calls.
- `abcd_inputs.py` — the input resolver. Detects single vs bulk vs DOI table, and fetches **open-access** PDFs for DOIs (Unpaywall → OpenAlex → Semantic Scholar). Downloads are magic-byte verified, so a paywall answering `200 text/html` is reported as unresolved rather than saved as a broken PDF. Records service, URL, license and sha256 per fetch.
- `abcd_synthesize.py` — cross-paper synthesis: `claims[]` with per-paper evidence, strength and contradictions; consensus/divergence per construct with the papers behind each direction and the variables that measured it; role consistency per variable with per-paper provenance and the dd release each mapping holds in; and a dataset row per paper. **Counts by paper, not by finding.**
- `abcd_export.py` — JSON + Markdown tables + Turtle writers shared by both drivers. The Turtle uses PROV-O plus a small `abcd:` vocabulary, carrying quote, `usedContext`, char offsets, section/page, `mentionAsWritten`, `ndaOrNbdcTable` and `nbdcDomain` into triples.

### `examples/`
- `ner-example.md` — end-to-end NER worked example.
- `resource-example.md` — end-to-end resource extraction worked example.
- `reproschema-example.md` — end-to-end PDF → ReproSchema worked example.

### `connecting/` (how to wire the skill into different LLM platforms)

All of these are **host-model mode** (see "Who runs the LLM stages") except the MCP
server and a deliberately headless `pipeline.py` run: the agent is the extractor, so
no LLM API key is involved. Codex CLI needs no guide of its own — it reads `SKILL.md`
and behaves like Claude Code here.

- `claude-code.md` — install as a Claude Code skill (`~/.claude/skills/` or `.claude/skills/`). Auto-discovery via the `SKILL.md` frontmatter. Also the reference for "why no API key is needed".
- `pi-dev.md` — install as a [Pi](https://pi.dev) skill (`~/.pi/agent/skills/`, `~/.agents/skills/`, or `.pi/skills/`). Pi is a CLI coding agent with native Agent Skills support and a built-in `bash` tool, so it runs the pipeline directly — same story as Claude Code.
- `claude-desktop.md` — **Claude Desktop has a split execution model**: chat UI on your machine, code interpreter in Anthropic's cloud sandbox (so it cannot reach your `localhost:8000` directly). Use the MCP server config in this guide to bridge.
- `claude-skills.md` — upload as a hosted Anthropic Skill on claude.ai or use with the Claude Agent SDK.
- `custom-gpt.md` — wire as an OpenAI Custom GPT (Instructions + Knowledge files + optional server-side Action).
- `mcp-server.md` — expose the pipeline as an MCP server so any MCP-aware client (Claude Code, Cursor, ChatGPT desktop, custom agents) can call it.

## Minimal mental model

If you remember nothing else, remember this:

> Three short, focused prompts in sequence (extract, align, judge), each emitting strict JSON that the next prompt parses. Add a concept-mapping tool call inside alignment when you need real ontology IRIs. Chunk long inputs at sentence boundaries and merge by stable identifiers. Validate against a JSON schema.

That's the entire skill. The references and prompts here are the careful version of that one sentence.
