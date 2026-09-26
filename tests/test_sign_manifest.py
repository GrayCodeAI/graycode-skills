"""Tests for tools/sign_manifest.py (Ed25519-only registry signing).

Every test uses a throwaway keypair generated in-process; the real private key
only exists as the SKILLS_ED25519_PRIVATE_KEY GitHub Actions secret.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import sign_manifest
from sign_manifest import (
    PINNED_PUBLIC_KEY_PATH,
    build_signature_document,
    compute_content_hash,
    generate_ed25519_keypair,
    load_key_material,
    resolve_key,
    sign_hash_ed25519,
    target_digest,
    verify_hash_ed25519,
    verify_signature_document,
    write_ed25519_keypair,
)

# The public key Rho pins (graycode-eco spec, 2026-09-27). If this changes, Rho's
# pinned copy must change in the same release, so the test fails loudly.
EXPECTED_PINNED_PUBLIC_KEY = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEAr9I2NG1Sih9Mu04/eOA8FmJhczSLBYiXeLAl1rqusQU=\n"
    "-----END PUBLIC KEY-----\n"
)


def run_cli(*argv: str):
    """Invoke sign_manifest's CLI in-process; returns SystemExit code (or None)."""
    old_argv = sys.argv
    sys.argv = ["sign_manifest.py", *argv]
    try:
        sign_manifest.main()
    except SystemExit as exc:
        return exc.code
    finally:
        sys.argv = old_argv
    return None


@pytest.fixture
def keypair(tmp_path):
    private_out = tmp_path / "throwaway-private.pem"
    public_out = tmp_path / "throwaway-public.pem"
    private_pem, public_pem = write_ed25519_keypair(private_out, public_out)
    return private_out, public_out, private_pem, public_pem


@pytest.fixture(autouse=True)
def _no_key_env(monkeypatch):
    for env in ("SKILLS_SIGNING_KEY", "SKILLS_ED25519_PRIVATE_KEY", "SKILLS_ED25519_PUBLIC_KEY"):
        monkeypatch.delenv(env, raising=False)


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------


def test_compute_content_hash_single_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello world\n")
    expected = hashlib.sha256()
    expected.update(b"sample.txt")
    expected.update(b"hello world\n")
    assert compute_content_hash(tmp_path) == expected.hexdigest()


def test_compute_content_hash_empty_dir_returns_empty_digest(tmp_path):
    assert compute_content_hash(tmp_path) == hashlib.sha256().hexdigest()


def test_compute_content_hash_is_deterministic(tmp_path):
    (tmp_path / "b.txt").write_text("bbb")
    (tmp_path / "a.txt").write_text("aaa")
    first = compute_content_hash(tmp_path)
    assert first == compute_content_hash(tmp_path)
    assert len(first) == 64


def test_target_digest_file_dir_and_missing(tmp_path):
    f = tmp_path / "registry.json"
    f.write_bytes(b'{"skills": []}')
    assert target_digest(f) == hashlib.sha256(b'{"skills": []}').hexdigest()
    assert target_digest(tmp_path) == compute_content_hash(tmp_path)
    assert target_digest(tmp_path / "missing.json") is None


# ---------------------------------------------------------------------------
# Ed25519 primitives
# ---------------------------------------------------------------------------


def test_ed25519_keygen_returns_pem_pair():
    private_pem, public_pem = generate_ed25519_keypair()
    assert "-----BEGIN PRIVATE KEY-----" in private_pem
    assert "-----BEGIN PUBLIC KEY-----" in public_pem


def test_ed25519_sign_and_verify_round_trip():
    private_pem, public_pem = generate_ed25519_keypair()
    signature = sign_hash_ed25519("abc123def456", private_pem)
    assert verify_hash_ed25519("abc123def456", signature, public_pem)
    assert not verify_hash_ed25519("tampered", signature, public_pem)


def test_signed_message_is_ascii_hex_digest_not_raw_bytes():
    # Contract: the message is the 64 ASCII bytes of the lowercase hex digest.
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import serialization

    private_pem, public_pem = generate_ed25519_keypair()
    digest = hashlib.sha256(b"registry bytes").hexdigest()
    signature = bytes.fromhex(sign_hash_ed25519(digest, private_pem))
    public_key = serialization.load_pem_public_key(public_pem.encode())
    public_key.verify(signature, digest.encode("ascii"))  # raises if wrong
    with pytest.raises(InvalidSignature):
        public_key.verify(signature, bytes.fromhex(digest))
    assert len(signature) == 64


def test_ed25519_wrong_public_key_fails():
    private_a, _ = generate_ed25519_keypair()
    _, public_b = generate_ed25519_keypair()
    sig = sign_hash_ed25519("deadbeef", private_a)
    assert not verify_hash_ed25519("deadbeef", sig, public_b)


def test_ed25519_malformed_signature_fails():
    _, public_pem = generate_ed25519_keypair()
    assert not verify_hash_ed25519("digest", "not-hex-zz!", public_pem)


def test_ed25519_malformed_public_key_fails():
    assert not verify_hash_ed25519("digest", "00" * 64, "not-a-pem")


def test_ed25519_sign_rejects_non_pem_private_key():
    # A former HMAC shared secret is not a valid Ed25519 private key.
    with pytest.raises(ValueError):
        sign_hash_ed25519("digest", "my-shared-secret")


def test_hmac_scheme_is_gone():
    assert not hasattr(sign_manifest, "sign_hash")
    assert not hasattr(sign_manifest, "verify_hash")
    assert not hasattr(sign_manifest, "HMAC_KEY_ENV")


# ---------------------------------------------------------------------------
# Pinned public key
# ---------------------------------------------------------------------------


def test_pinned_public_key_is_committed_and_matches_rho_pin():
    assert PINNED_PUBLIC_KEY_PATH == sign_manifest.REPO_ROOT / "keys" / "registry-ed25519.pub"
    assert PINNED_PUBLIC_KEY_PATH.read_text(encoding="utf-8") == EXPECTED_PINNED_PUBLIC_KEY


def test_pinned_public_key_is_an_ed25519_public_key():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    key = serialization.load_pem_public_key(EXPECTED_PINNED_PUBLIC_KEY.encode())
    assert isinstance(key, Ed25519PublicKey)


def test_no_private_key_material_is_committed():
    repo = sign_manifest.REPO_ROOT
    for path in (repo / "keys").iterdir():
        assert "PRIVATE KEY" not in path.read_text(encoding="utf-8"), path


# ---------------------------------------------------------------------------
# Signature documents (the registry contract)
# ---------------------------------------------------------------------------


def _signed(tmp_path, private_pem, payload=b'{"version": 1, "skills": []}\n'):
    target = tmp_path / "registry.json"
    target.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    document = build_signature_document(target, digest, sign_hash_ed25519(digest, private_pem))
    return target, document


def test_build_signature_document_shape(tmp_path, keypair):
    _, _, private_pem, _ = keypair
    target, document = _signed(tmp_path, private_pem)
    assert set(document) == {"target", "sha256", "algorithm", "signature"}
    assert document["target"] == "registry.json"
    assert document["algorithm"] == "ed25519"
    assert document["sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()
    assert len(bytes.fromhex(document["signature"])) == 64


def test_verify_signature_document_accepts_valid(tmp_path, keypair):
    _, _, private_pem, public_pem = keypair
    target, document = _signed(tmp_path, private_pem)
    assert verify_signature_document(target, document, public_pem) == []


@pytest.mark.parametrize(
    "mutate, expected",
    [
        (lambda d: d.update(algorithm="hmac-sha256"), "algorithm must be 'ed25519'"),
        (lambda d: d.update(target="other.json"), "target must be 'registry.json'"),
        (lambda d: d.update(sha256="0" * 64), "sha256 mismatch"),
        (lambda d: d.update(sha256="ABC"), "sha256 must be a lowercase"),
        (lambda d: d.update(signature=""), "signature must be a non-empty"),
        (lambda d: d.update(signature="00" * 64), "does not verify"),
    ],
)
def test_verify_signature_document_rejects_tampering(tmp_path, keypair, mutate, expected):
    _, _, private_pem, public_pem = keypair
    target, document = _signed(tmp_path, private_pem)
    mutate(document)
    problems = verify_signature_document(target, document, public_pem)
    assert any(expected in p for p in problems), problems


def test_verify_signature_document_rejects_modified_registry(tmp_path, keypair):
    _, _, private_pem, public_pem = keypair
    target, document = _signed(tmp_path, private_pem)
    target.write_bytes(b'{"version": 1, "skills": [{"name": "evil"}]}\n')
    problems = verify_signature_document(target, document, public_pem)
    assert any("sha256 mismatch" in p for p in problems)


def test_verify_signature_document_rejects_other_signer(tmp_path, keypair):
    _, _, private_pem, _ = keypair
    _, other_public = generate_ed25519_keypair()
    target, document = _signed(tmp_path, private_pem)
    problems = verify_signature_document(target, document, other_public)
    assert problems == ["Ed25519 signature does not verify with the given public key"]


def test_verify_signature_document_rejects_non_object(tmp_path):
    assert verify_signature_document(tmp_path, ["x"], "pem") == [
        "signature document must be a JSON object"
    ]


def test_verify_signature_document_missing_target(tmp_path, keypair):
    _, _, private_pem, public_pem = keypair
    target, document = _signed(tmp_path, private_pem)
    target.unlink()
    assert any("does not exist" in p for p in verify_signature_document(target, document, public_pem))


# ---------------------------------------------------------------------------
# Key resolution
# ---------------------------------------------------------------------------


def test_write_ed25519_keypair_writes_files(keypair):
    private_out, public_out, private_pem, public_pem = keypair
    assert private_out.read_text(encoding="utf-8") == private_pem
    assert public_out.read_text(encoding="utf-8") == public_pem
    assert (private_out.stat().st_mode & 0o777) == 0o600
    assert verify_hash_ed25519("digest", sign_hash_ed25519("digest", private_pem), public_pem)


def test_load_key_material_accepts_pem_file_path(keypair):
    _, public_out, _, public_pem = keypair
    assert load_key_material(public_pem) == public_pem
    assert load_key_material(str(public_out)) == public_pem
    assert load_key_material("raw-secret") == "raw-secret"


def test_resolve_key_env_fallback(monkeypatch):
    monkeypatch.setenv("SKILLS_ED25519_PRIVATE_KEY", "env-value")
    assert resolve_key(None, "SKILLS_ED25519_PRIVATE_KEY", "test") == "env-value"
    assert resolve_key("cli-value", "SKILLS_ED25519_PRIVATE_KEY", "test") == "cli-value"


def test_resolve_key_missing_exits():
    with pytest.raises(SystemExit) as excinfo:
        resolve_key(None, "SKILLS_ED25519_PRIVATE_KEY", "test")
    assert excinfo.value.code == 2


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_sign_verify_end_to_end(tmp_path, capsys, keypair):
    private_out, public_out, _, _ = keypair
    target = tmp_path / "registry.json"
    target.write_text('{"skills": []}', encoding="utf-8")

    # `--ed25519` stays accepted: it is the documented publish command.
    run_cli("sign", str(target), "--ed25519", "--key", str(private_out))
    result = json.loads(capsys.readouterr().out)
    assert result == {
        "target": "registry.json",
        "sha256": hashlib.sha256(b'{"skills": []}').hexdigest(),
        "algorithm": "ed25519",
        "signature": result["signature"],
    }

    run_cli("verify", str(target), "--key", str(public_out), "--signature", result["signature"])
    assert "OK" in capsys.readouterr().out

    sig_file = tmp_path / "registry-signature.json"
    sig_file.write_text(json.dumps(result), encoding="utf-8")
    code = run_cli("verify", str(target), "--key", str(public_out), "--signature-file", str(sig_file))
    assert code == 0
    assert "OK" in capsys.readouterr().out

    target.write_text('{"skills": ["tampered"]}', encoding="utf-8")
    code = run_cli("verify", str(target), "--key", str(public_out), "--signature", result["signature"])
    assert code == 1
    assert "FAIL" in capsys.readouterr().err
    code = run_cli("verify", str(target), "--key", str(public_out), "--signature-file", str(sig_file))
    assert code == 1
    assert "sha256 mismatch" in capsys.readouterr().err


def test_cli_sign_uses_private_key_env(tmp_path, capsys, monkeypatch, keypair):
    _, _, private_pem, public_pem = keypair
    monkeypatch.setenv("SKILLS_ED25519_PRIVATE_KEY", private_pem)
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    assert run_cli("sign", str(target)) is None
    document = json.loads(capsys.readouterr().out)
    assert verify_signature_document(target, document, public_pem) == []


def test_cli_sign_without_key_fails_closed(tmp_path, capsys):
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    code = run_cli("sign", str(target), "--ed25519")
    assert code == 2
    assert "SKILLS_ED25519_PRIVATE_KEY" in capsys.readouterr().err


def test_cli_sign_rejects_legacy_hmac_secret(tmp_path, capsys):
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    code = run_cli("sign", str(target), "--key", "dev-fallback-key")
    assert code == 2
    assert "invalid Ed25519 private key" in capsys.readouterr().err


def test_cli_sign_missing_target_exits_nonzero(tmp_path, capsys):
    code = run_cli("sign", str(tmp_path / "nope.json"), "--key", "k")
    assert code == 1
    assert "does not exist" in capsys.readouterr().err


def test_cli_verify_defaults_to_pinned_public_key(tmp_path, capsys, monkeypatch, keypair):
    # With no --key and no env var, verify uses the committed pinned key; a
    # signature from any other key (here: a throwaway key) must be rejected.
    _, _, private_pem, _ = keypair
    target, document = _signed(tmp_path, private_pem)
    sig_file = tmp_path / "registry-signature.json"
    sig_file.write_text(json.dumps(document), encoding="utf-8")
    code = run_cli("verify", str(target), "--signature-file", str(sig_file))
    assert code == 1
    assert "does not verify" in capsys.readouterr().err

    # Point the pinned path at the throwaway public key to prove it is used.
    _, public_out, _, _ = keypair
    monkeypatch.setattr(sign_manifest, "PINNED_PUBLIC_KEY_PATH", public_out)
    assert run_cli("verify", str(target), "--signature-file", str(sig_file)) == 0


def test_cli_verify_uses_public_key_env(tmp_path, capsys, monkeypatch, keypair):
    _, _, _, public_pem = keypair
    monkeypatch.setenv("SKILLS_ED25519_PUBLIC_KEY", public_pem)
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    wrong_private, _ = generate_ed25519_keypair()
    wrong_sig = sign_hash_ed25519(hashlib.sha256(b"{}").hexdigest(), wrong_private)
    code = run_cli("verify", str(target), "--signature", wrong_sig)
    assert code == 1
    assert "FAIL" in capsys.readouterr().err


def test_cli_verify_missing_pinned_key_exits_2(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sign_manifest, "PINNED_PUBLIC_KEY_PATH", tmp_path / "absent.pub")
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    code = run_cli("verify", str(target), "--signature", "00")
    assert code == 2
    assert "no key provided" in capsys.readouterr().err


def test_cli_verify_unreadable_signature_file(tmp_path, capsys, keypair):
    _, public_out, _, _ = keypair
    target = tmp_path / "registry.json"
    target.write_text("{}", encoding="utf-8")
    bad = tmp_path / "registry-signature.json"
    bad.write_text("not json", encoding="utf-8")
    code = run_cli("verify", str(target), "--key", str(public_out), "--signature-file", str(bad))
    assert code == 1
    assert "cannot read" in capsys.readouterr().err


def test_cli_keygen_without_files_prints_json_keypair(capsys):
    run_cli("keygen")
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["algorithm"] == "ed25519"
    assert result["private_key"].startswith("-----BEGIN PRIVATE KEY-----")
    assert result["public_key"].startswith("-----BEGIN PUBLIC KEY-----")
    assert "Never commit the private key" in captured.err
