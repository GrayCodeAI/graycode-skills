# Skill Registry

`registry.json` is a **generated artifact**. It is not committed to git; the
source of truth is the `SKILL.md` files under `categories/`.

## Generate locally

```bash
python tools/update_registry.py
```

## Published registry

On every push to `main` that touches `categories/`, `tools/`, `keys/`,
`manifest-schema.toml` or the workflow itself,
[`publish-registry.yml`](../.github/workflows/publish-registry.yml) validates the
corpus, regenerates `registry.json`, signs it, verifies the signature, and
uploads both files to the rolling GitHub release `registry-latest`:

- `https://github.com/GrayCodeAI/graycode-skills/releases/download/registry-latest/registry.json`
- `https://github.com/GrayCodeAI/graycode-skills/releases/download/registry-latest/registry-signature.json`

This is the index Rho reads for `rho skills search`, `info` and `trending`. There
is no CDN; the GitHub release is the distribution point. Each run also keeps
both files as a 90-day Actions artifact (`skill-registry`) for forensics.

## Signature

The registry is signed with **Ed25519 only**. The public key is committed at
[`keys/registry-ed25519.pub`](../keys/registry-ed25519.pub) and pinned by Rho:

```
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAr9I2NG1Sih9Mu04/eOA8FmJhczSLBYiXeLAl1rqusQU=
-----END PUBLIC KEY-----
```

The private key exists only as the `SKILLS_ED25519_PRIVATE_KEY` GitHub Actions
secret. If that secret is unset the publish job fails; it never falls back to
another scheme or an unsigned upload.

`registry-signature.json` is the JSON printed by
`python tools/sign_manifest.py sign registry.json --ed25519`:

```json
{
  "target": "registry.json",
  "sha256": "<lowercase hex SHA-256 of the exact registry.json bytes>",
  "algorithm": "ed25519",
  "signature": "<hex Ed25519 signature>"
}
```

The signed message is the 64 ASCII bytes of the lowercase hex digest, not the
raw 32-byte digest.

### Verifying

A client must:

1. download both files;
2. require `algorithm == "ed25519"`;
3. recompute the SHA-256 of the downloaded `registry.json` bytes and require it
   to equal `sha256`;
4. verify `signature` over the hex digest with the pinned public key;
5. refuse to use the index if any step fails (no unsigned fallback).

With this repository checked out:

```bash
python tools/sign_manifest.py verify registry.json \
  --signature-file registry-signature.json
```

`verify` uses `keys/registry-ed25519.pub` unless `--key` or
`SKILLS_ED25519_PUBLIC_KEY` is given. With OpenSSL 3 only:

```bash
jq -r .signature registry-signature.json | xxd -r -p > registry.sig
printf '%s' "$(shasum -a 256 registry.json | cut -c1-64)" > registry.sha256
openssl pkeyutl -verify -pubin -inkey keys/registry-ed25519.pub \
  -rawin -in registry.sha256 -sigfile registry.sig
```

The publish workflow runs the same `verify` against the committed key before
it uploads anything.

### Rotating the key

1. `python tools/sign_manifest.py keygen --private-out <secure path> --public-out keys/registry-ed25519.pub`
2. Store the private PEM as the `SKILLS_ED25519_PRIVATE_KEY` secret; never commit it.
3. Update the expected key in `tests/test_sign_manifest.py` and ship the new
   pinned key in a Rho release before, or together with, the first registry
   signed by the new key. Old clients reject registries signed by a key they
   do not pin.

## Why not in git?

At about 6 MB, committing `registry.json` would add diff noise and slow clones.
