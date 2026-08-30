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
            {"plugins": [{"name": "starling", "skills": []}]},
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


class TestMain:
    def test_syncs_single_skill(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        _create_skill(
            repo,
            "python",
            "code-review",
            textwrap.dedent("""\
            ---
            name: code-review
            description: Reviews code
            invoke: /hawk:code-review
            ---

            Body.
            """),
        )

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert len(skills) == 1
        assert skills[0]["name"] == "code-review"
        assert skills[0]["path"] == "categories/python/code-review"
        assert skills[0]["invoke"] == "/hawk:code-review"

    def test_syncs_multiple_skills_across_categories(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        _create_skill(
            repo,
            "python",
            "skill-a",
            "---\nname: skill-a\ndescription: A\ninvoke: /hawk:a\n---\n\nBody.\n",
        )
        _create_skill(
            repo,
            "devops",
            "skill-b",
            "---\nname: skill-b\ndescription: B\ninvoke: /hawk:b\n---\n\nBody.\n",
        )

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert len(skills) == 2
        names = [s["name"] for s in skills]
        # Should be sorted by category then skill name
        assert "skill-a" in names
        assert "skill-b" in names

    def test_sorted_output(self, marketplace_env: tuple):
        """Skills should be sorted by category then by skill directory name."""
        repo, marketplace = marketplace_env
        _create_skill(repo, "z-cat", "aaa-skill", "---\nname: aaa-skill\n---\n\nBody.\n")
        _create_skill(repo, "a-cat", "zzz-skill", "---\nname: zzz-skill\n---\n\nBody.\n")

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        paths = [s["path"] for s in skills]
        assert paths[0] == "categories/a-cat/zzz-skill"
        assert paths[1] == "categories/z-cat/aaa-skill"

    def test_missing_invoke_defaults_to_hawk_prefix(self, marketplace_env: tuple):
        repo, marketplace = marketplace_env
        _create_skill(
            repo,
            "tools",
            "my-tool",
            "---\nname: my-tool\ndescription: A tool\n---\n\nBody.\n",
        )

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert skills[0]["invoke"] == "/hawk:my-tool"

    def test_name_from_frontmatter_over_directory(self, marketplace_env: tuple):
        """If frontmatter has a name, use it instead of the directory name."""
        repo, marketplace = marketplace_env
        _create_skill(
            repo,
            "tools",
            "my-tool",
            "---\nname: custom-name\ndescription: X\n---\n\nBody.\n",
        )

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert skills[0]["name"] == "custom-name"

    def test_name_falls_back_to_directory_name(self, marketplace_env: tuple):
        """If frontmatter has no name, fall back to the directory name."""
        repo, marketplace = marketplace_env
        _create_skill(
            repo,
            "tools",
            "dir-name",
            "---\ndescription: X\n---\n\nBody.\n",
        )

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert skills[0]["name"] == "dir-name"

    def test_skill_without_skill_md_skipped(self, marketplace_env: tuple):
        """A skill directory without SKILL.md should be skipped."""
        repo, marketplace = marketplace_env
        # Create a category directory with a skill that has no SKILL.md
        skill_dir = repo / "categories" / "empty-cat" / "no-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "README.md").write_text("Not a skill.\n", encoding="utf-8")

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert len(skills) == 0

    def test_non_directory_files_in_categories_ignored(self, marketplace_env: tuple):
        """Regular files in categories/ should be ignored, not treated as categories."""
        repo, marketplace = marketplace_env
        # Put a file (not a directory) in categories/
        (repo / "categories" / "README.md").write_text("Categories readme.\n", encoding="utf-8")
        _create_skill(
            repo,
            "real-cat",
            "real-skill",
            "---\nname: real-skill\n---\n\nBody.\n",
        )

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        skills = data["plugins"][0]["skills"]
        assert len(skills) == 1
        assert skills[0]["name"] == "real-skill"

    def test_empty_categories_produces_empty_skills(self, marketplace_env: tuple):
        """With no skills, the marketplace should have an empty skills array."""
        repo, marketplace = marketplace_env

        with (
            patch("sync_marketplace.CATEGORIES_DIR", repo / "categories"),
            patch("sync_marketplace.MARKETPLACE", marketplace),
            patch("sync_marketplace.REPO_ROOT", repo),
        ):
            main()

        data = json.loads(marketplace.read_text())
        assert data["plugins"][0]["skills"] == []
