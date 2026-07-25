"""Tests for tools/sign_manifest.py."""

from __future__ import annotations

import hashlib
import hmac
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from sign_manifest import compute_content_hash, sign_hash, verify_hash


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
