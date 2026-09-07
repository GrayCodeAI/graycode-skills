---
name: registrar-dns-management
description: "List, add, update, and delete DNS records at a domain registrar via its XML API, including subdomain linking."
license: MIT
tags:
- dns
- networking
---

# Namecheap DNS

Manage DNS records at Namecheap via the XML API. The API has two
quirks that bite first-time users:

1. **IP allowlist required** — every request must come from an IP
   pre-whitelisted at Namecheap → Profile → Tools → Namecheap API
   Access → Whitelisted IPs. **Sandbox IPs change between
   sessions; always confirm with `curl -s https://api.ipify.org`
   first.** If you get error `1011150 Invalid request IP: <ip>`, ask
   the user to add that IP to the whitelist.
2. **Updates are wholesale** — there is no "add one record" endpoint.
   `setHosts` REPLACES every record on the domain. You must `getHosts`
   first, then resend ALL existing records plus your new one.

## Required environment

| Env var | What it is |
|---|---|
| `NAMECHEAP_API_KEY` | API key from Namecheap → Profile → Tools → API Access |
| `NAMECHEAP_API_USER` | Namecheap account username — used as both `ApiUser` and `UserName` |

Optional: `NAMECHEAP_CLIENT_IP` (defaults to `curl -s https://api.ipify.org`), `NAMECHEAP_EMAIL_TYPE` (`FWD` or `MX`), `NAMECHEAP_API_BASE`.

## Endpoint

Production: `https://api.namecheap.com/xml.response`
Sandbox: `https://api.sandbox.namecheap.com/xml.response` (separate
account; usually you want production)

## List records

```bash
MY_IP=$(curl -s https://api.ipify.org)
curl -s -G "https://api.namecheap.com/xml.response" \
  --data-urlencode "ApiUser=$NAMECHEAP_API_USER" \
  --data-urlencode "ApiKey=$NAMECHEAP_API_KEY" \
  --data-urlencode "UserName=$NAMECHEAP_API_USER" \
  --data-urlencode "ClientIp=$MY_IP" \
  --data-urlencode "Command=namecheap.domains.dns.getHosts" \
  --data-urlencode "SLD=your-app" \
  --data-urlencode "TLD=ai"
```

Parse the XML response — each record looks like:

```xml
<host HostId="498699225" Name="www" Type="CNAME"
      Address="your-app.fly.dev." MXPref="10" TTL="300"
      IsActive="true" />
```

Quick parse with grep:

```bash
echo "$RESP" | grep -oE 'Name="[^"]+" Type="[^"]+" Address="[^"]+"'
```

## Add or update records (setHosts replaces all)

**You MUST include every existing record you want to keep, plus the
new one.** Forgetting any record will silently delete it.

```bash
MY_IP=$(curl -s https://api.ipify.org)

curl -s -G "https://api.namecheap.com/xml.response" \
  --data-urlencode "ApiUser=$NAMECHEAP_API_USER" \
  --data-urlencode "ApiKey=$NAMECHEAP_API_KEY" \
  --data-urlencode "UserName=$NAMECHEAP_API_USER" \
  --data-urlencode "ClientIp=$MY_IP" \
  --data-urlencode "Command=namecheap.domains.dns.setHosts" \
  --data-urlencode "SLD=your-app" \
  --data-urlencode "TLD=ai" \
  --data-urlencode "EmailType=FWD" \
  \
  `# existing record 1 (apex A)` \
  --data-urlencode "HostName1=@" \
  --data-urlencode "RecordType1=A" \
  --data-urlencode "Address1=66.241.124.148" \
  --data-urlencode "TTL1=300" \
  \
  `# existing record 2 (apex AAAA)` \
  --data-urlencode "HostName2=@" \
  --data-urlencode "RecordType2=AAAA" \
  --data-urlencode "Address2=2a09:8280:1::e7:30bb:1" \
  --data-urlencode "TTL2=300" \
  \
  `# NEW record: docs.example.com → Fly` \
  --data-urlencode "HostName5=docs" \
  --data-urlencode "RecordType5=CNAME" \
  --data-urlencode "Address5=131zmog.your-docs-app.fly.dev." \
  --data-urlencode "TTL5=300"
```

**Success response** contains `Status="OK"` and `IsSuccess="true"`.

## Standard linking pattern: subdomain → Fly app

```bash
# 1. On Fly: create cert (issues challenge + provisions LB hostname)
fly certs add subdomain.example.com -a my-app

# 2. Get the recommended CNAME target from Fly
fly certs setup subdomain.example.com -a my-app
# → CNAME subdomain.example.com → <hash>.my-app.fly.dev

# 3. Add CNAME at Namecheap (use setHosts pattern above)

# 4. Wait for DNS propagation (60-120s usually)
# Sandbox local DNS is slow; verify via Cloudflare DoH:
curl -s "https://1.1.1.1/dns-query?name=subdomain.example.com&type=CNAME" \
  -H "accept: application/dns-json"

# 5. Verify cert issued
fly certs check subdomain.example.com -a my-app
# → "Status = Issued" + "Certificate is verified and active"

# 6. Test (sandbox DNS may lag; use --resolve to force):
APP_IP=$(curl -s -G "https://1.1.1.1/dns-query?name=my-app.fly.dev&type=A" \
  -H "accept: application/dns-json" | python3 -c "import sys,json; print(json.load(sys.stdin)['Answer'][0]['data'])")
curl -sI --resolve subdomain.example.com:443:$APP_IP \
  https://subdomain.example.com/
```

## Common errors

| Error code | Meaning | Fix |
|---|---|---|
| `1011150` Invalid request IP | Sandbox IP not whitelisted | Get IP via `curl https://api.ipify.org`, ask user to whitelist at Namecheap → Profile → Tools → API |
| `1011102` API Key invalid / API access not enabled | Wrong key, or production/sandbox endpoint mismatch | Check `NAMECHEAP_API_KEY` env var, use `api.namecheap.com` (NOT sandbox) |
| Records silently deleted | Forgot to resend in setHosts | Always `getHosts` first; build full record list including additions |
| MX records on subdomain silently dropped | `EmailType=FWD` blocks subdomain MX | Use `EmailType=MX` and resend all apex MX records explicitly (eforward1-5) |
| Long DKIM TXT record dropped | Sometimes works on retry | Resend the same setHosts call once or twice — Namecheap occasionally rejects long TXT silently and accepts it on retry |

## Resend domain setup pattern

Resend gives you 3 records to add:
- `resend._domainkey` TXT (DKIM)
- `send` MX → feedback-smtp.us-east-1.amazonses.com
- `send` TXT (SPF)

**Critical**: must use `EmailType=MX`, not `FWD`. If domain currently uses
Namecheap email forwarding, include eforward1-5 MX records explicitly:

```
HostName=@  Type=MX  Address=eforward1.registrar-servers.com.  MXPref=10
HostName=@  Type=MX  Address=eforward2.registrar-servers.com.  MXPref=10
HostName=@  Type=MX  Address=eforward3.registrar-servers.com.  MXPref=10
HostName=@  Type=MX  Address=eforward4.registrar-servers.com.  MXPref=15
HostName=@  Type=MX  Address=eforward5.registrar-servers.com.  MXPref=20
HostName=@  Type=TXT Address="v=spf1 include:spf.efwd.registrar-servers.com ~all"
```

## Scripts

```bash
# List records (XML or JSON)
scripts/getHosts.sh example com
scripts/getHosts.sh example com --json

# Replace ALL hosts with the JSON array on stdin (wholesale setHosts)
scripts/getHosts.sh example com --json > /tmp/hosts.json
# edit /tmp/hosts.json, then:
cat /tmp/hosts.json | scripts/setHosts.sh example com
```

`setHosts` **replaces every record** — always start from `getHosts --json` and merge your changes into the full list.
