"""Tests for tools/sign_manifest.py."""

from __future__ import annotations

import hashlib
import hmac
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from sign_manifest import (
    compute_content_hash,
    generate_ed25519_keypair,
    load_key_material,
    resolve_key,
    sign_hash,
    sign_hash_ed25519,
    verify_hash,
    verify_hash_ed25519,
    write_ed25519_keypair,
)

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"


def run_cli(*argv: str):
    """Invoke sign_manifest's CLI in-process; returns SystemExit code (or None)."""
    import sign_manifest

    old_argv = sys.argv
    sys.argv = ["sign_manifest.py", *argv]
    try:
        sign_manifest.main()
    except SystemExit as exc:
        return exc.code
    finally:
        sys.argv = old_argv
    return None


def test_compute_content_hash_single_file(tmp_path):
    # compute_content_hash operates on a directory; a single-file dir
    # must match the manual per-file hash (rel path + content).
    f = tmp_path / "sample.txt"
    f.write_text("hello world\n")
    expected = hashlib.sha256()
    expected.update(b"sample.txt")
    expected.update(b"hello world\n")
    assert compute_content_hash(tmp_path) == expected.hexdigest()


def test_compute_content_hash_empty_dir_returns_empty_digest(tmp_path):
    # An empty (or nonexistent) directory yields the SHA256 of nothing.
    assert compute_content_hash(tmp_path) == hashlib.sha256().hexdigest()


def test_compute_content_hash_is_deterministic(tmp_path):
    (tmp_path / "b.txt").write_text("bbb")
    (tmp_path / "a.txt").write_text("aaa")
    # Hash must be deterministic regardless of directory traversal order.
    first = compute_content_hash(tmp_path)
    second = compute_content_hash(tmp_path)
    assert first == second
    assert len(first) == 64  # SHA-256 hex digest length.


def test_sign_and_verify_round_trip():
    secret = "my-secret-key"
    digest = "abc123def456"
    signature = sign_hash(digest, secret)
    assert verify_hash(digest, signature, secret)
    assert not verify_hash("tampered", signature, secret)


def test_verify_wrong_secret_fails():
    digest = "deadbeef"
    sig = sign_hash(digest, "secret-a")
    assert not verify_hash(digest, sig, "secret-b")


def test_signature_is_deterministic():
    # Same inputs must produce the same signature (HMAC is deterministic).
    sig1 = sign_hash("digest", "key")
    sig2 = sign_hash("digest", "key")
    assert sig1 == sig2
    # And it must match a manual HMAC computation.
    expected = hmac.new(b"key", b"digest", hashlib.sha256).hexdigest()
    assert sig1 == expected


# ---------------------------------------------------------------------------
# Ed25519 (asymmetric) scheme
# ---------------------------------------------------------------------------


def test_ed25519_keygen_returns_pem_pair():
    private_pem, public_pem = generate_ed25519_keypair()
    assert "-----BEGIN PRIVATE KEY-----" in private_pem
    assert "-----END PRIVATE KEY-----" in private_pem
    assert "-----BEGIN PUBLIC KEY-----" in public_pem
    assert "-----END PUBLIC KEY-----" in public_pem


def test_ed25519_sign_and_verify_round_trip():
    private_pem, public_pem = generate_ed25519_keypair()
    digest = "abc123def456"
    signature = sign_hash_ed25519(digest, private_pem)
    assert verify_hash_ed25519(digest, signature, public_pem)
    assert not verify_hash_ed25519("tampered", signature, public_pem)


def test_ed25519_wrong_public_key_fails():
    private_a, _ = generate_ed25519_keypair()
    _, public_b = generate_ed25519_keypair()
    sig = sign_hash_ed25519("deadbeef", private_a)
    # A signature from keypair A must not verify against keypair B — unlike
    # the legacy shared-secret scheme, verifiers cannot forge signatures.
    assert not verify_hash_ed25519("deadbeef", sig, public_b)


def test_ed25519_malformed_signature_fails():
    _, public_pem = generate_ed25519_keypair()
    assert not verify_hash_ed25519("digest", "not-hex-zz!", public_pem)


def test_ed25519_malformed_public_key_fails():
    assert not verify_hash_ed25519("digest", "00" * 64, "not-a-pem")


def test_ed25519_sign_rejects_non_pem_private_key():
    # An HMAC-style shared secret is not a valid PEM private key.
    with pytest.raises(ValueError):
        sign_hash_ed25519("digest", "my-shared-secret")


def test_write_ed25519_keypair_writes_files(tmp_path):
    private_out = tmp_path / "signing-private.pem"
    public_out = tmp_path / "signing-public.pem"
    private_pem, public_pem = write_ed25519_keypair(private_out, public_out)
    assert private_out.read_text(encoding="utf-8") == private_pem
    assert public_out.read_text(encoding="utf-8") == public_pem
    # The private key file must only be readable by its owner.
    assert (private_out.stat().st_mode & 0o777) == 0o600
    # And the written pair must actually work for sign/verify.
    sig = sign_hash_ed25519("digest", private_pem)
    assert verify_hash_ed25519("digest", sig, public_pem)


def test_load_key_material_accepts_pem_file_path(tmp_path):
    _, public_pem = generate_ed25519_keypair()
    key_file = tmp_path / "public.pem"
    key_file.write_text(public_pem, encoding="utf-8")
    # Literal PEM is passed through; a path to a PEM file is read from disk.
    assert load_key_material(public_pem) == public_pem
    assert load_key_material(str(key_file)) == public_pem
    # Anything else is returned unchanged (key parsing fails later if invalid).
    assert load_key_material("raw-secret") == "raw-secret"


def test_resolve_key_env_fallback(monkeypatch):
    monkeypatch.setenv("SKILLS_ED25519_PRIVATE_KEY", "env-value")
    assert resolve_key(None, "SKILLS_ED25519_PRIVATE_KEY", "test") == "env-value"
    # An explicit CLI value wins over the environment.
    assert resolve_key("cli-value", "SKILLS_ED25519_PRIVATE_KEY", "test") == "cli-value"


def test_resolve_key_missing_exits(monkeypatch):
    monkeypatch.delenv("SKILLS_ED25519_PRIVATE_KEY", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        resolve_key(None, "SKILLS_ED25519_PRIVATE_KEY", "test")
    assert excinfo.value.code == 2


def test_cli_ed25519_sign_verify_end_to_end(tmp_path, capsys):
    # Full CLI round trip: keygen writes key files, sign uses the private
    # key file path, verify accepts the pinned public key file path.
    private_out = tmp_path / "signing-private.pem"
    public_out = tmp_path / "signing-public.pem"
    run_cli("keygen", "--private-out", str(private_out), "--public-out", str(public_out))
    capsys.readouterr()  # drain keygen output
    assert private_out.read_text(encoding="utf-8").startswith("-----BEGIN PRIVATE KEY-----")
    assert public_out.read_text(encoding="utf-8").startswith("-----BEGIN PUBLIC KEY-----")

    target = tmp_path / "registry.json"
    target.write_text('{"skills": []}', encoding="utf-8")

    run_cli("sign", str(target), "--ed25519", "--key", str(private_out))
    result = json.loads(capsys.readouterr().out)
    assert result["algorithm"] == "ed25519"
    assert result["sha256"] == hashlib.sha256(b'{"skills": []}').hexdigest()

    run_cli("verify", str(target), "--ed25519", "--key", str(public_out),
            "--signature", result["signature"])
    assert "OK" in capsys.readouterr().out

    # A tampered digest must fail verification with a non-zero exit code.
    target.write_text('{"skills": ["tampered"]}', encoding="utf-8")
    code = run_cli("verify", str(target), "--ed25519", "--key", str(public_out),
                   "--signature", result["signature"])
    assert code == 1
    assert "FAIL" in capsys.readouterr().err


def test_cli_hmac_sign_verify_still_works(tmp_path, capsys):
    # The legacy shared-secret scheme remains the default and unchanged.
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    run_cli("sign", str(target), "--key", "dev-fallback-key")
    result = json.loads(capsys.readouterr().out)
    assert result["algorithm"] == "hmac-sha256"
    # Legacy scheme: HMAC over the SHA-256 hex digest of the file contents.
    digest = hashlib.sha256(b"{}").hexdigest()
    expected = hmac.new(b"dev-fallback-key", digest.encode("utf-8"), hashlib.sha256).hexdigest()
    assert result["sha256"] == digest
    assert result["signature"] == expected
    run_cli("verify", str(target), "--key", "dev-fallback-key", "--signature", expected)
    assert "OK" in capsys.readouterr().out


def test_cli_keygen_without_files_prints_json_keypair(capsys):
    run_cli("keygen")
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["algorithm"] == "ed25519"
    assert result["private_key"].startswith("-----BEGIN PRIVATE KEY-----")
    assert result["public_key"].startswith("-----BEGIN PUBLIC KEY-----")
    assert "Never commit the private key" in captured.err


def test_cli_sign_missing_target_exits_nonzero(tmp_path, capsys):
    code = run_cli("sign", str(tmp_path / "nope.json"), "--key", "k")
    assert code == 1
    assert "does not exist" in capsys.readouterr().err


def test_cli_verify_hmac_mismatch_exits_nonzero(tmp_path, capsys):
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    code = run_cli("verify", str(target), "--key", "k", "--signature", "00" * 32)
    assert code == 1
    assert "FAIL" in capsys.readouterr().err


def test_cli_verify_ed25519_uses_public_key_env(tmp_path, capsys, monkeypatch):
    # Verification can be keyed purely from the pinned public key env var.
    _, public_pem = generate_ed25519_keypair()
    monkeypatch.setenv("SKILLS_ED25519_PUBLIC_KEY", public_pem)
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    digest = hashlib.sha256(b"{}").hexdigest()
    # Sign with a different (wrong) key so verification must fail.
    wrong_private, _ = generate_ed25519_keypair()
    wrong_sig = sign_hash_ed25519(digest, wrong_private)
    code = run_cli("verify", str(target), "--ed25519", "--signature", wrong_sig)
    assert code == 1
    assert "FAIL" in capsys.readouterr().err


def test_cli_missing_key_exits_with_usage_error(tmp_path, capsys, monkeypatch):
    for env in ("SKILLS_SIGNING_KEY", "SKILLS_ED25519_PRIVATE_KEY", "SKILLS_ED25519_PUBLIC_KEY"):
        monkeypatch.delenv(env, raising=False)
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    code = run_cli("sign", str(target))
    assert code == 2
    assert "SKILLS_SIGNING_KEY" in capsys.readouterr().err
