---
name: knowledge-base-rdf-ingestion
description: "Log in, ingest RDF triples into workspaces, search knowledge graphs, and query W3C PROV-O provenance via MCP tools."
license: Apache-2.0
tags:
- knowledge-base
- rdf
- semantic-web
---

# BrainKB Skills
This skill provides tools for ingesting, querying, and exploring **BrainKB (Brain Knowledgebase)**.

**Every BrainKB operation goes through the `brainkb_*` MCP tools. There is no
fallback.** If a tool errors, read the error and fix the cause — do not reach for
`curl`, a shell script, a different MCP server, or a direct HTTP call to
`queryservice`/`usermanagement`. Those paths bypass the identity the MCP holds, so
they either fail differently or succeed under the wrong attribution, and a mutation
attributed to the wrong caller cannot be undone. The only `curl` in this document is
the **operator's** deployment health check at the end, run on the deploy host by a
human, and it is not an agent fallback.

## Connectivity — READ FIRST

There are two ways to reach BrainKB, and the right one depends on where this code
runs:

- **Hosted remote — `https://mcp.brainkb.org/mcp` (live).** Works from anywhere,
  including cloud/sandbox sessions. Register it once:
  ```bash
  claude mcp add --scope user --transport http brainkb https://mcp.brainkb.org/mcp
  ```
  The operator has already configured the backend, so **do not pass `base_url`**
  to any tool here — see the allowlist note under *Credentials & safety*.
  Authenticate per caller (PAT via `Authorization: Bearer`, or the login tools).
- **Local stdio MCP → `http://localhost:8010`.** Only works when the caller runs on
  the **same machine** as the BrainKB Docker stack, through the local MCP process.
  A cloud/sandbox session **cannot** reach a `localhost` deployment on the user's
  laptop and no base URL will fix that — use the hosted remote instead.

Two notes on diagnosing failures:

- A **connection error / HTTP 000 / connection refused** means the caller can't
  reach the deployment — don't keep guessing URLs. For the local path, check the
  MCP is running and the stack is up (`http://localhost:8010/openapi.json` → 200 on
  that machine). Ask the user rather than retrying different hosts.
- `GET https://mcp.brainkb.org/mcp` in a browser returns **406 "Client must accept
  text/event-stream"**. That is the endpoint working, not an outage; `/` serves a
  plain landing page and `/healthz` returns `ok`.

Do not fall back to curl, a local script, or another MCP server from any session —
use the hosted remote's MCP tools, or stop and report what is blocking.

**Rate limits apply on the hosted remote** (per caller IP): roughly 8 logins, 40
writes/ingests, 120 reads and 30 admin calls per minute. A limited call returns
`status_code: 429` with a `detail` naming the bucket — surface it and wait out the
window. Never retry-loop, and never split one job into many calls to get around it.

## Credentials & safety

- **How to authenticate — pick in this order. Do NOT ask the user for a password
  by default; BrainKB is a Globus/OAuth-first system and password login is being
  retired.**
  1. **Already configured?** On the hosted remote each caller authenticates via an
     `Authorization: Bearer <token>` header, or a `BRAINKB_TOKEN` (PAT) set in the
     MCP config — in that case no login step is needed at all. Check with
     `brainkb_whoami()` before asking for anything.
  2. **Personal Access Token (PAT)** — the recommended browser-free credential.
     If the user has one, `brainkb_use_token("brainkb_pat_…")` (or they set it as
     `BRAINKB_TOKEN`). If they don't, mint one after step 3 with
     `brainkb_create_token(name, days)`.
  3. **Globus / ORCID / GitHub (browser)** — the normal way to sign in as a real
     user. Call `brainkb_globus_login()`; it returns a URL for the user to open,
     they sign in, the browser shows a short code, and you finish with
     `brainkb_finish_login("<code>")`. **This is what you should do when the user
     says "log in as <their account>" — start the Globus flow, do not ask for a
     password.**
  4. **Password (legacy, discouraged)** — only if the user *explicitly* has a
     password account and asks to use it: `brainkb_login(email, password)`. Never
     volunteer this path or prompt for a password unprompted.
- **Base URL**: on the hosted remote it is fixed by the operator — omit `base_url`
  entirely. For a local stdio MCP the default is `http://localhost:8010`; ask only
  if it isn't already set and the user hasn't said where the deployment is.
- **Never print, echo, or store the password or the JWT token.** Pass them straight
  to the login step, and keep them out of chat — in the operator's shell snippets
  read them from an environment variable, never inline. (The one exception is the PAT
  returned by `brainkb_create_token`, shown to the user **once** so they can copy it
  into their config — never re-display it afterward.)
- A PAT is **revocable instantly** (`brainkb_revoke_token`) and its roles are
  re-checked live on every use, so a ban/demotion takes effect at once.
- **Identity must be verified, never assumed — this is the #1 correctness rule.**
  Mutations (create space, ingest, add member, grant) are **attributed to the
  authenticated identity permanently** (provenance records who did what). A login
  step reporting "Logged in as X" is **not proof** the next call runs as X: the MCP
  silently falls back to a configured `BRAINKB_EMAIL`/`BRAINKB_PASSWORD`,
  `BRAINKB_TOKEN`, or an `Authorization` header when the session login isn't
  carried forward (common on the hosted `streamable-http` transport). So:
  1. After **every** login, call `brainkb_whoami()` and confirm `email` == the
     intended user.
  2. **Immediately before any write/mutation**, call `brainkb_whoami()` again and
     confirm it still matches. Only proceed if it does.
  3. If it shows a **different/unexpected** account (e.g. a shared `test@…`),
     **STOP** — report the mismatch, don't write. The durable fix is a per-call
     credential that can't be shadowed: a **PAT** (`BRAINKB_TOKEN` /
     `brainkb_use_token`) or an `Authorization: Bearer` header. A leftover
     `BRAINKB_EMAIL`/`BRAINKB_PASSWORD` in the MCP config is the usual culprit and
     should be removed on a shared/multi-user MCP.
- Confirm before mutating actions (creating a space, ingesting, changing
  visibility, adding members). Reads are safe.
- **Authorization is role-based, not just JWT** (see the section below). A `403`
  usually means the user's **role/capability** (or a space access rule) doesn't
  permit the action — not that the API token is invalid. Explain which
  role/capability is needed and that an Admin can grant it.

## Core concepts (so you pick the right call)

- **Space** = an owner-controlled workspace containing named graphs, with
  `visibility` = `private` (members only) or `public` (anyone, even without
  logging in, can read). Two `space_type`s: **individual** (a personal space) and
  **team** (shared). Ingest into a graph requires owner/editor membership of its
  space *and* the ingest capability.
- **Roles govern what a user may do** (JWT is only API access). Roles come from the
  user's account; they map to capabilities like create-space / ingest / admin.
- **Ingestion is submit-and-forget**: it returns a `job_id` and runs in the
  background. Always poll job status rather than assuming it finished.
- **Provenance** lives natively in the graph DB (PROV-O). Every ingest is an
  activity; each job's added triples are a queryable **delta**.
- **A SynthScholar review reaches BrainKB by being ingested, like any other RDF.**
  The `synthscholar` skill runs the review and writes `review.ttl`; a user with
  write access ingests it here, into the graph
  `https://brainkb.org/synthscholar/reviews/<review_id>/` bound to a space. Going
  through the ingest pipeline is what gives the review a job, PROV-O provenance and
  a search index. See "Ingest a SynthScholar review".

## Authorization (roles & capabilities)

Who can do what is decided by the user's **role** → **capability**, then space
membership, then any per-space **access rule**. Key rules to set expectations:

- **Create a team space**: Admin/SuperAdmin only — or a user an admin has **granted**
  `create_team_space`. Use `space_type="team"`.
- **Create an individual/private space**: any write-capable role (Curator, Lab
  Member, Submitter, Annotator, Mapper, Knowledge Contributor, Admin). Default
  `space_type="individual"`.
- **Ingest / recover**: write-capable role (+ owner/editor of the space).
- **Arbitrary SPARQL**: Admin/SuperAdmin only.
- **No role**: read **public** content only — cannot create/ingest/read private.
- **Delegated upgrades** (Admin only): `brainkb_grant_capability(member, capability)`
  — e.g. let a Lab Member create team spaces. Inspect with
  `brainkb_capabilities(member)`. Admin-only caps (`grant`, `sparql_admin`) are not
  delegatable.
- **Fine-grained per-space rules**: within a space, restrict an action to a role /
  member / space-role (see "Manage & delegate"). Owner + Admin always bypass.

If an action is denied, check the user's roles/capabilities
(`brainkb_capabilities`) and either ask an Admin to grant the needed capability, or
adjust the space's access rules.

## Workflows

### 0. Register a new account (no login needed)
For password-based signup: `brainkb_register(full_name, email, password)`. This
creates the credential **and** a canonical profile with a default `Curator` role,
so the user is a first-class identity. The account starts **inactive** — an
Admin/SuperAdmin must activate it (see §9) before login works. (Alternatively,
users can onboard by first login via Globus/ORCID/GitHub, which auto-provisions
the same profile + default role.) Never echo the password back.

### 1. Log in

**Auth order (TL;DR) — take the first that applies:**
1. `brainkb_whoami()` → if `authenticated: true` (a PAT/header is already
   configured), **stop, you're done.**
2. User has a PAT → `brainkb_use_token("brainkb_pat_…")` (or it's set as
   `BRAINKB_TOKEN`). Best for repeated use — survives across calls, no browser.
3. Need to sign in as an account → **Globus** (`brainkb_globus_login` →
   `brainkb_finish_login`). Then mint a PAT (`brainkb_create_token`) so future
   sessions skip the browser.
4. Password (`brainkb_login`) → **only** if the user explicitly has one. Never
   prompt for a password on your own.
Always `brainkb_whoami()` again after logging in to confirm the identity stuck
(see the ⚠️ box below). PAT/header = per-call identity (reliable); in-session
login can evaporate on the hosted remote.

**Local (stdio) vs hosted remote — how the PAT is passed:**
- **Local/stdio:** put the PAT in `BRAINKB_TOKEN` (config env). Simple, single-user.
- **Hosted remote (`mcp.brainkb.org`, streamable-http):** each caller sends their
  PAT as an **`Authorization: Bearer <pat>`** header — a baked-in `BRAINKB_TOKEN`
  is **ignored** there (it would make every anonymous caller act as one shared
  identity) unless the operator sets `MCP_ALLOW_SHARED_IDENTITY`. So on the remote
  it's per-caller header, not a shared env token.
- The backend URL is **allowlisted** (`MCP_ALLOWED_BASE_URLS`): `base_url` /
  `X-BrainKB-Base-URL` can only point at pre-approved backends (that URL is where
  credentials are sent). An unknown base URL is refused — don't try to work around
  it by guessing hosts.

**First run `brainkb_whoami()`** — if it already reports `authenticated: true`
(header token or `BRAINKB_TOKEN` PAT is configured), you're done; don't ask for
anything.

**If it reports `authenticated: false`, do NOT stop and offer the user a menu of
auth methods.** Immediately call `brainkb_globus_login()` and hand over the URL it
returns — that is the only path that works from a cold start, so presenting it as
a choice just adds a round trip. Then take the code they paste,
`brainkb_finish_login("<code>")`, and **mint a PAT in the same turn** with
`brainkb_create_token(name="laptop", days=90)` so the next session doesn't repeat
any of this. Only ask the user something if they *offer* a PAT, or if the login
itself fails.

Two things not to say while doing it:

- Don't read `base_url` as the user's own machine. It is the **server's** backend,
  not what the client connected to. On the hosted remote it reads
  `http://host.docker.internal:8010` — that is the MCP's *co-located* stack inside
  the deployment, and it is correct. Never tell the user they're "pointed at a
  local stack" or that their PAT might be for the wrong backend because of it.
- Don't warn that an in-session login "won't stick" before trying. Within one
  session it persists; it just doesn't carry into the *next* session — which is
  what minting the PAT solves.

For reference, the methods in preference order — **default to Globus, never prompt
for a password unprompted:**

- **Globus / ORCID / GitHub (browser) — the default for "log in as <account>":**
  1. `brainkb_globus_login()` (or `brainkb_globus_login("orcid")` / `("github")`)
     → returns a URL; give it to the user to open and sign in.
  2. The browser then shows a short one-time **code** — ask the user to paste it.
  3. `brainkb_finish_login("<code>")` → completes login for this session.
  The browser sign-in is unavoidable (only the user can consent at the provider),
  but the rest stays in the skill. First OAuth login auto-creates/links the
  profile + a default `Curator` role. **When a user asks to sign in as a specific
  account and no PAT/header is configured, start THIS flow — do not ask for a
  password.**
- **Personal Access Token (PAT) — recommended for repeated use, no browser:**
  1. `brainkb_use_token("brainkb_pat_…")` if the user already has one — done.
  2. To mint one: log in once (Globus, above), then
     `brainkb_create_token(name="laptop", days=3)` → returns a `brainkb_pat_…`
     token **once**. Give it to the user to copy.
  3. The user sets it as `BRAINKB_TOKEN` in the MCP config (or calls
     `brainkb_use_token("<pat>")` per session). No login/browser afterward until
     it expires (default 3 days; pass `days` up to the server cap for longer).
  - Manage: `brainkb_list_tokens()` (metadata only), `brainkb_revoke_token(id)`
    (instant). PATs are the cleanest way to avoid re-authenticating every session.
- **Password (legacy, discouraged — being retired):**
  `brainkb_login(email, password, base_url?)`. Use **only** if the user explicitly
  says they have a password account and want to use it. Never prompt for a password
  otherwise.

> **⚠️ ALWAYS verify identity after logging in — do not trust the login message.**
> Immediately after `brainkb_finish_login` / `brainkb_login` / `brainkb_use_token`,
> call **`brainkb_whoami()`** and confirm the returned `email` is the account you
> intended. A login step can report "Logged in as X" yet subsequent calls run as a
> **different** account — because the MCP falls back, silently, to a configured
> `BRAINKB_EMAIL`/`BRAINKB_PASSWORD` (or `BRAINKB_TOKEN`, or an `Authorization`
> header) when the just-established session isn't carried into the next call (this
> is common on the hosted `streamable-http` transport, where per-session login may
> not persist between tool calls). **If `whoami` shows a different or unexpected
> account, STOP — the login did not take effect. Do NOT create/ingest/mutate**
> (see the identity rule in "Credentials & safety"). The reliable fix is a
> per-call credential that can't be shadowed: a **PAT** via `BRAINKB_TOKEN` /
> `brainkb_use_token`, or an `Authorization: Bearer` header — not an in-memory
> session login on a multi-user remote.

**Troubleshooting login/auth (common failures):**
- **`brainkb_globus_login` → the browser ends on `…?error=unauthorized_client`.**
  The Globus app is the **wrong type**: it must be a **"Portal / application you
  host"** (confidential OAuth client), NOT a **"Service API"** app. A Service-API
  app can't run the login (authorization-code) flow, so Globus rejects it. Fix is
  server-side (register a Portal-type app); as the agent, tell the user this rather
  than retrying — a new code won't help.
- **`…?error=…redirect… mismatch` / "Mismatching redirect URI".** The backend's
  `USERMANAGEMENT_PUBLIC_BASE_URL` doesn't match the redirect registered on the
  Globus app (e.g. `localhost` vs the public host, `http` vs `https`, a typo). Also
  server-side; retrying won't help.
- **`finish_login` says "Logged in as X" but `whoami` says `authenticated: false`
  (or a different user).** The in-session login didn't persist across calls — the
  hosted `streamable-http` transport may give each call a fresh session. Don't keep
  re-running the browser flow. Switch to a **PAT**: set `BRAINKB_TOKEN` (or
  `brainkb_use_token`), which authenticates per-call and survives. On the multi-user
  remote, an `Authorization: Bearer` header per request is the intended model.
- **`401` on a call after you were "logged in".** Session/PAT expired — re-auth
  (prefer a fresh PAT). `403`, by contrast, means authenticated-but-not-permitted
  (a role/capability/access-rule issue), not a token problem.
Call `brainkb_login(email, password, base_url?)`. Confirm with `brainkb_whoami()`.
(New accounts must be activated by an admin first — see §9.)

### 2. Create / choose a workspace (space)
- Individual/private workspace (any write-capable role):
  `brainkb_create_space(slug, name, "private", description)` (space_type defaults to
  "individual").
- Team space (Admin/SuperAdmin, or a user granted `create_team_space`):
  `brainkb_create_space(slug, name, "private", description, space_type="team")`.
  If the user isn't authorized you'll get a 403 — an Admin can grant them
  `create_team_space` (see "Manage & delegate").
- Bind a named graph to it (required before ingesting into that graph):
  `brainkb_add_space_graph(slug, graph_iri, description)` — `graph_iri` like
  `https://brainkb.org/graph/<slug>/`.
- **Always pass a non-empty `description`** when registering a graph (and when
  creating a space). The description is stored in the graph registry and surfaces
  in provenance / listings — leaving it blank leaves the graph undocumented (it
  shows up with an empty description). If the user didn't give one, ask for a short
  description, or derive a sensible one from the space/graph name and the data
  being ingested; don't silently register with an empty description.
- **Uniqueness (enforced by the backend):** a space `slug` is **globally unique**
  and a named-graph IRI is **globally unique** (one graph belongs to exactly one
  space). Creating a space with a taken slug, or binding an already-registered
  graph, returns **409** — pick a different slug / IRI. Don't retry the same value.
- **Deletion — what is and isn't removable:** spaces and named graphs are
  **permanent — there is NO delete** (preserves provenance/history, same "we don't
  hard-delete" policy as user accounts). What you *can* remove: a **space member**
  (`brainkb_remove_*`/members endpoint) and a **fine-grained access rule**
  (`brainkb_remove_access_rule`). To retire a space in practice, set it private
  and/or remove members — you cannot delete it. So choose slugs/graph IRIs
  deliberately: a typo can't be deleted, only abandoned.
- **See what's available to the user + their permission:** `brainkb_list_spaces()`
  returns each visible space annotated with the caller's own permission —
  `your_role` (`owner`/`editor`/`viewer`/`null`), `is_owner`, `access`
  (`owner`/`member`/`public`), and `can_write` (their space role permits ingest;
  a real ingest also needs the `ingest` capability + any per-space access rules).
  Use it to tell the user which spaces they can **write** to vs. only **read** vs.
  only see as **public**, rather than guessing.

### 3. Ingest
- **Before ingesting, verify identity: call `brainkb_whoami()` and confirm the
  `email` is the intended user.** Ingest is **attributed** — the job's `user_id`
  and the provenance (`prov:wasAssociatedWith` / `prov:wasAttributedTo`) are set to
  the authenticated identity, permanently. If `whoami` shows the wrong account
  (e.g. a fallback `test@…` from a stale `BRAINKB_EMAIL`), the data will be
  **mis-attributed and cannot be silently reassigned** — STOP and fix the login
  (use a PAT / header) before ingesting. Never ingest "hoping" the earlier login
  stuck.
- **Ingesting "into a space" → resolve the graph first.** Ingest targets a
  **named graph IRI**, not a space. When the user says "ingest into the *hmba*
  space", first find that space's graph: `brainkb_list_spaces()` (or
  `brainkb_read_space("hmba")`) → use its registered graph IRI. If the space has
  no graph yet, `brainkb_add_space_graph(slug, graph_iri, description)` first
  (owner/editor). Then ingest into that `graph_iri`.
- **A file, on the hosted remote: upload it, then ingest by id.** Run this (or have
  the user run it) — the HTTP library reads the file off disk, so not one byte enters
  your context:
  ```python
  import requests, hashlib, pathlib
  f = pathlib.Path("review.ttl")
  r = requests.post(
      "https://mcp.brainkb.org/upload",
      params={"filename": f.name,
              "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
              "graph": "https://brainkb.org/graph/my-lab/"},   # omit to stage only
      headers={"Authorization": f"Bearer {TOKEN}"},
      data=f.open("rb"),          # streamed — never buffered, never in context
  )
  print(r.json())
  ```
  With `graph` set the server submits the ingest itself and answers `202` at once —
  upload and forget; poll `brainkb_upload_status(upload_id)` until it reports a
  `job_id`. Without it you get a staged `upload_id` for
  `brainkb_ingest_upload(graph_iri, upload_id)`. **5 GB per file**, and it needs
  nothing but the PAT the user already has — no operator change.
- Raw text: `brainkb_ingest_text(graph_iri, data)` (Turtle/N-Triples/JSON-LD).
- Files: `brainkb_ingest_files(graph_iri, [paths])`. The tool **opens the file and
  uploads the bytes**, so the file must exist on the machine running the MCP
  *process* — on the hosted remote that is the server, not the user's laptop. Remote
  file ingest is therefore **disabled unless the operator set `MCP_INGEST_ROOT`**,
  and paths must sit inside that directory.
- Both return a `job_id`. Tell the user ingestion is running in the background.

**Never re-emit a file's RDF through `brainkb_ingest_text`.** This is the rule that
matters most in this whole section, because breaking it is unrecoverable:

- `ingest_text` takes the RDF as a *string*, which means the bytes pass through the
  model. Turtle is dense and full of exactly what gets silently altered in
  transcription — ligatures (`speciﬁc`), Greek (α, β), embedded newlines, escaped
  quotes, long IRIs. Byte-exact reproduction of a real file is not something to
  gamble on.
- Ingest is **append-only**. There is no delete for triples and no unregister for a
  graph. One mangled literal is in that graph permanently, and the provenance record
  records it as yours.
- So `ingest_text` is for RDF **you authored in this session** — a handful of triples
  you just constructed and can see in full. It is not a transport for a file.

**Never split one RDF document across several ingest calls.** Not "carefully", not
"at subject boundaries" — the reason is not size, it is identity. Blank-node labels
(`_:b10`) are scoped to a single document, and each `ingest_text` call is a separate
parse. A blank node referenced in call A and call B becomes **two different nodes**,
so the triples hanging off it detach from the subject they describe. The result is a
graph that ingests cleanly, reports success, and is quietly wrong — in an
append-only store. A real review export hits this immediately: its `content_text`
literals hang off shared blank nodes, and the only unit that is safe to send alone
is a whole subject closure, which for that file was 409 KB.

**Never split RDF as text.** If a payload genuinely exceeds the raw-text cap
(`MCP_MAX_INGEST_BYTES`, 10 MB by default), splitting on blank lines or statement
boundaries cuts inside multi-line `"""` literals and produces chunks that still
parse individually while losing triples. Split with a real parser (rdflib, at
subject boundaries), and reconcile the triple count of the parts against the whole
before ingesting anything. A file under 10 MB needs no splitting at all — the cap is
not the reason a large file fails on the remote; the filesystem boundary is.

**Deciding what to do with a file the user hands you:**

| Situation | Do this |
|---|---|
| Hosted remote, file on the user's machine | **`POST /upload` then `brainkb_ingest_upload`** — the normal answer. A few lines of `requests` with their PAT; the library moves the bytes, you never see them. Pass `graph=` to make it fire-and-forget |
| File is on the machine running the MCP process (local stdio) | `brainkb_ingest_files` — bytes stream from disk, nothing passes through the model |
| Hosted remote, `MCP_INGEST_ROOT` set, file already inside it | `brainkb_ingest_files` with a path under that root |
| Hosted remote, uploads disabled (`MCP_UPLOAD_ENABLED=false`) | **Stop and hand it to the operator**: they re-enable uploads, or set `MCP_INGEST_ROOT` plus a bind mount for data already on the server. Do not chunk it, do not retype it, do not offer a "test with one chunk" compromise — a partial ingest of mangled data is worse than no ingest |
| RDF you generated in this session, small enough to see whole | `brainkb_ingest_text`, with `sha256=` |

`brainkb_ingest_text` accepts `sha256=` and `expected_bytes=`. Use them every time
the RDF has a canonical form you can hash (`shasum -a 256 file.ttl`, `wc -c`): the
server compares them against what actually arrived and **refuses the write on any
mismatch**, which is the difference between a clean rejection and permanent
corruption. A digest mismatch is the guard working — do not retry by re-typing the
RDF, because the second attempt is no more faithful than the first.

**Verify every ingest against a count you knew in advance.** After the job reaches a
terminal state, `brainkb_delta(job_id)` reports the exact triples it added. Compare
that number to the source's triple count. A silent shortfall is the characteristic
failure of any path that moves RDF through text, and it looks like success until
someone counts.

### 3a. Ingest a SynthScholar review (PRISMA literature review)

This is the handoff from the **`synthscholar` skill**: it runs the review and writes
`review.ttl`; this skill puts that file into a space, through the normal ingest
pipeline, so the review gets a job, PROV-O provenance and a search index like any
other data. Nothing about the ingest itself is special-cased; what this section adds
is the IRI convention and the mistakes that are unrecoverable in an append-only
store.

**Where the TTL comes from.** Either source, same procedure from step 2 on:

- **A local run** (the usual case) — the `synthscholar` skill's
  `scripts/export_review.py … --formats md ttl` leaves `out/review.ttl` on disk.
- **A hosted review** on mlservice — export it:
  `GET https://mlservice.brainkb.org/api/synth-scholar/public/reviews/<id>/export?format=ttl`
  (published reviews need no credential; `/api/synth-scholar/public/reviews` lists
  them). An unpublished one needs an ml_service token, which these MCP tools do not
  hold — have the user export it from the SynthScholar UI and give you the path.

**Steps.**

1. `brainkb_whoami()` — confirm the email. This is the whole point of ingesting
   through the pipeline: the job, `prov:wasAssociatedWith` and the delta are
   attributed to this identity, permanently. If it is a stale fallback account, the
   review's provenance names the wrong person and cannot be reassigned.
2. Count the triples **before** sending, and keep the number:
   ```bash
   python -c "import rdflib;g=rdflib.Graph();g.parse('out/review.ttl');print(len(g))"
   ```
   This is step 7's baseline. The `synthscholar` skill runs the same check after
   export, so the number may already be in hand.
3. Pick the space and confirm it with the user. `brainkb_list_spaces()` shows
   `can_write` and `visibility` — see the visibility note below before choosing.
4. **Derive the graph IRI from the review id — don't invent one.** It is always:
   ```
   https://brainkb.org/synthscholar/reviews/<review_id>/
   ```
   `<review_id>` is the review's own id, verbatim: `review_0001_20260505234027`
   from mlservice, `review_local_<timestamp>` from a local run. It is
   `protocol.review_id` in the TTL and the `review_id` field in the API — read it,
   don't compose one. One review, one graph, one IRI, wherever it ran; that is what
   makes a review addressable across spaces and re-findable later. (The registry
   normalises to a trailing slash, so include it.)

   Then register it (owner/editor):
   `brainkb_add_space_graph(slug, graph_iri, "PRISMA review — <research question>")`.
   Give the description the research question, not the review id. A registry entry
   reading `review_0001_20260505234027` tells the next person nothing, and graph
   bindings are permanent — there is no rename. A 409 means this review is already
   bound to a space: that is the answer, not an error to work around. Stop and check
   whether it was already ingested rather than registering a variant IRI.
5. Upload, then ingest. **A review export is megabytes** (one subject closure alone
   measured 409 KB), so this is the upload path, not `brainkb_ingest_text` — the
   "never re-emit a file's RDF" rule above was written about this exact file:

   ```python
   import requests, hashlib, pathlib

   f = pathlib.Path("out/review.ttl")
   GRAPH = "https://brainkb.org/synthscholar/reviews/review_0001_20260505234027/"

   print(requests.post(
       "https://mcp.brainkb.org/upload",
       params={"filename": f.name,
               "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
               "graph": GRAPH},
       headers={"Authorization": f"Bearer {TOKEN}"},
       data=f.open("rb"),          # streamed off disk — never enters context
       timeout=600,
   ).json())
   ```

   On a local stdio MCP with the file on the same machine,
   `brainkb_ingest_files(GRAPH, ["out/review.ttl"])` does the same thing directly.
6. Poll `brainkb_upload_status(upload_id)` for the `job_id`, then
   `brainkb_job_status(job_id)` to a terminal state.
7. Reconcile `brainkb_delta(job_id)` against step 2's count, and report both numbers.
   A shortfall is the characteristic failure of anything that moves RDF, and "job
   done" will not show it.

Then the review answers `brainkb_search`, `brainkb_read_space`,
`brainkb_provenance_graph` and `brainkb_delta`. Note the `synthscholar` skill's Mode 2
SPARQL recipes still run against the **exported `.ttl`**, not the graph — arbitrary
SPARQL on BrainKB needs an Admin role. Keep the file; ingesting doesn't replace it as
the analysis surface.

**Ingest each review exactly once.** Review ids are unique, so distinct reviews never
collide — the hazard is re-ingesting the *same* review into the *same* graph. Ingest
is append-only with no replace, and a review export hangs its `content_text` literals
off **blank nodes**, whose identity is per-parse: the second pass does not
de-duplicate, it creates a disconnected copy of every abstract, permanently. So a
409 from `brainkb_add_space_graph` is the guard doing its job — it means this review
already has a graph. Check whether it was ingested before you send anything.

A re-run is a different review with a different id (mlservice mints a fresh
`review_<counter>_<ts>` per session, and a local run mints a fresh
`review_local_<ts>`), so it gets its own IRI without any special handling. The one
case to watch is a hand-edited `protocol.json` that pins `review_id` across runs —
then two different result sets claim one IRI.

**Visibility follows the space, not the review.** `is_public` on a hosted review
governs the SynthScholar API only. Once ingested, the triples are readable by
whoever can read the space — so ingesting an unpublished review into a public space
publishes it. Name the target space and its visibility when you ask the user to
confirm.

**Pass the exact IRI you registered, trailing slash included.** The registry check
normalises (`check_named_graph_exists` appends a `/` before looking), but the ingest
writes to the IRI **as given** — `create_job(graph=named_graph_iri)`, verbatim. So
registering `…/<review_id>/` and then ingesting into `…/<review_id>` passes every
check and silently lands the data in a *second, unregistered* graph one character
away from the right one. Nothing reports this; the job succeeds.

**Operator note: one writer per review.** ml_service can also push a completed
review's RDF straight into Oxigraph (`SYNTH_SCHOLAR_GRAPHDB_NAMED_GRAPH_PREFIX`, HTTP
PUT with `replace=true`), bypassing query_service — no job, no PROV-O, no search
index, and no space, so only an Admin SPARQL query can see the result. Its IRI is
`prefix + review_id` with **no** trailing slash, i.e. the near-miss above: with both
paths running you get two graphs per review, a governed one and an invisible shadow
copy, rather than one correct graph.

The direct push is therefore **off by default**
(`SYNTH_SCHOLAR_PUSH_TO_GRAPHDB=false`), leaving this ingest as the only writer. On an
unfamiliar deployment, a shadow graph is one holding triples under a review IRI that
does **not** appear in `brainkb_list_registered_graphs`.

For a deployment that ran with the push enabled, those graphs are also a latent
exposure: having no space, an index row for one would carry a NULL `space_id`, and
the search filter treats a NULL space as visible to **every signed-in user**. Nothing
indexes them today, but an admin running `POST /api/search/reindex` would make every
completed review, published or not, searchable by any authenticated account. Bind
review graphs to spaces before backfilling, not after.

### 4. Check ingest status
- `brainkb_job_status(job_id)` → status (`pending`/`running`/`done`/`partial`/
  `failed`/`error`), progress %, current file/stage, and per-file failures.
- Poll every few seconds until terminal; report success/failure counts. Use
  `brainkb_list_jobs()` to show recent jobs. If a job is stuck/errored, offer
  `brainkb_recover_job(job_id)`.
- For an upload staged via `POST /upload`, the job only exists once the server has
  submitted it: `brainkb_upload_status(upload_id)` reports `staged` → `submitting` →
  `submitted` (with the `job_id` to poll) or `failed`. A `failed` submission **keeps
  the staged bytes**, so retry with `brainkb_ingest_upload` — never re-upload, and
  never fall back to retyping the RDF.
- **Always finish by reconciling the count.** `brainkb_delta(job_id)` reports the
  triples the job actually added; compare it to the source's own count (`rapper -c
  file.ttl`, or rdflib). "Job done" plus a short count means data was lost, and it is
  the only way that failure ever becomes visible.

### 5. Read / search
- Search (access-filtered): `brainkb_search(q, space?, limit?)`. Omit `space` for
  a full search across everything the user may read.
- Read a whole space's RDF: `brainkb_read_space(slug)`.
- List registered graphs: `brainkb_list_registered_graphs()`.
- **"All named graphs in the store" is answerable without SPARQL.** The registry at
  `https://brainkb.org/metadata/named-graph` is not a partial view of the data
  graphs — it is all of them, for every space: both insert endpoints run an `ASK`
  against it (`check_named_graph_exists`) and refuse to ingest into a graph that is
  not registered, so no data graph can exist outside it. The rest of the store is
  fixed infrastructure, enumerated in the backend's own skip-list:
  `metadata/named-graph`, `metadata/spaces/`, `provenance/`, plus one
  `provenance/delta/{job_id}` per ingest job (from `brainkb_list_jobs()`). So the
  complete answer is `brainkb_list_registered_graphs()` + those four, and saying "I
  can't enumerate the store without SPARQL" is wrong. What SPARQL *is* needed for is
  **triple counts per graph** — there is no counting endpoint.
- Arbitrary SPARQL: `brainkb_sparql(query)` — **last resort.** It needs an
  Admin/SuperAdmin role (the `sparql_admin` capability), so for most users it 403s.
  Reach for the purpose-built tool first: "what graphs exist" is
  `brainkb_list_registered_graphs()`, not a SPARQL `SELECT DISTINCT ?g`; "what's in
  this space" is `brainkb_read_space(slug)`; "find X" is `brainkb_search(q)`;
  "what changed" is the delta tools below. Hand-writing SPARQL for a question one
  of those answers is how a 403 gets mistaken for a broken deployment.

**Telling "the tool is missing" from "the tool is disabled".** These look the same
from a failed call and are not: a tool absent from the server's `tools/list` means the
deployment predates it (the operator has not rebuilt), while a tool that answers 403
with a message naming an env var is present and switched off. Never report a feature
as "hidden because unconfigured" without checking which case it is — if the tool does
not appear in your available tools at all, the fix is a redeploy, not configuration.

**An empty result is not proof of absence.** `brainkb_list_spaces()` serves
anonymous callers a public-only view, so `{"spaces": []}` can mean *either* "you
own no spaces" *or* "your credential wasn't accepted and you were treated as
anonymous". Before telling the user they have nothing, confirm with
`brainkb_whoami()` **and** one auth-required call (e.g.
`brainkb_list_registered_graphs()`): if that 401s while `list_spaces` returns 200,
the empty list is an auth failure, not an empty account. Say "I couldn't confirm"
rather than "you have none."

### 6. Provenance
- Whole job: `brainkb_provenance_job(job_id)`.
- A graph's history: `brainkb_provenance_graph(graph_iri)` and
  `brainkb_delta_history(graph_iri)`.
- Exactly what a job added: `brainkb_delta(job_id)`.
- Compare two ingests: `brainkb_delta_compare(job_id_a, job_id_b)`.

#### "What changed / what's new?" — answering change-over-time questions
Yes, the skill can answer these — they're all built on the delta history (each
ingest records the exact triples it added, with a timestamp). Patterns:

- **"What changed on graph G over time?"** → `brainkb_delta_history(G)` — one entry
  per change (job, triple count, timestamp), newest first. That IS the change log.
- **"What's new on G (recently / since <date>)?"** → take `brainkb_delta_history(G)`
  (newest first) and report the top entries, or filter by their `generatedAtTime`
  ≥ the date. For the actual triples of a recent change, `brainkb_delta(job_id)`.
- **"What changed on a TEAM SPACE over time / what's new in the space?"** A space
  holds **several graphs**, and there is no single space-level feed — so:
  1. get the space's graphs: `brainkb_read_space(slug)` (or the space manifest from
     `brainkb_list_spaces`/get-space) → its `graphs` list;
  2. `brainkb_delta_history(g)` for **each** graph;
  3. **merge** the entries and sort by timestamp → a unified "what changed in this
     space" timeline; the newest few are "what's new."
  Say you aggregated across the space's graphs (so the user knows the scope).
- **"What did job A add vs job B?"** → `brainkb_delta_compare(A, B)`.
- **"Who changed it?"** → `brainkb_provenance_job(job_id)` / `provenance_graph` →
  the `prov:Agent` on each activity.

Caveat (the two clocks, below): this answers **when it was ingested/changed in
BrainKB**, not when a real-world event occurred. "What's new" = newly *ingested*,
not newly *happened*. And you only see changes in graphs/spaces the caller may
read (private-space deltas require membership).

#### Temporal & provenance querying — mind the TWO clocks
There are two different "when"s. Pick the right one for the question, and say
which you're answering:

1. **Transaction / ingestion time — "when was X *added/asserted*, and by whom?"**
   This is what the PROV-O layer records. Every ingest is a `prov:Activity` with
   `prov:startedAtTime`/`endedAtTime`, a `prov:Agent` (`prov:wasAssociatedWith`),
   and an `IngestionDelta` (`prov:generatedAtTime` + a `deltaGraph` holding the
   **exact** triples that job added). To answer "when/who added X":
   - `brainkb_delta_history(graph_iri)` → every change to that graph with its
     **timestamp** + job, newest first;
   - find the delta whose `deltaGraph` contains X, then `brainkb_delta(job_id)`
     for the exact triples and `brainkb_provenance_job(job_id)` for the agent/time.
   Use this for audit/"who put this here"/"what changed since <date>" questions.

2. **Domain / valid time — "when did X *actually happen* in the real world?"**
   PROV timestamps do NOT tell you this. A donor's birth date, when an experiment
   ran, a sample's collection date — those are **properties in the domain data**,
   not provenance. Answer them by querying that property in the graph (e.g.
   `brainkb_search`, or `brainkb_sparql` on the domain predicate), NOT via delta
   history.

Don't conflate them: "when was this record added" (clock 1) ≠ "when did the event
occur" (clock 2). If the user's "when X…" is ambiguous, ask which they mean, or
state which clock your answer used. Ingestion provenance can't substitute for a
missing domain timestamp, and vice versa.

### 7. Share publicly / manage a workspace
- Publish: `brainkb_set_space_visibility(slug, "public")` (owner/manager). Warn that
  a public space is readable by **anyone, including unauthenticated clients**.
- Add teammates: `brainkb_add_space_member(slug, email, "editor"|"viewer")`.

### 8. Manage & delegate (RBAC)
- **Admin vs SuperAdmin:** **SuperAdmin** is bootstrapped at deployment (env
  allowlist), is protected (can't be banned/deleted/demoted), and is the **only**
  role that can create/remove **Admins** or ban an Admin. **Admin** is granted by a
  SuperAdmin; same KG powers but itself manageable. Both manage **all** team spaces.
- **`manage_team_space` is scoped:** a non-admin with it manages **only** team
  spaces they **created (own)** or were **assigned to** (a member of / matched by a
  per-space `manage` rule) — never all team spaces. Only Admin/SuperAdmin manage all.
- **See the options first:** `brainkb_list_capabilities()` returns the catalog —
  all KG capabilities, which are delegatable (`grantable`), which are admin-only
  (`grant`, `sparql_admin`), and what each means.
- **Grant to an INDIVIDUAL** (Admin/SuperAdmin): inspect with
  `brainkb_capabilities(member)`; grant with
  `brainkb_grant_capability(member, "create_team_space")` (or `ingest`,
  `manage_team_space`, …); revoke with `brainkb_revoke_capability`.
- **Grant to a GROUP/role** (Admin/SuperAdmin): give a capability to *every* member
  of a role/group — including a custom group you created:
  `brainkb_grant_role_capability("uk_collaborator", "ingest")`;
  inspect with `brainkb_role_capabilities(role)`; revoke with
  `brainkb_revoke_role_capability`. Only `grantable` caps may be delegated
  (`grant`/`sparql_admin` are never delegatable — no escalation).
- **Custom groups**: create with `brainkb_create_role("uk_collaborator",
  "Community", "UK collaborators")`, assign with `brainkb_assign_role(email,
  "uk_collaborator")`, then grant it capabilities (above) and/or per-space access.
  A **new group starts with no powers** (read only) until you grant capabilities —
  creating/assigning it is not enough by itself.

  **Worked example — a group that can ingest, end to end:**
  ```
  brainkb_create_role("uk_collaborator", "Community", "UK collaborators")
  brainkb_grant_role_capability("uk_collaborator", "ingest")   # give the group the power
  brainkb_assign_role("alice@uk.org", "uk_collaborator")       # put a user in it
  brainkb_capabilities("alice@uk.org")                         # verify → includes "ingest"
  ```
  Global capability (ingest anywhere they have space write) vs per-space: to scope a
  group to ONE space instead, skip grant_role_capability and add a space write rule —
  `brainkb_add_access_rule("lab-space","write","global_role","uk_collaborator")`.

  Example prompt: *"Create a group uk_collaborator, let it ingest, and add alice@uk.org to it."*
- **Fine-grained per-space access rules** (space owner/manager): restrict an action
  within a space to a role, a member, or a space-role.
  - List: `brainkb_list_access_rules(slug)`.
  - Add: `brainkb_add_access_rule(slug, action, subject_type, subject_value)` where
    `action` ∈ read|write|manage; `subject_type` ∈ global_role|member|space_role.
    e.g. "only Admins may write here": `("write","global_role","Admin")`; "only this
    lab member may read": `("read","member","alice@lab.org")`.
  - Remove: `brainkb_remove_access_rule(slug, rule_id)`.
  - Owner and Admin/SuperAdmin always bypass rules (no lockout).

### 9. Admin: manage users, roles & activation (usermanagement service)
These act on the **usermanagement service** (a separate service with its own
token) and require the caller to hold an **Admin/SuperAdmin** role. They work when
the MCP has credentials (env auto-login, or `brainkb_login(email, password)` — an
OAuth-only session can't log into usermanagement).
- Onboarding: users self-register with `brainkb_register(...)` (see §0) or by
  **first login via Globus/ORCID/GitHub** — both auto-create the profile + a
  default `Curator` role. Password signups then need admin activation:
  `brainkb_activate_user(email)`. Admins adjust roles afterward.
- Inspect: `brainkb_list_users(q, role)` · `brainkb_available_roles()`.
- Deactivate/reactivate login access: `brainkb_deactivate_user(email)` /
  `brainkb_activate_user(email)`.
- Assign / remove a role (= permission group: Lab Member, External, custom, …):
  `brainkb_assign_role(email, role)` / `brainkb_remove_role(email, role)`
  (the user must have a profile — i.e. have signed in once).
- New group/category: `brainkb_create_role("uk_collaborator", "Community",
  "UK collaborators")` then `brainkb_assign_role(email, "uk_collaborator")`, then
  grant it KG capabilities via §8 (`brainkb_grant_role_capability`).
- **Permissions catalog**: `brainkb_list_permissions()` lists usermanagement
  permissions (resource/action, used for page-access); add new ones with
  `brainkb_create_permission(name, resource, action, description)`. (KG action
  capabilities are separate — see `brainkb_list_capabilities` in §8.)
- **SuperAdmin > Admin**: assigning/removing the `Admin` role, and banning an
  Admin, are **SuperAdmin-only**. The `SuperAdmin` role is protected (can't be
  removed/banned).
- **No deletion — ban instead**: accounts are never hard-deleted. Remove access
  with `brainkb_ban_user(email, reason)` (reversible; preserves history); lift with
  `brainkb_unban_user(email)`. `brainkb_deactivate_user` toggles login access.
- KG-specific capabilities (create team spaces, ingest, etc.) are granted with the
  query_service admin tools — see §8.

## Typical end-to-end

1. `brainkb_login(...)`
2. `brainkb_create_space("my-lab", "My Lab", "private", "My lab's working data")`
3. `brainkb_add_space_graph("my-lab", "https://brainkb.org/graph/my-lab/", "My lab cell-type annotations")`  ← always give a description
4. `brainkb_ingest_text("https://brainkb.org/graph/my-lab/", "<ttl>")` → job_id
5. poll `brainkb_job_status(job_id)` until `done`
6. `brainkb_search("<term>", space="my-lab")` / `brainkb_provenance_graph(iri)`
7. (optional) `brainkb_set_space_visibility("my-lab", "public")`

### Worked example: "Ingest my TTL into the hmba space, then show what changed."
This is the exact pattern for an **existing** space + "what changed":
1. `brainkb_whoami()` — confirm the intended identity (attribution is permanent).
2. `brainkb_list_spaces()` → find `hmba` and its registered graph IRI `G` (if it
   has none, `brainkb_add_space_graph("hmba", G, "<desc>")` first).
3. `brainkb_ingest_text(G, "<the user's TTL>")` → `job_id` (or
   `brainkb_ingest_files(G, [paths])`).
4. Poll `brainkb_job_status(job_id)` until terminal; report success/fail counts.
5. **"what changed"** → `brainkb_delta(job_id)` (exact triples this ingest added).
   For the graph's full change log, `brainkb_delta_history(G)`; for who/when,
   `brainkb_provenance_job(job_id)`.
This is transaction/ingestion-time provenance ("what was just added"), per the
two-clocks note in §6.

## Deployment smoke test (is the deploy done & healthy?)

Use this to confirm a fresh deployment is up and the auth stack (SSO + PAT +
Globus) works. Two ways: **curl** (run on the deploy host, or against the public
URLs) and **MCP tools** (from a session with the `brainkb` MCP registered). Run
the layers in order and stop at the first failure — a later layer can't pass if
an earlier one didn't.

Set the two base URLs first (defaults are the unified local stack):

```bash
BASE="${BRAINKB_URL:-http://localhost:8010}"                 # query_service
UM="${USERMANAGEMENT_URL:-http://localhost:8004}"            # usermanagement
# Deployment example:
#   BASE=https://query.brainkb.org   UM=https://usermanagement.brainkb.org
```

### Layer 1 — services reachable (no auth)

```bash
# Each should print 200. Anything else (000/connection refused) = not reachable.
curl -s -o /dev/null -w "query_service   openapi : %{http_code}\n" "$BASE/openapi.json"
curl -s -o /dev/null -w "usermanagement  jwks    : %{http_code}\n" "$UM/.well-known/jwks.json"
curl -s -o /dev/null -w "usermanagement  openapi : %{http_code}\n" "$UM/openapi.json"
# JWKS must contain a key (RS256 issuer live):
curl -s "$UM/.well-known/jwks.json" | python3 -c 'import sys,json;k=json.load(sys.stdin).get("keys",[]);print("jwks keys:",len(k),"OK" if k else "MISSING")'
```

### Layer 2 — Globus/OAuth configured + redirect correct

```bash
# Globus should show "configured": true. If false, GLOBUS_CLIENT_ID/SECRET aren't set.
curl -s "$UM/api/auth/providers" | python3 -m json.tool
```
The server builds the redirect as `${USERMANAGEMENT_PUBLIC_BASE_URL}/api/auth/globus/callback`.
Confirm `USERMANAGEMENT_PUBLIC_BASE_URL` is the **public** host (e.g.
`https://usermanagement.brainkb.org`), not `localhost` — and that this exact
callback URL is registered in the Globus app. A `localhost` value here is the
usual cause of a Globus "redirect mismatch" after deploy.

### Layer 3 — SSO login → per-service exchange (needs a password account)

```bash
# 1) login -> refresh token
REFRESH=$(curl -s -X POST "$UM/api/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"'"$EMAIL"'","password":"'"$PASSWORD"'"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("refresh_token",""))')
[ -n "$REFRESH" ] && echo "login OK" || echo "login FAILED"
# 2) exchange -> query_service access token
QTOK=$(curl -s -X POST "$UM/api/auth/exchange" -H "Authorization: Bearer $REFRESH" \
  -H 'Content-Type: application/json' -d '{"audience":"query_service"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("access_token",""))')
# 3) use it against query_service (expect 200)
curl -s -o /dev/null -w "query_service /api/spaces : %{http_code}\n" "$BASE/api/spaces" -H "Authorization: Bearer $QTOK"
```

### Layer 4 — Personal Access Token round-trip

Needs a **session token** (`$STOK`) — the usermanagement JWT for a logged-in
user. If you have a password account, mint one from the refresh token above:
`STOK=$(curl -s -X POST "$UM/api/auth/exchange" -H "Authorization: Bearer $REFRESH" -H 'Content-Type: application/json' -d '{"audience":"usermanagement"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')`

```bash
# create (default lifetime is 3 days)
CREATE=$(curl -s -X POST "$UM/api/auth/tokens" -H "Authorization: Bearer $STOK" \
  -H 'Content-Type: application/json' -d '{"name":"smoke-test","days":3}')
echo "$CREATE" | python3 -m json.tool
PAT=$(echo "$CREATE" | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')
PID=$(echo "$CREATE" | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
# exchange PAT -> query_service token, then use it (expect 200)
PQ=$(curl -s -X POST "$UM/api/auth/pat/exchange" -H 'Content-Type: application/json' \
  -d '{"token":"'"$PAT"'","audience":"query_service"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("access_token",""))')
curl -s -o /dev/null -w "PAT -> query_service : %{http_code}  (expect 200)\n" "$BASE/api/spaces" -H "Authorization: Bearer $PQ"
# revoke, then confirm the PAT no longer exchanges (expect 401)
curl -s -X DELETE "$UM/api/auth/tokens/$PID" -H "Authorization: Bearer $STOK" >/dev/null
curl -s -o /dev/null -w "PAT after revoke     : %{http_code}  (expect 401)\n" -X POST "$UM/api/auth/pat/exchange" \
  -H 'Content-Type: application/json' -d '{"token":"'"$PAT"'","audience":"query_service"}'
```

A healthy deploy prints: layer-1 all `200` + `jwks keys: N OK`; layer-2 Globus
`configured: true`; layer-3 `login OK` + `200`; layer-4 create returns a
`brainkb_pat_…` token, `PAT -> query_service : 200`, `PAT after revoke : 401`.

### Via the MCP (same checks, no curl)

From a session with the `brainkb` MCP registered (base URL pointed at the
deploy):

1. `brainkb_login(email, password)` **or** `brainkb_globus_login()` →
   `brainkb_finish_login(code)`. Then `brainkb_whoami()` → should report
   `authenticated: true` and the right `base_url`/email (proves login + SSO
   exchange).
2. `brainkb_list_spaces()` → returns without error (proves query_service auth via
   the exchanged token).
3. **PAT:** `brainkb_create_token(name="smoke-test", days=3)` → returns a
   `brainkb_pat_…` once; `brainkb_list_tokens()` → shows it `active: true`;
   `brainkb_revoke_token(<id>)` → `revoked: true`. To prove end-to-end, set that
   PAT as `BRAINKB_TOKEN` (or `brainkb_use_token("<pat>")`) and re-run
   `brainkb_whoami()` / `brainkb_list_spaces()` — they should still work with **no
   password/browser**.
4. Admin reachability (if Admin/SuperAdmin): `brainkb_list_users(limit=1)` returns
   without error (proves the `usermanagement` audience exchange too).

If step 1 errors with a connection failure, re-read **Connectivity** above — the
session can't reach the deploy (localhost from a cloud session, or stack down).

## Fallback: curl (no MCP)

Only use this when running **on the same machine/network as the deployment**
(so `localhost:8010` resolves to the real stack). From a cloud/sandbox session,
curl to `localhost` will fail — use the local MCP instead.

Base = the deployment URL (default `http://localhost:8010`).

```bash
# login (capture token into a variable — never print it)
TOKEN=$(curl -s -X POST "$BASE/api/token" -H 'Content-Type: application/json' \
  -d '{"email":"'"$EMAIL"'","password":"'"$PASSWORD"'"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

# create space + bind a graph
curl -s -X POST "$BASE/api/spaces" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"slug":"my-lab","name":"My Lab","visibility":"private"}'
curl -s -X POST "$BASE/api/spaces/my-lab/graphs" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"named_graph_url":"https://brainkb.org/graph/my-lab/","description":"lab data"}'

# ingest (URL-encode user_id and named_graph_iri)
curl -s -X POST "$BASE/api/insert/raw/knowledge-graph-triples?user_id=$EMAIL&named_graph_iri=https%3A%2F%2Fbrainkb.org%2Fgraph%2Fmy-lab%2F" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: text/plain' --data-binary @data.ttl

# job status
curl -s "$BASE/api/insert/user/jobs/detail?user_id=$EMAIL&job_id=<JOB_ID>" -H "Authorization: Bearer $TOKEN"

# search / provenance
curl -s "$BASE/api/search?q=<term>" -H "Authorization: Bearer $TOKEN"
curl -s "$BASE/api/provenance/named-graph?iri=https%3A%2F%2Fbrainkb.org%2Fgraph%2Fmy-lab%2F" -H "Authorization: Bearer $TOKEN"
```

The `user_id` query parameter must equal the logged-in user's email — the server
rejects acting on another user's behalf.

## Example SPARQL queries

These are **examples / starting points**, not an exhaustive or fixed set — adapt
them (graph IRIs, filters, terms) to the question at hand, or write your own.
Run them with the `brainkb_sparql(query)` tool (**requires an Admin/SuperAdmin
role**; non-admins use the structured tools like `brainkb_search`,
`brainkb_read_space`, `brainkb_provenance_*` instead). Replace `my-lab` / `JOB_ID`
with real values.

**Fixed graph IRIs**

| Purpose | Named graph |
|---|---|
| Graph registry (catalog) | `https://brainkb.org/metadata/named-graph` |
| Spaces manifest | `https://brainkb.org/metadata/spaces/` |
| Provenance | `https://brainkb.org/provenance/` |
| Per-job delta | `https://brainkb.org/provenance/delta/{job_id}` |
| A data graph | e.g. `https://brainkb.org/graph/my-lab/` |

Only data graphs appear in the registry; the four above are infrastructure the
backend maintains itself (`_SKIP_GRAPHS` in `indexing.py`, `PROVENANCE_DELTA_BASE`
in `provenance.py`). Registry + those four = the whole store.

**Common prefixes**

```sparql
PREFIX prov:    <http://www.w3.org/ns/prov#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX schema:  <https://schema.org/>
PREFIX brainkb: <https://brainkb.org/vocab/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
```

1) All named graphs + triple counts

```sparql
SELECT ?g (COUNT(*) AS ?triples) WHERE { GRAPH ?g { ?s ?p ?o } }
GROUP BY ?g ORDER BY DESC(?triples)
```

2) A graph's data

```sparql
SELECT ?s ?p ?o WHERE { GRAPH <https://brainkb.org/graph/my-lab/> { ?s ?p ?o } } LIMIT 200
```

3) Registry — which graphs are registered + by whom

```sparql
SELECT ?graph ?description ?registered_at ?registered_by WHERE {
  GRAPH <https://brainkb.org/metadata/named-graph> {
    ?graph dcterms:description ?description ; prov:generatedAtTime ?registered_at .
    OPTIONAL { ?graph prov:wasAttributedTo ?registered_by }
  }
}
```

4) Spaces manifest — visibility, owner, contained graphs

```sparql
SELECT ?space ?name ?visibility ?owner
       (GROUP_CONCAT(DISTINCT STR(?graph); SEPARATOR=", ") AS ?graphs) WHERE {
  GRAPH <https://brainkb.org/metadata/spaces/> {
    ?space a brainkb:Space ; schema:name ?name ;
           brainkb:visibility ?visibility ; brainkb:owner ?owner .
    OPTIONAL { ?space brainkb:containsGraph ?graph }
  }
} GROUP BY ?space ?name ?visibility ?owner
```

Space members (owner/editor/viewer):

```sparql
SELECT ?space ?role ?agent WHERE {
  GRAPH <https://brainkb.org/metadata/spaces/> {
    VALUES ?role { brainkb:owner brainkb:editor brainkb:viewer }
    ?space ?role ?agent .
  }
}
```

5) Provenance — ingestion activities (who/when/status)

```sparql
SELECT ?activity ?agent ?targetGraph ?status ?start ?end ?success ?fail WHERE {
  GRAPH <https://brainkb.org/provenance/> {
    ?activity a brainkb:IngestionActivity ;
              prov:wasAssociatedWith ?agent ;
              brainkb:targetGraph ?targetGraph ;
              brainkb:jobStatus ?status ;
              prov:startedAtTime ?start .
    OPTIONAL { ?activity prov:endedAtTime ?end }
    OPTIONAL { ?activity brainkb:successCount ?success }
    OPTIONAL { ?activity brainkb:failCount ?fail }
  }
} ORDER BY DESC(?start)
```

6) Change history + deltas for a graph

```sparql
SELECT ?delta ?deltaGraph ?added ?time WHERE {
  GRAPH <https://brainkb.org/provenance/> {
    ?delta a brainkb:IngestionDelta ;
           brainkb:targetGraph <https://brainkb.org/graph/my-lab/> ;
           brainkb:deltaGraph ?deltaGraph ;
           brainkb:addedTripleCount ?added ;
           prov:generatedAtTime ?time .
  }
} ORDER BY DESC(?time)
```

Exact triples one job added:

```sparql
SELECT ?s ?p ?o WHERE { GRAPH <https://brainkb.org/provenance/delta/JOB_ID> { ?s ?p ?o } }
```

7) Per-file results for a job

```sparql
SELECT ?name ?status ?http ?size WHERE {
  GRAPH <https://brainkb.org/provenance/> {
    ?file prov:wasGeneratedBy <https://brainkb.org/prov/activity/JOB_ID> ;
          brainkb:fileName ?name ; brainkb:uploadStatus ?status .
    OPTIONAL { ?file brainkb:httpStatus ?http }
    OPTIONAL { ?file brainkb:sizeBytes ?size }
  }
}
```

8) Find a term across graphs

```sparql
SELECT ?g ?s ?label WHERE {
  GRAPH ?g { ?s rdfs:label ?label . FILTER(CONTAINS(LCASE(STR(?label)), "purkinje")) }
}
```
