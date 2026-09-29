"""Tests for tools/sync_marketplace.py - marketplace sync logic."""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from sync_marketplace import extract_frontmatter, main

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def marketplace_env(tmp_path: Path):
    """Set up a fake repo root with categories/ and .claude-plugin/marketplace.json.

    Returns (repo_root, marketplace_path).
    """
    repo = tmp_path / "repo"
    repo.mkdir()

    # Create the marketplace.json template
    plugin_dir = repo / ".claude-plugin"
    plugin_dir.mkdir()
    marketplace = plugin_dir / "marketplace.json"
    marketplace.write_text(
        json.dumps(
            {"plugins": [{"name": "graycode-skills", "skills": []}]},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    # Create categories directory
    cats = repo / "categories"
    cats.mkdir()

    return repo, marketplace


def _create_skill(repo_root: Path, category: str, skill_name: str, frontmatter: str):
    """Helper to create a skill directory with a SKILL.md file."""
    skill_dir = repo_root / "categories" / category / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(frontmatter, encoding="utf-8")
    return skill_dir


# ---------------------------------------------------------------------------
# extract_frontmatter
# ---------------------------------------------------------------------------


class TestExtractFrontmatter:
    def test_valid_skill_md(self, tmp_path: Path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            textwrap.dedent("""\
            ---
            name: my-skill
            description: A useful skill
            license: MIT
            tags: [test]
            ---

            Body content.
            """),
            encoding="utf-8",
        )
        result = extract_frontmatter(skill_md)
        assert result["name"] == "my-skill"
        assert result["description"] == "A useful skill"

    def test_no_frontmatter_returns_empty(self, tmp_path: Path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("# Just a heading\n\nNo frontmatter.\n", encoding="utf-8")
        result = extract_frontmatter(skill_md)
        assert result == {}

    def test_malformed_yaml_returns_empty(self, tmp_path: Path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\n: [[[\n---\nBody\n", encoding="utf-8")
        result = extract_frontmatter(skill_md)
        assert result == {}


# ---------------------------------------------------------------------------
# main - end-to-end with filesystem
# ---------------------------------------------------------------------------


def _run(repo: Path, marketplace: Path, *argv: str):
    with (
        patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
        patch("sync_marketplace.MARKETPLACE", marketplace),
        patch("sync_marketplace.REPO_ROOT", repo),
        patch("sync_marketplace.VERSION_FILE", repo / "VERSION"),
        patch("sys.argv", ["sync_marketplace.py", *argv]),
    ):
        main()
    return json.loads(marketplace.read_text())


class TestMain:
    def test_one_plugin_per_category_with_directory_skills(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        (repo / "VERSION").write_text("1.2.3\n", encoding="utf-8")
        _create_skill(repo, "python", "skill-a", "---\nname: skill-a\ndescription: A\n---\nBody.\n")
        _create_skill(repo, "python", "skill-c", "---\nname: skill-c\ndescription: C\n---\nBody.\n")
        _create_skill(repo, "devops", "skill-b", "---\nname: skill-b\ndescription: B\n---\nBody.\n")

        data = _run(repo, marketplace)

        assert data["plugins"] == [
            {
                "name": "graycode-skills-devops",
                "source": "./categories/devops",
                "description": "GrayCode Skills, devops category: 1 skill.",
                "version": "1.2.3",
                "skills": ["./"],
            },
            {
                "name": "graycode-skills-python",
                "source": "./categories/python",
                "description": "GrayCode Skills, python category: 2 skills.",
                "version": "1.2.3",
                "skills": ["./"],
            },
        ]

    def test_skills_are_path_strings_not_objects(self, marketplace_env: tuple):
        """Regression (F121): Claude Code rejects object entries in `skills`."""
        repo, marketplace = marketplace_env
        _create_skill(repo, "tools", "my-tool", "---\nname: my-tool\ninvoke: /x:y\n---\nBody.\n")
        data = _run(repo, marketplace)
        for plugin in data["plugins"]:
            assert all(isinstance(entry, str) for entry in plugin["skills"])
            for entry in plugin["skills"]:
                assert (repo / plugin["source"] / entry).is_dir()

    def test_top_level_keys_preserved_and_defaults_filled(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        marketplace.write_text(
            json.dumps({"name": "custom", "metadata": {"x": 1}, "plugins": []}), encoding="utf-8"
        )
        _create_skill(repo, "tools", "t", "---\nname: t\n---\nBody.\n")
        data = _run(repo, marketplace)
        assert data["name"] == "custom"
        assert data["metadata"] == {"x": 1}
        assert data["owner"]["name"] == "GrayCode AI"
        assert "Agent Skills" in data["description"]
        assert list(data)[-1] == "plugins"

    def test_version_falls_back_to_template_without_version_file(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        marketplace.write_text(
            json.dumps({"plugins": [{"name": "old", "version": "9.9.9"}]}), encoding="utf-8"
        )
        _create_skill(repo, "tools", "t", "---\nname: t\n---\nBody.\n")
        data = _run(repo, marketplace)
        assert data["plugins"][0]["version"] == "9.9.9"

    def test_duplicate_skill_names_fail(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        _create_skill(repo, "a", "one", "---\nname: same\n---\nBody.\n")
        _create_skill(repo, "b", "two", "---\nname: same\n---\nBody.\n")
        with pytest.raises(SystemExit, match="Duplicate skill name 'same'"):
            _run(repo, marketplace)

    def test_name_falls_back_to_directory_name(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        _create_skill(repo, "tools", "dir-name", "---\ndescription: X\n---\n\nBody.\n")
        from sync_marketplace import build_skills

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            skills = build_skills()
        assert skills == [{"name": "dir-name", "category": "tools", "path": "categories/tools/dir-name"}]

    def test_skill_without_skill_md_skipped(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        skill_dir = repo / "categories" / "empty-cat" / "no-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "README.md").write_text("Not a skill.\n", encoding="utf-8")
        assert _run(repo, marketplace)["plugins"] == []

    def test_non_directory_files_in_categories_ignored(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        (repo / "categories" / "README.md").write_text("Categories readme.\n", encoding="utf-8")
        _create_skill(repo, "real-cat", "real-skill", "---\nname: real-skill\n---\n\nBody.\n")
        data = _run(repo, marketplace)
        assert [p["name"] for p in data["plugins"]] == ["graycode-skills-real-cat"]

    def test_check_mode(self, marketplace_env: tuple, capsys):
        repo, marketplace = marketplace_env
        _create_skill(repo, "tools", "t", "---\nname: t\n---\nBody.\n")
        _run(repo, marketplace)
        _run(repo, marketplace, "--check")
        assert "in sync" in capsys.readouterr().out
        _create_skill(repo, "other", "u", "---\nname: u\n---\nBody.\n")
        with pytest.raises(SystemExit) as exc:
            _run(repo, marketplace, "--check")
        assert exc.value.code == 1

    @pytest.mark.parametrize("content, message", [("{not json", "not valid JSON"), ("[]", "unexpected")])
    def test_invalid_template_fails(self, marketplace_env: tuple, content: str, message: str):
        repo, marketplace = marketplace_env
        marketplace.write_text(content, encoding="utf-8")
        with pytest.raises(SystemExit, match=message):
            _run(repo, marketplace)


def test_checked_in_marketplace_matches_claude_code_shape():
    """The committed manifest keeps the shape `claude plugin validate --strict`
    accepted and `claude plugin install` loaded (Claude Code 2.1.283,
    2026-09-27): a top-level description and, per plugin, a category source
    directory plus string `skills` paths that exist in the repo."""
    repo = Path(__file__).resolve().parent.parent
    data = json.loads((repo / ".claude-plugin" / "marketplace.json").read_text())
    assert data["name"] == "graycode-skills"
    assert data["description"]
    names = set()
    for plugin in data["plugins"]:
        assert set(plugin) == {"name", "source", "description", "version", "skills"}
        assert plugin["name"].startswith("graycode-skills-")
        category = plugin["name"].removeprefix("graycode-skills-")
        assert plugin["source"] == f"./categories/{category}"
        assert plugin["skills"] == ["./"]
        assert plugin["name"] not in names
        names.add(plugin["name"])
        assert any((repo / plugin["source"]).glob("*/SKILL.md"))
