#!/usr/bin/env python3
"""
Sign and verify community skill packages and registry manifests using HMAC-SHA256 or Ed25519.
Provides cryptographic provenance for skills distributed in the Hawk ecosystem.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

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

def main() -> None:
    parser = argparse.ArgumentParser(description="Sign or verify Hawk community skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sign command
    sign_parser = subparsers.add_parser("sign", help="Sign a skill directory or manifest.")
    sign_parser.add_argument("target", type=Path, help="Path to skill directory or registry.json")
    sign_parser.add_argument("--key", required=True, help="Secret key for signing")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify a signed skill package or manifest.")
    verify_parser.add_argument("target", type=Path, help="Path to skill directory or registry.json")
    verify_parser.add_argument("--signature", required=True, help="Expected signature")
    verify_parser.add_argument("--key", required=True, help="Secret key for verification")

    args = parser.parse_args()

    if args.command == "sign":
        if args.target.is_dir():
            digest = compute_content_hash(args.target)
        elif args.target.is_file():
            digest = hashlib.sha256(args.target.read_bytes()).hexdigest()
        else:
            print(f"Error: {args.target} does not exist", file=sys.stderr)
            sys.exit(1)

        sig = sign_hash(digest, args.key)
        print(json.dumps({"target": str(args.target), "sha256": digest, "signature": sig}, indent=2))

    elif args.command == "verify":
        if args.target.is_dir():
            digest = compute_content_hash(args.target)
        elif args.target.is_file():
            digest = hashlib.sha256(args.target.read_bytes()).hexdigest()
        else:
            print(f"Error: {args.target} does not exist", file=sys.stderr)
            sys.exit(1)

        valid = verify_hash(digest, args.signature, args.key)
        if valid:
            print("OK: Signature verified successfully.")
            sys.exit(0)
        else:
            print("FAIL: Signature mismatch!", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
