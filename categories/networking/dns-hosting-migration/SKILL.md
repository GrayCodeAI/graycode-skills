---
name: dns-hosting-migration
description: "Migrate DNS hosting to Cloudflare, import records, flip nameservers, and manage DNS records via API with rollback."
license: MIT
tags:
- dns
- networking
- migration
---

# Cloudflare DNS Migration & Management

End-to-end automation for moving domains from Namecheap to Cloudflare,
plus ongoing record management. Designed to be reusable across many domains.

## Required environment

Cloudflare auth needs **two** credentials:

| Var | What it is | When used |
|---|---|---|
| `CLOUDFLARE_API_KEY` | Account-scoped API Token (`cfat_*`) | All ongoing DNS operations: list/add/edit/delete records, zone settings, listing zones. **Use this by default.** |
| `CLOUDFLARE_GLOBAL_API_KEY` + `CLOUDFLARE_EMAIL` | Global API Key + email | **Only** for `POST /zones` (creating new zones in the account). Cloudflare's API requires User-level auth for zone creation; account tokens cannot do this. |

🔴 **Security note.** `CLOUDFLARE_GLOBAL_API_KEY` grants full account access
(billing, members, everything). Treat it carefully:
- Use Bearer auth (`Authorization: Bearer ...`) for `CLOUDFLARE_API_KEY`
- Use header-pair auth (`X-Auth-Key:` + `X-Auth-Email:`) for the global key
- **Never write either to disk, configs, URLs, or git**
- Always pass via env var; never log values

For the registrar side (Namecheap), see the `namecheap-dns` skill —
it shares its IP-allowlist + setHosts conventions with this one.

## The hard rule: zone creation needs Global Key

Account API Tokens (the safer, narrower kind) **cannot create zones**.
Cloudflare's `POST /zones` endpoint always rejects them with:

```
Requires permission "com.cloudflare.api.account.zone.create"
```

This is a Cloudflare API limitation, not a missing permission.
Solution: use the Global API Key for the single zone-create call,
then switch back to the account token for everything else.

The migration scripts handle this split automatically.

## Endpoints reference

| Operation | Method | URL | Auth |
|---|---|---|---|
| Verify token | GET | `/user/tokens/verify` (Bearer) or `/accounts/{id}/tokens/verify` | account token |
| List accounts | GET | `/accounts` | global key |
| List zones | GET | `/zones?name=domain.com` | account token |
| Create zone | POST | `/zones` body `{name, account:{id}, type:"full"}` | **global key only** |
| Delete zone | DELETE | `/zones/{zone_id}` | account token |
| List records | GET | `/zones/{zone_id}/dns_records?per_page=100` | account token |
| Create record | POST | `/zones/{zone_id}/dns_records` | account token |
| Update record | PUT | `/zones/{zone_id}/dns_records/{id}` | account token |
| Delete record | DELETE | `/zones/{zone_id}/dns_records/{id}` | account token |

## Record body shape

```json
{
  "type": "A | AAAA | CNAME | MX | TXT | CAA | SRV | NS",
  "name": "subdomain.example.com",   // FQDN, NOT just "subdomain"
  "content": "1.2.3.4",              // for MX/SRV use specific shapes
  "ttl": 300,                        // 1 = "auto" (300s)
  "proxied": false,                   // grey cloud (DNS only) by default
  "priority": 10,                    // MX records only
  "comment": "..."                   // optional, helpful for audit
}
```

Cloudflare auto-strips the trailing dot on CNAME/MX targets, but be
consistent — pass `your-app.fly.dev.` (with dot) the same way
the registrar stored it.

## Proxy default: OFF (grey cloud)

Set `proxied: false` for everything by default. Reasons:
- WebSockets / SSE often break with default proxy settings
- Fly.io, Vercel, Netlify already terminate TLS — proxying adds
  cert-renewal complications (`_acme-challenge` flow)
- Easier rollback if something is wrong

Enable per-record manually after migration is verified (`/zones/{id}/dns_records/{id}` PATCH `{proxied: true}`).

## Workflow: full migration (Namecheap → Cloudflare)

```
1. Audit current DNS at Namecheap        → scripts/audit.sh <domain>
2. Create zone in Cloudflare              → scripts/migrate.sh <domain> create
3. Import all records to Cloudflare       → scripts/migrate.sh <domain> import
4. Verify resolution via DoH against
   Cloudflare's NS (BEFORE flipping)      → scripts/migrate.sh <domain> verify
5. Flip nameservers at Namecheap          → scripts/migrate.sh <domain> flip
6. Watch propagation                      → scripts/migrate.sh <domain> watch
```

Pause for confirmation between steps 3 and 5 — the flip is the only
step that affects live traffic.

## Verifying against Cloudflare's NS BEFORE flipping

Cloudflare's nameservers serve the new zone immediately, even though
public DNS still points to Namecheap. Query CF's NS directly to
confirm records are correct:

```bash
# DoH query AGAINST Cloudflare's authoritative NS:
NS=emerson.ns.cloudflare.com  # one of the assigned NS for this zone
NS_IP=$(curl -s "https://1.1.1.1/dns-query?name=$NS&type=A" \
  -H "accept: application/dns-json" | python3 -c "import json,sys; print(json.load(sys.stdin)['Answer'][0]['data'])")

# Direct UDP DNS via dig — but sandbox lacks dig. Use a public DoT/DoH proxy
# OR run kdig if available, OR use python:
python3 -c "
import socket, struct
# (truncated — see scripts/dns-direct-query.py for full impl)
"
```

In practice the `migrate.sh verify` step uses a Python helper that
sends a UDP DNS query directly to the Cloudflare NS IP and parses
the response, so we know the zone is right BEFORE switching.

## Per-domain state

Each migration writes state to `.dns-state/<domain>/`:

```
.dns-state/example.com/
├── audit-pre.json           # records before migration
├── cloudflare-zone.json     # zone metadata + NS
├── records-imported.json    # what was sent to Cloudflare
├── verify.log               # NS-direct query results
├── flip.log                 # registrar response when flipping NS
├── post-cutover.json        # records after migration
└── report.md                # human-readable summary
```

This lets us re-run any step idempotently and roll back precisely.

## Rollback

```bash
scripts/rollback.sh <domain>
```

Sets nameservers back to the pre-migration values (saved in
`audit-pre.json`). The Cloudflare zone is left intact — re-running
`migrate.sh <domain> flip` will redo the cutover without re-importing.

## Common gotchas

| Symptom | Cause | Fix |
|---|---|---|
| `POST /zones` returns code 0 "Requires permission ..." | Used account token instead of global key | Use `CLOUDFLARE_GLOBAL_API_KEY` + `CLOUDFLARE_EMAIL` headers |
| `_acme-challenge` records dropped after migration | Forgot to import them | Always include `_acme-challenge*` CNAMEs — Fly/Vercel/etc need them for cert renewal |
| Email stops working after cutover | Namecheap `EmailType=FWD` auto-injected MX/SPF that aren't stored as host records | Before migration, manually add the eforward MX (10/10/10/15/20 priority) + SPF TXT to Cloudflare |
| Cert renewal fails 30 days post-migration | Same as above (`_acme-challenge` issue) | Verify all `_acme-challenge.*` records are in Cloudflare via `audit.sh` |
| `proxied: true` breaks the site | Cloudflare SSL mode default is "Flexible" | Set zone SSL to "Full (strict)" before enabling proxy, or leave proxy off |
| Namecheap setHosts deletes records | Wholesale replace — must include all records | Use the namecheap-dns skill's `setHosts` pattern |
| Sandbox IP not whitelisted at Namecheap | IP rotates between sandbox sessions | `curl https://api.ipify.org`; ask user to whitelist |
| `harden.sh` reports 4 CAAs added but only 1 (the last) actually persists | `cf_upsert_record` matched on `(type, name)` only. CAA records share that key but differ by `(tag, value)`, so each new CAA UPDATED the previous one instead of inserting alongside. Same bug existed for MX (5 eforward MXes on apex collapse to 1) and TXT (multiple SPF/DKIM/verification TXTs on same name collapse). | Fixed in `lib.sh:cf_upsert_record` — now matches `(type, name, tag, value)` for CAA, `(type, name, content)` for MX/TXT. **Always verify post-hardening:** `cf_api GET "/zones/$ZID/dns_records?type=CAA"` should return 4 records (`issue letsencrypt.org`, `issue pki.goog`, `issuewild ;`, `iodef mailto:…`). |
| Public resolvers (1.1.1.1, 8.8.8.8) keep returning Namecheap NS for 30+ min after the flip — even though the parent TLD is delegating to Cloudflare | "Lame delegation" during a registrar transition: Namecheap's `dns1/dns2.registrar-servers.com` keep claiming `aa=1` (authoritative) and serve in-zone NS records with their own 30min TTL. When a resolver queries Namecheap directly (instead of re-asking the parent), it caches the stale answer until the in-zone TTL expires. | This is expected and harmless — the parent .ai/.com TLD is the source of truth. **Verify the parent directly** using `dns-direct-query.py v0n0.nic.ai example.com NS` (or the equivalent TLD NS for other zones). If the parent says Cloudflare and the CF zone status is `active`, you're done. Public resolvers will catch up within 30-60 min. The site works either way because both NS sets resolve to the same origin records. |

## File: scripts/migrate.sh

The main migration driver. Takes a domain + step, runs that step,
saves state to `.dns-state/<domain>/`. Designed for re-runs.

```bash
scripts/migrate.sh example.com full       # create+import+verify, then STOPS and prints
                                          # the flip/watch commands (flip touches live
                                          # traffic, so it is never run implicitly)
scripts/migrate.sh example.com create     # create zone only
scripts/migrate.sh example.com import     # import records only
scripts/migrate.sh example.com verify     # query CF's NS to confirm
scripts/migrate.sh example.com flip       # update NS at Namecheap
scripts/migrate.sh example.com watch      # poll propagation
```

## File: scripts/audit.sh

Read-only state check — current registrar, current NS, current records,
whether zone exists in Cloudflare yet, what's missing. Safe to run anytime.

```bash
scripts/audit.sh example.com
```

## File: scripts/rollback.sh

Sets nameservers at Namecheap back to `dns1/2.registrar-servers.com`
(or the original NS saved in `audit-pre.json`).

```bash
scripts/rollback.sh example.com
```


## Progressive disclosure — load only when needed

Keep this `SKILL.md` for auth, migration workflow, endpoints, and gotchas.
Deep script docs live under `references/`:

| When you need… | Read |
|---|---|
| Zone hardening (SSL/WAF/CAA/DNSSEC tiers) | `references/harden.md` |
| DNSSEC DS paste at registrar | run `scripts/dnssec-instructions.sh <domain>`; background in `references/harden.md` |
| Cloudflare Origin CA certs | `references/origin-ca.md` |
| Export zone as YAML/JSON/TF | `references/dns-export.md` |
| Restrict Fly origin to Cloudflare only | `references/fly-restrict-origin.md` (also under `scripts/`) |
| Shared shell helpers | `scripts/lib.sh` |

Run the scripts from `scripts/`; the reference files are the human/agent deep-dive for each.

## Script index (quick)

```bash
scripts/audit.sh <domain>
scripts/migrate.sh <domain> full|create|import|verify|flip|watch
scripts/rollback.sh <domain>
scripts/harden.sh <domain> [--enable-proxy=false] [...]
scripts/dnssec-instructions.sh <domain>
scripts/origin-ca.sh <domain>
scripts/dns-export.sh <domain> [--format=yaml|json|zonefile|terraform]
scripts/cf-ips-fetch.sh
scripts/dns-direct-query.py   # UDP query against a specific NS IP
```

