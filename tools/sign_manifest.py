#!/usr/bin/env python3
"""
Sign and verify community skill packages and registry manifests.

Two signature schemes are supported:

* HMAC-SHA256 (default, legacy): a symmetric shared-secret signature over the
  SHA-256 digest of a skill directory or manifest file. Anyone who holds the
  shared secret can forge signatures, so this scheme only proves possession
  of the secret, not per-origin provenance.
* Ed25519 (``--ed25519``): an asymmetric signature over the same digest. The
  private key signs; verifiers only need the pinned public key and cannot
  forge signatures. Generate a keypair with the ``keygen`` subcommand, keep
  the private key in CI secrets, and commit or otherwise pin the public key
  for verifiers.

Key material may be passed via ``--key`` (literal PEM for Ed25519, secret
string for HMAC, or a path to a PEM file for Ed25519) or through the
``SKILLS_SIGNING_KEY`` (HMAC), ``SKILLS_ED25519_PRIVATE_KEY`` (Ed25519 sign)
and ``SKILLS_ED25519_PUBLIC_KEY`` (Ed25519 verify) environment variables.

Ed25519 requires the optional ``cryptography`` package; the legacy HMAC path
uses only the standard library.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

HMAC_KEY_ENV = "SKILLS_SIGNING_KEY"
ED25519_PRIVATE_KEY_ENV = "SKILLS_ED25519_PRIVATE_KEY"
ED25519_PUBLIC_KEY_ENV = "SKILLS_ED25519_PUBLIC_KEY"

def compute_content_hash(skill_dir: Path) -> str:
    """Compute deterministic SHA256 digest of all files in a skill directory."""
    hasher = hashlib.sha256()
    for file_path in sorted(skill_dir.rglob("*")):
        if file_path.is_file() and not file_path.name.startswith("."):
            rel_path = file_path.relative_to(skill_dir).as_posix()
            hasher.update(rel_path.encode("utf-8"))
            hasher.update(file_path.read_bytes())
    return hasher.hexdigest()

def sign_hash(digest: str, secret: str) -> str:
    """Sign a SHA256 digest with a secret key using HMAC-SHA256."""
    return hmac.new(secret.encode("utf-8"), digest.encode("utf-8"), hashlib.sha256).hexdigest()

def verify_hash(digest: str, signature: str, secret: str) -> bool:
    """Verify an HMAC-SHA256 signature for a given digest."""
    expected = sign_hash(digest, secret)
    return hmac.compare_digest(expected, signature)

def load_key_material(value: str) -> str:
    """Resolve a --key value that is either literal PEM/key text or a path to a file."""
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
    """Sign a SHA256 digest with an Ed25519 private key; returns hex-encoded signature."""
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

def main() -> None:
    parser = argparse.ArgumentParser(description="Sign or verify Hawk community skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Keygen command
    keygen_parser = subparsers.add_parser("keygen", help="Generate an Ed25519 signing keypair.")
    keygen_parser.add_argument(
        "--private-out", type=Path, default=None,
        help="Optional path to write the private key PEM to (must be kept secret).")
    keygen_parser.add_argument(
        "--public-out", type=Path, default=None,
        help="Optional path to write the public key PEM to (safe to commit/pin).")

    # Sign command
    sign_parser = subparsers.add_parser("sign", help="Sign a skill directory or manifest.")
    sign_parser.add_argument("target", type=Path, help="Path to skill directory or registry.json")
    sign_parser.add_argument("--key", default=None, help="HMAC secret or Ed25519 private key PEM (or PEM file path)")
    sign_parser.add_argument(
        "--ed25519", action="store_true",
        help="Sign with Ed25519 instead of legacy HMAC-SHA256 (requires the cryptography package).")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify a signed skill package or manifest.")
    verify_parser.add_argument("target", type=Path, help="Path to skill directory or registry.json")
    verify_parser.add_argument("--signature", required=True, help="Expected signature")
    verify_parser.add_argument("--key", default=None, help="HMAC secret or Ed25519 public key PEM (or PEM file path)")
    verify_parser.add_argument(
        "--ed25519", action="store_true",
        help="Verify an Ed25519 signature instead of legacy HMAC-SHA256 (requires the cryptography package).")

    args = parser.parse_args()

    if args.command == "keygen":
        private_pem, public_pem = write_ed25519_keypair(args.private_out, args.public_out)
        print(json.dumps({"algorithm": "ed25519", "private_key": private_pem, "public_key": public_pem}, indent=2))
        print(
            "Keep the private key in CI secrets (SKILLS_ED25519_PRIVATE_KEY); "
            "pin the public key for verifiers. Never commit the private key.",
            file=sys.stderr,
        )

    elif args.command == "sign":
        if args.target.is_dir():
            digest = compute_content_hash(args.target)
        elif args.target.is_file():
            digest = hashlib.sha256(args.target.read_bytes()).hexdigest()
        else:
            print(f"Error: {args.target} does not exist", file=sys.stderr)
            sys.exit(1)

        if args.ed25519:
            key = load_key_material(
                resolve_key(args.key, ED25519_PRIVATE_KEY_ENV, "Ed25519 signing"))
            sig = sign_hash_ed25519(digest, key)
            algorithm = "ed25519"
        else:
            key = resolve_key(args.key, HMAC_KEY_ENV, "HMAC signing")
            sig = sign_hash(digest, key)
            algorithm = "hmac-sha256"
        print(json.dumps({"target": str(args.target), "sha256": digest, "algorithm": algorithm, "signature": sig}, indent=2))

    elif args.command == "verify":
        if args.target.is_dir():
            digest = compute_content_hash(args.target)
        elif args.target.is_file():
            digest = hashlib.sha256(args.target.read_bytes()).hexdigest()
        else:
            print(f"Error: {args.target} does not exist", file=sys.stderr)
            sys.exit(1)

        if args.ed25519:
            key = load_key_material(
                resolve_key(args.key, ED25519_PUBLIC_KEY_ENV, "Ed25519 verification"))
            valid = verify_hash_ed25519(digest, args.signature, key)
        else:
            key = resolve_key(args.key, HMAC_KEY_ENV, "HMAC verification")
            valid = verify_hash(digest, args.signature, key)
        if valid:
            print("OK: Signature verified successfully.")
            sys.exit(0)
        else:
            print("FAIL: Signature mismatch!", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
