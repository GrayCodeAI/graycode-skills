# Skill Registry

`registry.json` is a **generated artifact** — it is NOT committed to git.

## Generate locally

```bash
python tools/update_registry.py
```

## In CI

The registry is generated fresh in CI before publishing to the CDN. It is not stored in the repository.

## Why not in git?

At 4+ MB, committing `registry.json` creates excessive diff noise and slows clones. The source of truth is the individual `SKILL.md` files under `categories/`.
