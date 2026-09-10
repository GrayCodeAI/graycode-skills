"""Tests for tools/package_skill.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from package_skill import SAFE_NAME_RE, SAFE_VERSION_RE, _sanitized_identifier, compute_checksum

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def skill_dir(tmp_path: Path) -> Path:
    d = tmp_path / "my-skill"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\nname: my-skill\ndescription: A test skill\nlicense: MIT\nversion: 1.0\n---\n# My Skill\n",
        encoding="utf-8",
    )
    (d / "helper.sh").write_text("#!/bin/sh\necho hi\n", encoding="utf-8")
    return d


def test_sanitized_identifier_accepts_safe():
    assert _sanitized_identifier("my-skill", "name", SAFE_NAME_RE) == "my-skill"
    assert _sanitized_identifier("1.0", "version", SAFE_VERSION_RE) == "1.0"


def test_sanitized_identifier_rejects_path_traversal():
    with pytest.raises(SystemExit):
        _sanitized_identifier("../../../../tmp/pwned", "name", SAFE_NAME_RE)


def test_compute_checksum(tmp_path: Path):
    f = tmp_path / "data.txt"
    f.write_bytes(b"hello world")
    assert compute_checksum(f) == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


def test_package_skill_end_to_end(skill_dir: Path, tmp_path: Path):
    out = tmp_path / "dist"
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "package_skill.py"),
            str(skill_dir),
            "--skip-validate",
            "--output-dir",
            str(out),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    archive = out / "my-skill-1.0.tar.gz"
    meta = out / "my-skill-1.0.meta.json"
    assert archive.exists()
    assert meta.exists()
    metadata = json.loads(meta.read_text(encoding="utf-8"))
    assert metadata["name"] == "my-skill"
    assert metadata["version"] == "1.0"
    assert metadata["sha256"] == compute_checksum(archive)
    with tarfile.open(archive, "r:gz") as tar:
        names = tar.getnames()
    assert "my-skill/SKILL.md" in names
    assert "my-skill/helper.sh" in names
