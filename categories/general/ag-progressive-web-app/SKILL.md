---
name: ag-progressive-web-app
description: Build Progressive Web Apps (PWAs) with offline support, installability,
  and caching strategies. Trigger whenever the user mentions PWA, service workers,
  web app manifests, Workbox, 'add to home scr...
license: MIT
tags:
- pwa
- web-dev
- service-worker
- frontend
- offline
risk: safe
source: community
date_added: 2026-03-17
tools:
- gemini
- cursor
- claude
---

## Checklist Before Shipping

- [ ] Site is served over HTTPS
- [ ] `manifest.json` has `name`, `short_name`, `start_url`, `display`, `icons` (192 + 512)
- [ ] Icons have `purpose: "any maskable"`
- [ ] `sw.js` registers without errors in DevTools → Application → Service Workers
- [ ] App shell loads from cache when network is throttled to "Offline" in DevTools
- [ ] `offline.html` fallback is cached and served when navigation fails offline
- [ ] Lighthouse PWA audit passes (Chrome DevTools → Lighthouse tab)
- [ ] Tested on iOS Safari (manual install flow) and Android Chrome (install prompt)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
