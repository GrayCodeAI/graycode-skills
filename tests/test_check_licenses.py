"""Tests for tools/check_licenses.py (copyleft gate, F116)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import check_licenses as cl


@pytest.mark.parametrize(
    "value",
    [
        "GPL-3.0",
        "GPL-2.0 license",
        "GPLv3 license",
        "AGPL-3.0",
        "AGPL-3.0 (referencing Twitter's algorithm source)",
        "LGPL-2.1-or-later",
        "For MATLAB and for Octave (GNU General Public License version 3)",
        "GNU Affero General Public License v3",
    ],
)
def test_copyleft_values_are_detected(value):
    assert cl.is_copyleft_license_value(value)


@pytest.mark.parametrize(
    "value",
    ["MIT", "MIT license", "Apache-2.0", "BSD-3-Clause license", "ISC", "CC-BY-4.0", "MPL-2.0",
     "Proprietary. LICENSE.txt has complete terms", "Unknown"],
)
def test_permissive_values_are_not_flagged(value):
    assert not cl.is_copyleft_license_value(value)


def _skill(root: Path, rel: str, license_line: str | None) -> Path:
    skill = root / "categories" / rel
    skill.mkdir(parents=True)
    fm = "---\nname: x\ndescription: d\n"
    if license_line is not None:
        fm += f"license: {license_line}\n"
    (skill / "SKILL.md").write_text(fm + "tags: [a]\n---\nBody\n", encoding="utf-8")
    return skill


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setattr(cl, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(cl, "CATEGORIES_DIR", tmp_path / "categories")
    monkeypatch.setattr(cl, "EXCEPTIONS_PATH", tmp_path / "license_exceptions.txt")
    return tmp_path


def test_find_violations_covers_frontmatter_and_license_files(repo):
    _skill(repo, "general/ok", "MIT")
    _skill(repo, "general/fm-gpl", "GPL-3.0")
    lic_skill = _skill(repo, "general/file-gpl", "MIT")
    (lic_skill / "LICENSE").write_text("GNU GENERAL PUBLIC LICENSE\nVersion 3\n", encoding="utf-8")
    _skill(repo, "general/no-license", None)

    violations, checked = cl.find_violations()

    assert checked == 5  # 1 LICENSE file + 4 SKILL.md files
    assert ("categories/general/fm-gpl", "frontmatter license: 'GPL-3.0'") in violations
    assert ("categories/general/file-gpl/LICENSE", "LICENSE file is GPL") in violations
    assert len(violations) == 2


def test_main_fails_on_unreviewed_violation(repo, capsys):
    _skill(repo, "general/fm-gpl", "AGPL-3.0")
    with pytest.raises(SystemExit) as exc:
        _run_main([])
    assert exc.value.code == 1
    assert "categories/general/fm-gpl" in capsys.readouterr().out


def _run_main(argv):
    old = sys.argv
    sys.argv = ["check_licenses.py", *argv]
    try:
        cl.main()
    finally:
        sys.argv = old


def test_reviewed_exception_passes(repo, capsys):
    _skill(repo, "general/fm-gpl", "AGPL-3.0")
    (repo / "license_exceptions.txt").write_text(
        "# reviewed\ncategories/general/fm-gpl  # pending relicense\n", encoding="utf-8"
    )
    _run_main([])
    assert "1 reviewed exception(s)" in capsys.readouterr().out


def test_stale_exception_fails(repo, capsys):
    _skill(repo, "general/ok", "MIT")
    (repo / "license_exceptions.txt").write_text("categories/general/ok\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _run_main([])
    assert exc.value.code == 1
    assert "stale" in capsys.readouterr().out


def test_warn_mode_reports_without_failing(repo, capsys):
    _skill(repo, "general/fm-gpl", "GPL-2.0")
    _run_main(["--warn"])
    assert "⚠" in capsys.readouterr().out

