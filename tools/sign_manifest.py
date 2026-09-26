#!/usr/bin/env python3
"""
Sign and verify the skill registry (and skill directories) with Ed25519.

Ed25519 is the only supported scheme. The private key signs; verifiers only
need the pinned public key and cannot forge signatures. The public key that
verifiers pin is committed at ``keys/registry-ed25519.pub``; the matching
private key lives only in the ``SKILLS_ED25519_PRIVATE_KEY`` GitHub Actions
secret. (The former shared-secret HMAC-SHA256 scheme was removed: anyone who
could verify an HMAC signature could also forge one.)

Registry signature contract (produced by publish-registry.yml, verified by
Rho before it trusts the index):

* ``sha256`` is the lowercase hex SHA-256 digest of the exact bytes of the
  signed file.
* The signed message is the 64 ASCII bytes of that hex digest (not the raw
  32-byte digest).
* ``signature`` is the hex-encoded 64-byte Ed25519 signature.
* ``sign`` prints ``{"target", "sha256", "algorithm": "ed25519", "signature"}``
  as JSON; ``target`` is the signed file's base name (``registry.json``).

A verifier must require ``algorithm == "ed25519"``, recompute the digest of the
downloaded bytes and compare it with ``sha256``, then verify ``signature`` over
the hex digest with the pinned public key. Any failure means the registry must
not be used.

Key material may be passed via ``--key`` (literal PEM or a path to a PEM
file) or through ``SKILLS_ED25519_PRIVATE_KEY`` (sign) and
``SKILLS_ED25519_PUBLIC_KEY`` (verify). ``verify`` falls back to the committed
public key when neither is given. Requires the ``cryptography`` package.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ALGORITHM = "ed25519"
ED25519_PRIVATE_KEY_ENV = "SKILLS_ED25519_PRIVATE_KEY"
ED25519_PUBLIC_KEY_ENV = "SKILLS_ED25519_PUBLIC_KEY"
# The public key Rho pins. Committed so anyone can verify a published registry.
PINNED_PUBLIC_KEY_PATH = REPO_ROOT / "keys" / "registry-ed25519.pub"

_HEX_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


def compute_content_hash(skill_dir: Path) -> str:
    """Compute deterministic SHA256 digest of all files in a skill directory."""
    hasher = hashlib.sha256()
    for file_path in sorted(skill_dir.rglob("*")):
        if file_path.is_file() and not file_path.name.startswith("."):
            rel_path = file_path.relative_to(skill_dir).as_posix()
            hasher.update(rel_path.encode("utf-8"))
            hasher.update(file_path.read_bytes())
    return hasher.hexdigest()


def target_digest(target: Path) -> str | None:
    """Return the hex SHA-256 digest of a file's bytes or a skill directory.

    Returns None when the target does not exist.
    """
    if target.is_dir():
        return compute_content_hash(target)
    if target.is_file():
        return hashlib.sha256(target.read_bytes()).hexdigest()
    return None


def load_key_material(value: str) -> str:
    """Resolve a --key value that is either literal PEM text or a path to a PEM file."""
    if "-----BEGIN" in value:
        return value
    path = Path(value)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def generate_ed25519_keypair() -> tuple[str, str]:
    """Generate an Ed25519 keypair and return (private_pem, public_pem).

    The private PEM must be kept secret (CI secret store); the public PEM is
    safe to commit and hand to verifiers.
    """
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private_key = Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")
    return private_pem, public_pem


def sign_hash_ed25519(digest: str, private_key_pem: str) -> str:
    """Sign a hex digest (as ASCII bytes) with an Ed25519 private key; returns hex."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    key = serialization.load_pem_private_key(private_key_pem.encode("utf-8"), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError("key is not an Ed25519 private key")
    return key.sign(digest.encode("utf-8")).hex()


def verify_hash_ed25519(digest: str, signature: str, public_key_pem: str) -> bool:
    """Verify a hex-encoded Ed25519 signature for a digest against a public key."""
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    try:
        key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
        if not isinstance(key, Ed25519PublicKey):
            return False
        key.verify(bytes.fromhex(signature), digest.encode("utf-8"))
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def build_signature_document(target: Path, digest: str, signature: str) -> dict[str, str]:
    """Return the signature document published next to the signed target."""
    return {
        "target": target.resolve().name,
        "sha256": digest,
        "algorithm": ALGORITHM,
        "signature": signature,
    }


def verify_signature_document(target: Path, document: object, public_key_pem: str) -> list[str]:
    """Check a signature document against the target bytes and a public key.

    Implements the verifier side of the registry signature contract. Returns
    a list of human-readable problems; an empty list means the signature is
    valid for exactly these bytes.
    """
    if not isinstance(document, dict):
        return ["signature document must be a JSON object"]
    problems: list[str] = []
    algorithm = document.get("algorithm")
    if algorithm != ALGORITHM:
        problems.append(f"algorithm must be {ALGORITHM!r}, got {algorithm!r}")
    expected_target = target.resolve().name
    if document.get("target") != expected_target:
        problems.append(
            f"target must be {expected_target!r}, got {document.get('target')!r}"
        )
    claimed = document.get("sha256")
    if not isinstance(claimed, str) or not _HEX_DIGEST_RE.match(claimed):
        problems.append("sha256 must be a lowercase 64-character hex digest")
        claimed = None
    actual = target_digest(target)
    if actual is None:
        problems.append(f"{target} does not exist")
    elif claimed is not None and claimed != actual:
        problems.append(f"sha256 mismatch: document says {claimed}, file hashes to {actual}")
    signature = document.get("signature")
    if not isinstance(signature, str) or not signature:
        problems.append("signature must be a non-empty hex string")
    elif actual is not None and not verify_hash_ed25519(actual, signature, public_key_pem):
        problems.append("Ed25519 signature does not verify with the given public key")
    return problems


def write_ed25519_keypair(private_out: Path | None, public_out: Path | None) -> tuple[str, str]:
    """Generate an Ed25519 keypair and optionally write the PEMs to files.

    The private key file is chmod 0600 when written; the public key file is
    safe to commit or pin for verifiers.
    """
    private_pem, public_pem = generate_ed25519_keypair()
    if private_out is not None:
        private_out.write_text(private_pem, encoding="utf-8")
        with contextlib.suppress(OSError):
            private_out.chmod(0o600)
    if public_out is not None:
        public_out.write_text(public_pem, encoding="utf-8")
    return private_pem, public_pem


def resolve_key(cli_value: str | None, env_name: str, purpose: str) -> str:
    """Fall back to an environment variable when --key is omitted."""
    value = cli_value or os.environ.get(env_name)
    if not value:
        print(f"Error: no key provided for {purpose}; pass --key or set {env_name}", file=sys.stderr)
        sys.exit(2)
    return value


def resolve_public_key(cli_value: str | None) -> str:
    """Return the verification key: --key, then the env var, then the pinned key."""
    value = cli_value or os.environ.get(ED25519_PUBLIC_KEY_ENV)
    if value:
        return load_key_material(value)
    try:
        return PINNED_PUBLIC_KEY_PATH.read_text(encoding="utf-8")
    except OSError:
        print(
            f"Error: no key provided for Ed25519 verification; pass --key, set "
            f"{ED25519_PUBLIC_KEY_ENV}, or restore {PINNED_PUBLIC_KEY_PATH.name}",
            file=sys.stderr,
        )
        sys.exit(2)


def _require_digest(target: Path) -> str:
    digest = target_digest(target)
    if digest is None:
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)
    return digest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sign or verify GrayCode Skills registry manifests with Ed25519."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    keygen_parser = subparsers.add_parser("keygen", help="Generate an Ed25519 signing keypair.")
    keygen_parser.add_argument(
        "--private-out", type=Path, default=None,
        help="Optional path to write the private key PEM to (must be kept secret).")
    keygen_parser.add_argument(
        "--public-out", type=Path, default=None,
        help="Optional path to write the public key PEM to (safe to commit/pin).")

    sign_parser = subparsers.add_parser("sign", help="Sign a skill directory or manifest.")
    sign_parser.add_argument("target", type=Path, help="Path to skill directory or registry.json")
    sign_parser.add_argument(
        "--key", default=None,
        help=f"Ed25519 private key PEM or PEM file path (default: ${ED25519_PRIVATE_KEY_ENV})")
    sign_parser.add_argument(
        "--ed25519", action="store_true",
        help="Accepted for compatibility; Ed25519 is the only scheme.")

    verify_parser = subparsers.add_parser("verify", help="Verify a signed skill package or manifest.")
    verify_parser.add_argument("target", type=Path, help="Path to skill directory or registry.json")
    source = verify_parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--signature", help="Expected hex signature over the target's digest")
    source.add_argument(
        "--signature-file", type=Path,
        help="Signature JSON printed by 'sign'; also checks algorithm, target and sha256")
    verify_parser.add_argument(
        "--key", default=None,
        help=(f"Ed25519 public key PEM or PEM file path (default: ${ED25519_PUBLIC_KEY_ENV}, "
              "then keys/registry-ed25519.pub)"))
    verify_parser.add_argument(
        "--ed25519", action="store_true",
        help="Accepted for compatibility; Ed25519 is the only scheme.")

    args = parser.parse_args()

    if args.command == "keygen":
        private_pem, public_pem = write_ed25519_keypair(args.private_out, args.public_out)
        print(json.dumps({"algorithm": ALGORITHM, "private_key": private_pem, "public_key": public_pem}, indent=2))
        print(
            f"Keep the private key in CI secrets ({ED25519_PRIVATE_KEY_ENV}); "
            "pin the public key for verifiers. Never commit the private key.",
            file=sys.stderr,
        )

    elif args.command == "sign":
        digest = _require_digest(args.target)
        key = load_key_material(resolve_key(args.key, ED25519_PRIVATE_KEY_ENV, "Ed25519 signing"))
        try:
            sig = sign_hash_ed25519(digest, key)
        except (ValueError, TypeError) as exc:
            print(f"Error: invalid Ed25519 private key: {exc}", file=sys.stderr)
            sys.exit(2)
        print(json.dumps(build_signature_document(args.target, digest, sig), indent=2))

    elif args.command == "verify":
        public_key = resolve_public_key(args.key)
        if args.signature_file is not None:
            try:
                document = json.loads(args.signature_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                print(f"FAIL: cannot read {args.signature_file}: {exc}", file=sys.stderr)
                sys.exit(1)
            problems = verify_signature_document(args.target, document, public_key)
        else:
            digest = _require_digest(args.target)
            problems = [] if verify_hash_ed25519(digest, args.signature, public_key) else [
                "Ed25519 signature does not verify with the given public key"
            ]
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}", file=sys.stderr)
            sys.exit(1)
        print("OK: Signature verified successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
