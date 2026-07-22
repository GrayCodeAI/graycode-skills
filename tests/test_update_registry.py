"""Tests for tools/update_registry.py - registry building from skill directories."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Patch sys.path so we can import the module under test.
TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

# ---------------------------------------------------------------------------
# IMPORTANT: update_registry.py imports parse_frontmatter from frontmatter.py,
# which returns (dict | None, str). update_registry.py unpacks the tuple.
# We monkeypatch the module-level reference to return a tuple, matching
# the interface the code now uses.
# ---------------------------------------------------------------------------


# Import the module fresh so we can patch its parse_frontmatter reference.
import update_registry as _mod  # noqa: E402


def _make_parse_frontmatter_return_tuple(content: str) -> tuple[dict[str, Any] | None, str]:
    """Thin wrapper around the real parse_frontmatter that returns a
    (dict | None, body) tuple, matching the interface update_registry.py
    uses after the bug fix."""
    from frontmatter import parse_frontmatter as _real

    return _real(content)


@pytest.fixture(autouse=True)
def _patch_parse_frontmatter(monkeypatch: pytest.MonkeyPatch):
    """Replace parse_frontmatter inside update_registry with a version that
    returns the real (dict | None, body) tuple."""
    monkeypatch.setattr(_mod, "parse_frontmatter", _make_parse_frontmatter_return_tuple)


# ---------------------------------------------------------------------------
# Helpers for building fake skill directory trees
# ---------------------------------------------------------------------------


def _write_skill(
    base: Path,
    category: str,
    skill_name: str,
    *,
    frontmatter: str | None = None,
    extra_files: list[str] | None = None,
    scripts: list[str] | None = None,
) -> Path:
    """Create a minimal skill directory with a SKILL.md and optional extras.

    Returns the skill directory path.
    """
    skill_dir = base / "categories" / category / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    if frontmatter is None:
        frontmatter = (
            "---\n"
            f"name: {skill_name}\n"
            f'description: "A test skill"\n'
            f"tags: [test]\n"
            "---\n"
            "\n"
            "# Skill\n"
            "Body text.\n"
        )
    (skill_dir / "SKILL.md").write_text(frontmatter, encoding="utf-8")

    for f in extra_files or []:
        (skill_dir / f).parent.mkdir(parents=True, exist_ok=True)
        (skill_dir / f).write_text("content", encoding="utf-8")

    if scripts is not None:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        for s in scripts:
            (scripts_dir / s).write_text("#!/bin/bash\necho hi\n", encoding="utf-8")

    return skill_dir


# ===================================================================
# count_files
# ===================================================================


class TestCountFiles:
    def test_empty_directory(self, tmp_path: Path):
        d = tmp_path / "empty"
        d.mkdir()
        assert _mod.count_files(d) == 0

    def test_single_file(self, tmp_path: Path):
        (tmp_path / "a.txt").write_text("x")
        assert _mod.count_files(tmp_path) == 1

    def test_nested_files(self, tmp_path: Path):
        (tmp_path / "a.txt").write_text("x")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "b.txt").write_text("y")
        (sub / "c.txt").write_text("z")
        # Recursive count: a.txt + b.txt + c.txt = 3, but count_files counts
        # files in subdirectories too.  os.walk yields (dirpath, dirnames,
        # filenames) and we sum len(filenames) across all levels.
        assert _mod.count_files(tmp_path) == 3

    def test_ignores_directories(self, tmp_path: Path):
        """Only files are counted, not subdirectories themselves."""
        (tmp_path / "file.txt").write_text("x")
        (tmp_path / "subdir").mkdir()
        assert _mod.count_files(tmp_path) == 1


# ===================================================================
# has_scripts_dir
# ===================================================================


class TestHasScriptsDir:
    def test_no_scripts_dir(self, tmp_path: Path):
        assert _mod.has_scripts_dir(tmp_path) is False

    def test_empty_scripts_dir(self, tmp_path: Path):
        (tmp_path / "scripts").mkdir()
        assert _mod.has_scripts_dir(tmp_path) is False

    def test_scripts_dir_with_file(self, tmp_path: Path):
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        (scripts / "run.sh").write_text("#!/bin/bash\n")
        assert _mod.has_scripts_dir(tmp_path) is True


# ===================================================================
# build_registry - loading / basic registration
# ===================================================================


class TestRegistryLoading:
    def test_no_categories_dir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """If categories/ does not exist, returns empty list."""
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", tmp_path / "nonexistent")
        assert _mod.build_registry() == []

    def test_empty_categories_dir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Empty categories dir yields no entries."""
        cats = tmp_path / "categories"
        cats.mkdir()
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)
        assert _mod.build_registry() == []

    def test_single_skill(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "ai-ml", "summarizer")

        entries = _mod.build_registry()
        assert len(entries) == 1
        assert entries[0]["name"] == "summarizer"
        assert entries[0]["category"] == "ai-ml"
        assert entries[0]["path"] == "categories/ai-ml/summarizer"

    def test_multiple_skills_across_categories(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "ai-ml", "summarizer")
        _write_skill(tmp_path, "devops", "deployer")

        entries = _mod.build_registry()
        names = [e["name"] for e in entries]
        # Entries are sorted alphabetically by name
        assert "deployer" in names
        assert "summarizer" in names

    def test_sorts_entries_by_name(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "cat", "zebra-skill")
        _write_skill(tmp_path, "cat", "alpha-skill")
        _write_skill(tmp_path, "cat", "middle-skill")

        entries = _mod.build_registry()
        names = [e["name"] for e in entries]
        assert names == sorted(names, key=str.lower)


# ===================================================================
# build_registry - frontmatter extraction
# ===================================================================


class TestSkillRegistration:
    def test_name_from_frontmatter(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm = '---\nname: custom-name\ndescription: "Some desc"\n---\n'
        _write_skill(tmp_path, "cat", "dir-name", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["name"] == "custom-name"

    def test_name_defaults_to_dir_name(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # Frontmatter with no name field
        fm = "---\ndescription: desc\n---\n"
        _write_skill(tmp_path, "cat", "my-dir-name", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["name"] == "my-dir-name"

    def test_description_truncated_to_200_chars(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        long_desc = "word " * 100  # 500 chars
        fm = f"---\nname: x\ndescription: {long_desc}\n---\n"
        _write_skill(tmp_path, "cat", "long-desc-skill", frontmatter=fm)

        entries = _mod.build_registry()
        assert len(entries[0]["description"]) <= 200

    def test_multiline_description_collapsed(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm = '---\nname: multi\ndescription: "line one\nline two\nline three"\n---\n'
        _write_skill(tmp_path, "cat", "multi-skill", frontmatter=fm)

        entries = _mod.build_registry()
        # Multi-line description should have newlines collapsed to spaces
        assert "\n" not in entries[0]["description"]

    def test_file_count_populated(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "cat", "fcount", extra_files=["README.md", "data.json"])

        entries = _mod.build_registry()
        # SKILL.md + README.md + data.json = 3
        assert entries[0]["file_count"] == 3

    def test_has_scripts_true(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "cat", "with-scripts", scripts=["run.sh"])

        entries = _mod.build_registry()
        assert entries[0]["has_scripts"] is True

    def test_has_scripts_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "cat", "no-scripts")

        entries = _mod.build_registry()
        assert entries[0]["has_scripts"] is False

    def test_path_format(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "dev-tools", "linter")

        entries = _mod.build_registry()
        assert entries[0]["path"] == "categories/dev-tools/linter"

    def test_tags_from_frontmatter_list(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm = "---\nname: t\ntags: [python, ml, nlp]\n---\n"
        _write_skill(tmp_path, "cat", "tagged", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["tags"] == ["python", "ml", "nlp"]

    def test_tags_from_comma_separated_string(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm = "---\nname: t\ntags: python, ml, nlp\n---\n"
        _write_skill(tmp_path, "cat", "csv-tags", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["tags"] == ["python", "ml", "nlp"]


# ===================================================================
# Tag generation - default tags for empty tags
# ===================================================================


class TestTagGeneration:
    def test_empty_tags_get_category_default(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # tags: [] explicitly empty
        fm = "---\nname: notags\ntags: []\n---\n"
        _write_skill(tmp_path, "ai-ml", "no-tags-skill", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["tags"] == ["ai-ml"]

    def test_missing_tags_field_gets_category_default(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # No tags field at all
        fm = "---\nname: missingtags\ndescription: desc\n---\n"
        _write_skill(tmp_path, "dev-tools", "missing-tags-skill", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["tags"] == ["dev-tools"]

    def test_category_with_spaces_becomes_hyphenated(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # Create a category directory with a space in name
        fm = "---\nname: spaced\ndescription: desc\ntags: []\n---\n"
        skill_dir = cats / "Cloud Tools" / "spaced"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(fm, encoding="utf-8")

        entries = _mod.build_registry()
        assert entries[0]["tags"] == ["cloud-tools"]

    def test_whitespace_only_tags_in_string_treated_as_empty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # tags: "  ,  , "  -- commas with only whitespace => no real tags
        fm = '---\nname: whitespace\ntags: "  ,  , "\n---\n'
        _write_skill(tmp_path, "my-cat", "ws-tags", frontmatter=fm)

        entries = _mod.build_registry()
        # All stripped tags are empty, so falls back to category
        assert entries[0]["tags"] == ["my-cat"]


# ===================================================================
# Deduplication
# ===================================================================


class TestDeduplication:
    def test_duplicate_names_keeps_first(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm1 = "---\nname: dup-skill\ndescription: first one\ntags: [a]\n---\n"
        fm2 = "---\nname: dup-skill\ndescription: second one\ntags: [b]\n---\n"

        _write_skill(tmp_path, "cat-a", "dup-skill-alpha", frontmatter=fm1)
        _write_skill(tmp_path, "cat-b", "dup-skill-beta", frontmatter=fm2)

        entries = _mod.build_registry()
        # Only one entry with that name should exist
        dupes = [e for e in entries if e["name"] == "dup-skill"]
        assert len(dupes) == 1
        # Should be the first one (cat-a)
        assert dupes[0]["description"] == "first one"
        assert dupes[0]["category"] == "cat-a"

    def test_same_dir_name_different_frontmatter_names(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Two skills with the same directory name but different frontmatter names
        should both be included."""
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm1 = "---\nname: skill-one\ndescription: first\n---\n"
        fm2 = "---\nname: skill-two\ndescription: second\n---\n"

        _write_skill(tmp_path, "cat-a", "my-skill", frontmatter=fm1)
        _write_skill(tmp_path, "cat-b", "my-skill", frontmatter=fm2)

        entries = _mod.build_registry()
        names = [e["name"] for e in entries]
        assert "skill-one" in names
        assert "skill-two" in names
        assert len(entries) == 2


# ===================================================================
# Validation - directories/files without SKILL.md are skipped
# ===================================================================


class TestValidation:
    def test_no_skill_md_skipped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # Create a directory with no SKILL.md
        skill_dir = cats / "cat" / "no-skill-file"
        skill_dir.mkdir(parents=True)
        (skill_dir / "README.md").write_text("# Just a readme\n")

        entries = _mod.build_registry()
        assert len(entries) == 0

    def test_non_directory_in_categories_skipped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        cats.mkdir()
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # A regular file, not a directory, in categories/
        (cats / "a-file.txt").write_text("not a category")

        entries = _mod.build_registry()
        assert entries == []

    def test_non_directory_in_category_skipped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # A regular file inside a category directory
        cat_dir = cats / "my-cat"
        cat_dir.mkdir(parents=True)
        (cat_dir / "random-file.md").write_text("not a skill")

        entries = _mod.build_registry()
        assert entries == []

    def test_valid_and_invalid_skills_mixed(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        _write_skill(tmp_path, "cat", "valid-skill")

        # Invalid: no SKILL.md
        bad_dir = cats / "cat" / "no-skill-md"
        bad_dir.mkdir(parents=True)
        (bad_dir / "random.txt").write_text("nope")

        entries = _mod.build_registry()
        assert len(entries) == 1
        assert entries[0]["name"] == "valid-skill"


# ===================================================================
# Error handling - malformed input
# ===================================================================


class TestErrorHandling:
    def test_empty_frontmatter_skipped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """A SKILL.md with only '---' delimiters and no YAML content produces
        empty frontmatter; parse_frontmatter returns {} which is falsy? No,
        {} is falsy in Python... wait, actually {} is falsy. Let me check the
        parse_frontmatter logic. If YAML is empty, yaml.safe_load returns None,
        so parse_frontmatter returns (None, body).  update_registry treats None
        as skip."""
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm = "---\n---\n# Just body\n"
        _write_skill(tmp_path, "cat", "empty-fm", frontmatter=fm)

        entries = _mod.build_registry()
        # Should be skipped because parse_frontmatter returns None for empty yaml
        assert len(entries) == 0

    def test_no_frontmatter_skipped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """A SKILL.md with no frontmatter delimiters is skipped."""
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        no_fm = "# Just a heading\n\nSome content, no frontmatter.\n"
        _write_skill(tmp_path, "cat", "no-fm", frontmatter=no_fm)

        entries = _mod.build_registry()
        assert len(entries) == 0

    def test_invalid_yaml_frontmatter_skipped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A SKILL.md with malformed YAML in frontmatter is skipped."""
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        bad_yaml = "---\nname: test\n  bad indent: [unclosed\n---\n"
        _write_skill(tmp_path, "cat", "bad-yaml", frontmatter=bad_yaml)

        entries = _mod.build_registry()
        assert len(entries) == 0

    def test_missing_description_defaults_to_empty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        fm = "---\nname: nodesc\n---\n"
        _write_skill(tmp_path, "cat", "no-desc", frontmatter=fm)

        entries = _mod.build_registry()
        assert entries[0]["description"] == ""

    def test_description_as_non_string(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """If description is not a string (e.g., a number), the code should
        still handle it gracefully."""
        cats = tmp_path / "categories"
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", cats)

        # YAML parses `description: 123` as an integer
        fm = "---\nname: numdesc\ndescription: 123\ntags: [x]\n---\n"
        _write_skill(tmp_path, "cat", "num-desc", frontmatter=fm)

        entries = _mod.build_registry()
        # The code checks isinstance(description, str); for non-string, it
        # should skip the truncation and pass through as-is.
        assert entries[0]["description"] == 123


# ===================================================================
# main() integration
# ===================================================================


class TestMain:
    def _patch_paths(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Patch REPO_ROOT, CATEGORIES_DIR, and REGISTRY_PATH to use tmp_path.
        main() calls REGISTRY_PATH.relative_to(REPO_ROOT) so both must agree."""
        monkeypatch.setattr(_mod, "REPO_ROOT", tmp_path)
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", tmp_path / "categories")
        monkeypatch.setattr(_mod, "REGISTRY_PATH", tmp_path / "registry.json")

    def test_main_exits_cleanly_with_no_skills(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """main() should sys.exit(0) when no skills found."""
        monkeypatch.setattr(_mod, "REPO_ROOT", tmp_path)
        monkeypatch.setattr(_mod, "CATEGORIES_DIR", tmp_path / "nope")
        monkeypatch.setattr(_mod, "REGISTRY_PATH", tmp_path / "registry.json")

        with pytest.raises(SystemExit) as exc_info:
            _mod.main()
        assert exc_info.value.code == 0

    def test_main_writes_registry_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """main() should write a valid JSON file with skill entries."""
        self._patch_paths(tmp_path, monkeypatch)

        _write_skill(tmp_path, "cat", "test-skill")

        _mod.main()

        registry_path = tmp_path / "registry.json"
        assert registry_path.exists()
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "test-skill"

    def test_main_registry_ends_with_newline(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """The written JSON file should end with a trailing newline."""
        self._patch_paths(tmp_path, monkeypatch)

        _write_skill(tmp_path, "cat", "nl-skill")

        _mod.main()

        content = (tmp_path / "registry.json").read_text(encoding="utf-8")
        assert content.endswith("\n")

    def test_main_json_is_pretty_printed(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """The written JSON should be indented (pretty-printed)."""
        self._patch_paths(tmp_path, monkeypatch)

        _write_skill(tmp_path, "cat", "pretty-skill")

        _mod.main()

        content = (tmp_path / "registry.json").read_text(encoding="utf-8")
        # indent=2 means the JSON should contain newlines with 2-space indents
        assert "\n  " in content

    def test_check_succeeds_without_modifying_current_registry(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._patch_paths(tmp_path, monkeypatch)
        _write_skill(tmp_path, "cat", "current-skill")
        expected = _mod.render_registry(_mod.build_registry())
        registry_path = tmp_path / "registry.json"
        registry_path.write_text(expected, encoding="utf-8")

        _mod.main(["--check"])

        assert registry_path.read_text(encoding="utf-8") == expected

    def test_check_rejects_stale_registry_without_modifying_it(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._patch_paths(tmp_path, monkeypatch)
        _write_skill(tmp_path, "cat", "new-skill")
        registry_path = tmp_path / "registry.json"
        stale = "[]\n"
        registry_path.write_text(stale, encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            _mod.main(["--check"])

        assert exc_info.value.code == 1
        assert registry_path.read_text(encoding="utf-8") == stale

    def test_check_creates_missing_registry_and_passes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._patch_paths(tmp_path, monkeypatch)
        _write_skill(tmp_path, "cat", "unregistered-skill")
        registry_path = tmp_path / "registry.json"

        # When registry.json is missing, --check regenerates it (so the next
        # run can diff against a real baseline) and still reports success.
        _mod.main(["--check"])

        assert registry_path.exists()

    def test_check_rejects_empty_skill_corpus_without_modifying_registry(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._patch_paths(tmp_path, monkeypatch)
        registry_path = tmp_path / "registry.json"
        original = '[{"name": "existing"}]\n'
        registry_path.write_text(original, encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            _mod.main(["--check"])

        assert exc_info.value.code == 1
        assert registry_path.read_text(encoding="utf-8") == original
