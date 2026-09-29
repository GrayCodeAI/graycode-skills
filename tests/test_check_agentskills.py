"""Tests for tools/check_agentskills.py and spec-style tags (F287)."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import check_agentskills as ca
from frontmatter import frontmatter_tags
from validate_skill import validate_skill


def _skill(root: Path, name: str, frontmatter: str) -> Path:
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(f"---\n{textwrap.dedent(frontmatter)}---\n\nBody.\n", encoding="utf-8")
    return skill


CONFORMANT = """\
name: good-skill
description: Does one thing. Use when that thing is needed.
license: MIT
compatibility: Requires git
allowed-tools: Bash(git:*) Read
metadata:
  author: GrayCode AI
  version: "1.0"
  tags: rho, workflow
"""


def test_conformant_skill_has_no_problems(tmp_path):
    assert ca.check_skill(_skill(tmp_path, "good-skill", CONFORMANT)) == []


@pytest.mark.parametrize(
    "name, rule",
    [
        ("Upper-Case", "name-format"),
        ("double--hyphen", "name-format"),
        ("-leading", "name-format"),
        ("under_score", "name-format"),
        ("a" * 65, "name-length"),
    ],
)
def test_name_rules(tmp_path, name, rule):
    skill = _skill(tmp_path, name, f"name: {name}\ndescription: d\n")
    assert rule in {r for r, _ in ca.check_skill(skill)}


def test_other_rules(tmp_path):
    skill = _skill(
        tmp_path,
        "dir-name",
        "name: other-name\ndescription: ''\ntags: [a]\ncompatibility: ''\n"
        "metadata: None\nallowed-tools: [Read]\nlicense: 3\n",
    )
    rules = {r for r, _ in ca.check_skill(skill)}
    assert rules == {
        "unexpected-field",
        "name-directory",
        "description",
        "compatibility",
        "metadata",
        "allowed-tools",
        "license",
    }


def test_long_description_and_missing_frontmatter(tmp_path):
    long_desc = _skill(tmp_path, "long", "name: long\ndescription: " + "x" * 1025 + "\n")
    assert ("description-length" in {r for r, _ in ca.check_skill(long_desc)})
    bare = tmp_path / "bare"
    bare.mkdir()
    (bare / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
    assert ca.check_skill(bare) == [("frontmatter", "SKILL.md has no YAML frontmatter mapping")]


def test_strict_mode_exit_codes(tmp_path, capsys):
    category = tmp_path / "cat"
    _skill(category, "good-skill", CONFORMANT)
    assert ca.main(["--strict", str(category)]) == 0
    assert "1 skill(s) conform" in capsys.readouterr().out
    _skill(category, "bad", "name: bad\ndescription: d\ntags: [x]\n")
    assert ca.main(["--strict", str(category)]) == 1
    assert "unexpected-field" in capsys.readouterr().out
    assert ca.main(["--strict", str(tmp_path / "missing")]) == 1


def test_all_mode_reports_without_failing(tmp_path, monkeypatch, capsys):
    category = tmp_path / "categories" / "cat"
    _skill(category, "good-skill", CONFORMANT)
    _skill(category, "legacy", "name: legacy\ndescription: d\ntags: [x]\n")
    monkeypatch.setattr(ca, "CATEGORIES_DIR", tmp_path / "categories")
    assert ca.main(["--all"]) == 0
    out = capsys.readouterr().out
    assert "1/2 skills conform" in out
    assert "unexpected-field: 1" in out


def test_first_party_ecosystem_skills_conform():
    """categories/graycode holds GrayCode's own skills; they must follow the spec."""
    graycode = ca.CATEGORIES_DIR / "graycode"
    assert sorted(p.name for p in graycode.iterdir() if (p / "SKILL.md").is_file()) == [
        "across-checkpoint",
        "rho-workflow",
        "rover-verify",
    ]
    assert ca.main(["--strict", str(graycode)]) == 0


# ---------------------------------------------------------------------------
# metadata.tags: spec-conformant skills keep tags out of the top level
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "frontmatter, expected",
    [
        ({"tags": ["a", "b"]}, ["a", "b"]),
        ({"tags": "a, b"}, "a, b"),
        ({"metadata": {"tags": "rho, workflow  cli"}}, ["rho", "workflow", "cli"]),
        ({"tags": ["top"], "metadata": {"tags": "ignored"}}, ["top"]),
        ({"metadata": {"author": "x"}}, None),
        ({"metadata": "None"}, None),
        ({}, None),
    ],
)
def test_frontmatter_tags(frontmatter, expected):
    assert frontmatter_tags(frontmatter) == expected


def test_validator_accepts_metadata_tags(tmp_path):
    skill = _skill(tmp_path, "good-skill", CONFORMANT)
    result = validate_skill(skill)
    assert result.errors == []
    assert result.warnings == []


def test_validator_still_requires_some_tags(tmp_path):
    skill = _skill(tmp_path, "no-tags", "name: no-tags\ndescription: d\nlicense: MIT\n")
    assert any("at least 1 tag" in e for e in validate_skill(skill).errors)


def test_list_allowed_tools_passes_the_gate_but_not_the_spec(tmp_path):
    """Two ingested skills use a YAML list (tool names with spaces); the corpus
    gate accepts it, the conformance checker flags it."""
    skill = _skill(
        tmp_path,
        "tools-list",
        "name: tools-list\ndescription: d\nlicense: MIT\ntags: [a]\n"
        "allowed-tools: [Azure MCP/documentation]\n",
    )
    assert validate_skill(skill).errors == []
    assert "allowed-tools" in {rule for rule, _ in ca.check_skill(skill)}
