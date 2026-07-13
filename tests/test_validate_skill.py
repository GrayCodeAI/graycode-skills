"""Tests for tools/validate_skill.py."""

from __future__ import annotations

# Add tools/ to path so we can import the module under test
import json
import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from frontmatter import parse_frontmatter
from validate_skill import (
    TAG_PATTERN,
    WARNING_CATEGORIES,
    ValidationResult,
    compare_warning_budget,
    find_all_skills,
    load_warning_budget,
    main,
    path_exists_with_exact_case,
    validate_skill,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def skill_dir(tmp_path: Path) -> Path:
    """Create a minimal valid skill directory."""
    d = tmp_path / "test-skill"
    d.mkdir()
    (d / "SKILL.md").write_text(
        textwrap.dedent("""\
        ---
        name: test-skill
        description: A test skill
        license: MIT
        tags: [testing, example]
        ---

        # Test Skill

        ## Overview

        This is a test skill for unit testing.

        ## Instructions

        Do the thing.
        """),
        encoding="utf-8",
    )
    return d


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = "---\nname: foo\ndescription: bar\n---\n\nBody here"
        fm, body = parse_frontmatter(content)
        assert fm == {"name": "foo", "description": "bar"}
        assert "Body here" in body

    def test_no_frontmatter(self):
        content = "# Just a heading\n\nNo frontmatter"
        fm, body = parse_frontmatter(content)
        assert fm is None
        assert body == content

    def test_malformed_yaml(self):
        content = "---\n: invalid: yaml: [[[\n---\nBody"
        fm, body = parse_frontmatter(content)
        assert fm is None

    def test_empty_frontmatter(self):
        content = "---\n---\nBody"
        fm, body = parse_frontmatter(content)
        # Empty YAML parses as None, not a dict
        assert fm is None

    def test_frontmatter_with_multiline_body(self):
        content = "---\nname: x\n---\n\nLine 1\n\nLine 2\n\nLine 3"
        fm, body = parse_frontmatter(content)
        assert fm == {"name": "x"}
        assert "Line 1" in body
        assert "Line 3" in body


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------


class TestValidationResult:
    def test_passed_when_no_errors(self, tmp_path: Path):
        r = ValidationResult(tmp_path)
        assert r.passed is True
        assert r.errors == []
        assert r.warnings == []

    def test_failed_when_errors(self, tmp_path: Path):
        r = ValidationResult(tmp_path)
        r.error("something broke")
        assert r.passed is False
        assert len(r.errors) == 1

    def test_warnings_d_not_affect_pass(self, tmp_path: Path):
        r = ValidationResult(tmp_path)
        r.warn("just a warning")
        assert r.passed is True
        assert len(r.warnings) == 1
        assert r.warning_counts == {"uncategorized": 1}

    def test_warning_category_is_recorded(self, tmp_path: Path):
        r = ValidationResult(tmp_path)
        r.warn("broken", category="broken-internal-reference")
        assert r.warning_counts == {"broken-internal-reference": 1}

    def test_unknown_warning_category_is_rejected(self, tmp_path: Path):
        r = ValidationResult(tmp_path)
        with pytest.raises(ValueError, match="unknown warning category"):
            r.warn("broken", category="new-unbudgeted-category")


# ---------------------------------------------------------------------------
# Warning budget ratchet
# ---------------------------------------------------------------------------


class TestWarningBudget:
    @pytest.fixture
    def budget(self) -> dict[str, int]:
        return {category: 0 for category in WARNING_CATEGORIES}

    def test_exact_budget_matches(self, budget: dict[str, int]):
        budget["broken-internal-reference"] = 3
        assert compare_warning_budget(budget, budget) == []

    def test_growth_fails(self, budget: dict[str, int]):
        actual = dict(budget)
        actual["too-many-tags"] = 1
        differences = compare_warning_budget(actual, budget)
        assert differences == ["too-many-tags: 1 warnings exceeds the checked-in budget of 0"]

    def test_reduction_requires_ratchet_update(self, budget: dict[str, int]):
        budget["script-not-executable"] = 2
        differences = compare_warning_budget({}, budget)
        assert differences == [
            "script-not-executable: 0 warnings is below the checked-in budget of 2; "
            "lower the budget to lock in the improvement"
        ]

    def test_load_budget_rejects_missing_category(self, tmp_path: Path, budget: dict[str, int]):
        budget.pop("uncategorized")
        path = tmp_path / "budget.json"
        path.write_text(json.dumps(budget), encoding="utf-8")
        with pytest.raises(ValueError, match="missing categories: uncategorized"):
            load_warning_budget(path)

    def test_load_budget_rejects_unknown_category(self, tmp_path: Path, budget: dict[str, int]):
        budget["mystery"] = 1
        path = tmp_path / "budget.json"
        path.write_text(json.dumps(budget), encoding="utf-8")
        with pytest.raises(ValueError, match="unknown categories: mystery"):
            load_warning_budget(path)

    @pytest.mark.parametrize("invalid", [-1, 1.5, True, "1"])
    def test_load_budget_rejects_invalid_count(
        self, tmp_path: Path, budget: dict[str, int], invalid: object
    ):
        budget["uncategorized"] = invalid
        path = tmp_path / "budget.json"
        path.write_text(json.dumps(budget), encoding="utf-8")
        with pytest.raises(ValueError, match="must be a non-negative integer"):
            load_warning_budget(path)


class TestWarningBudgetCli:
    @staticmethod
    def write_budget(path: Path, **overrides: int) -> None:
        budget = {category: 0 for category in WARNING_CATEGORIES}
        budget.update(overrides)
        path.write_text(json.dumps(budget), encoding="utf-8")

    def test_matching_budget_passes(
        self,
        skill_dir: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ):
        budget_path = tmp_path / "budget.json"
        self.write_budget(budget_path)
        monkeypatch.setattr("validate_skill.find_all_skills", lambda: [skill_dir])
        monkeypatch.setattr(
            sys,
            "argv",
            ["validate_skill.py", "--all", "--warning-budget", str(budget_path)],
        )

        main()

        output = capsys.readouterr().out
        assert "Warning budget matches the checked-in baseline." in output
        assert "TOTAL" in output

    def test_warning_growth_fails(
        self,
        skill_dir: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ):
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        (skill_dir / "SKILL.md").write_text(
            content.replace("tags: [testing, example]", "tags: [one, two, three, four, five, six]"),
            encoding="utf-8",
        )
        budget_path = tmp_path / "budget.json"
        self.write_budget(budget_path)
        monkeypatch.setattr("validate_skill.find_all_skills", lambda: [skill_dir])
        monkeypatch.setattr(
            sys,
            "argv",
            ["validate_skill.py", "--all", "--warning-budget", str(budget_path)],
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        assert "too-many-tags: 1 warnings exceeds" in capsys.readouterr().out

    def test_warning_reduction_requires_baseline_update(
        self,
        skill_dir: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ):
        budget_path = tmp_path / "budget.json"
        self.write_budget(budget_path, **{"script-not-executable": 1})
        monkeypatch.setattr("validate_skill.find_all_skills", lambda: [skill_dir])
        monkeypatch.setattr(
            sys,
            "argv",
            ["validate_skill.py", "--all", "--warning-budget", str(budget_path)],
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        output = capsys.readouterr().out
        assert "script-not-executable: 0 warnings is below" in output
        assert "the budget to lock in the improvement" in output


# ---------------------------------------------------------------------------
# validate_skill - happy path
# ---------------------------------------------------------------------------


class TestValidateSkill:
    def test_valid_skill_passes(self, skill_dir: Path):
        result = validate_skill(skill_dir)
        assert result.passed is True
        assert result.errors == []

    def test_missing_skill_md(self, tmp_path: Path):
        d = tmp_path / "empty-skill"
        d.mkdir()
        result = validate_skill(d)
        assert result.passed is False
        assert any("SKILL.md not found" in e for e in result.errors)

    def test_no_frontmatter(self, tmp_path: Path):
        d = tmp_path / "no-fm"
        d.mkdir()
        (d / "SKILL.md").write_text(
            "# Just a heading\n\nSome body text without frontmatter.\n", encoding="utf-8"
        )
        result = validate_skill(d)
        assert result.passed is False
        assert any("no valid YAML frontmatter" in e for e in result.errors)

    def test_missing_required_fields(self, tmp_path: Path):
        d = tmp_path / "missing-fields"
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: missing-fields\n---\n\nBody\n", encoding="utf-8")
        result = validate_skill(d)
        assert result.passed is False
        error_text = " ".join(result.errors)
        assert "description" in error_text
        assert "license" in error_text

    def test_name_mismatch(self, tmp_path: Path):
        d = tmp_path / "dir-name"
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: different-name\ndescription: x\nlicense: MIT\ntags: [a]\n---\n\nBody\n",
            encoding="utf-8",
        )
        result = validate_skill(d)
        assert any("does not match directory name" in e for e in result.errors)

    def test_description_too_long(self, skill_dir: Path):
        long_desc = "x" * 250
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: test-skill\ndescription: {long_desc}\nlicense: MIT\ntags: [a]\n---\n\nBody\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert any("250 chars" in w for w in result.warnings)

    def test_no_tags(self, tmp_path: Path):
        d = tmp_path / "no-tags"
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: no-tags\ndescription: x\nlicense: MIT\ntags: []\n---\n\nBody\n",
            encoding="utf-8",
        )
        result = validate_skill(d)
        assert any("at least 1 tag" in e for e in result.errors)

    def test_invalid_tag_format(self, tmp_path: Path):
        d = tmp_path / "bad-tags"
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: bad-tags\ndescription: x\nlicense: MIT\ntags: [Bad_Tag!]\n---\n\nBody\n",
            encoding="utf-8",
        )
        result = validate_skill(d)
        assert any("invalid" in e.lower() for e in result.errors)

    def test_broken_internal_link(self, skill_dir: Path):
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nSee [broken](nonexistent.md) for details.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert any("Broken internal reference" in w for w in result.warnings)

    def test_script_missing_shebang(self, skill_dir: Path):
        scripts = skill_dir / "scripts"
        scripts.mkdir()
        script = scripts / "run.sh"
        script.write_text("echo hello\n", encoding="utf-8")
        script.chmod(0o755)
        result = validate_skill(skill_dir)
        assert any("missing shebang" in w for w in result.warnings)

    def test_script_not_executable(self, skill_dir: Path):
        scripts = skill_dir / "scripts"
        scripts.mkdir()
        script = scripts / "run.py"
        script.write_text("#!/usr/bin/env python3\nprint('hi')\n", encoding="utf-8")
        script.chmod(0o644)
        result = validate_skill(skill_dir)
        assert any("not executable" in w for w in result.warnings)

    def test_utf8_error(self, tmp_path: Path):
        d = tmp_path / "bad-encoding"
        d.mkdir()
        skill_md = d / "SKILL.md"
        skill_md.write_bytes(b"\x80\x81\x82\x83")
        result = validate_skill(d)
        assert any("UTF-8" in e for e in result.errors)


# ---------------------------------------------------------------------------
# TAG_PATTERN regex
# ---------------------------------------------------------------------------


class TestTagPattern:
    @pytest.mark.parametrize(
        "tag",
        ["python", "ai-ml", "web3", "a", "my-cool-tag"],
    )
    def test_valid_tags(self, tag: str):
        assert TAG_PATTERN.match(tag), f"Expected '{tag}' to be valid"

    @pytest.mark.parametrize(
        "tag",
        ["Python", "AI_ML", "-bad", "bad-", "1bad", "has space", "UPPER", ""],
    )
    def test_invalid_tags(self, tag: str):
        assert not TAG_PATTERN.match(tag), f"Expected '{tag}' to be invalid"


# ---------------------------------------------------------------------------
# find_all_skills
# ---------------------------------------------------------------------------


class TestFindAllSkills:
    def test_finds_skills_in_categories(self, tmp_path: Path):
        """Simulate categories/<cat>/<skill>/SKILL.md layout."""
        import validate_skill as vs

        original = vs.CATEGORIES_DIR
        try:
            cats = tmp_path / "categories"
            cats.mkdir()
            cat = cats / "python"
            cat.mkdir()
            skill = cat / "my-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: x\n---\n\nBody\n", encoding="utf-8")
            vs.CATEGORIES_DIR = cats

            found = find_all_skills()
            assert len(found) == 1
            assert found[0].name == "my-skill"
        finally:
            vs.CATEGORIES_DIR = original

    def test_empty_categories(self, tmp_path: Path):
        import validate_skill as vs

        original = vs.CATEGORIES_DIR
        try:
            cats = tmp_path / "empty-cats"
            cats.mkdir()
            vs.CATEGORIES_DIR = cats
            assert find_all_skills() == []
        finally:
            vs.CATEGORIES_DIR = original


# ---------------------------------------------------------------------------
# Markdown internal-reference scanning
# ---------------------------------------------------------------------------


class TestMarkdownInternalReferences:
    @staticmethod
    def write_body(skill_dir: Path, body: str, *, description: str = "A test skill") -> None:
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
                f"""\
                ---
                name: test-skill
                description: {description}
                license: MIT
                tags: [testing]
                ---

                {body}
                """
            ),
            encoding="utf-8",
        )

    def test_code_examples_and_escaped_syntax_are_not_links(self, skill_dir: Path):
        self.write_body(
            skill_dir,
            r"""
            # Examples

            ```markdown
            [fenced](missing-fenced.md)
            [escape](../outside-fence.md)
            ```

            ~~~~text
            [tilde fenced](missing-tilde.md)
            ~~~~

            `[inline](missing-inline.md)` and
            ``[inline with `](missing-inline-two.md)`` and
            \[escaped](missing-escaped.md) are examples.

            [real](missing-real.md) is a dependency.
            """,
        )

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 1
        assert result.warning_counts["path-traversal"] == 0
        assert result.warnings == ["SKILL.md: Broken internal reference: [real](missing-real.md)"]

    def test_even_backslash_prefix_does_not_escape_a_real_link(self, skill_dir: Path):
        self.write_body(skill_dir, r"Two slashes \\[real](missing.md) still precede a link.")

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 1

    def test_inline_code_in_real_link_label_is_preserved_in_warning(self, skill_dir: Path):
        self.write_body(skill_dir, "Read [the `guide`](missing.md).")

        result = validate_skill(skill_dir)

        assert result.warnings == ["SKILL.md: Broken internal reference: [the `guide`](missing.md)"]

    def test_invalid_escape_does_not_turn_whitespace_into_a_path(self, skill_dir: Path):
        self.write_body(skill_dir, r"This is not a link: [guide](docs/My\ Guide.md).")

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 0

    def test_frontmatter_link_like_text_is_not_a_body_dependency(self, skill_dir: Path):
        self.write_body(
            skill_dir,
            "# No body links",
            description='"Example syntax: [label](missing.md)"',
        )

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 0

    def test_uri_anchor_and_same_document_targets_are_skipped(self, skill_dir: Path):
        self.write_body(
            skill_dir,
            """
            [HTTPS](HTTPS://example.com/docs?q=1#part)
            [email](MAILTO:maintainer@example.com)
            [custom](vscode://example/resource)
            [cdn](//cdn.example.com/asset.png)
            [anchor](#overview)
            [query](?view=raw#overview)
            [empty]()
            """,
        )

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 0
        assert result.warning_counts["path-traversal"] == 0

    def test_query_fragment_titles_and_encoded_paths_preserve_real_checks(self, skill_dir: Path):
        docs = skill_dir / "docs"
        docs.mkdir()
        (docs / "Guide (v1).md").write_text("# Guide\n", encoding="utf-8")
        self.write_body(
            skill_dir,
            """
            [encoded](docs/Guide%20%28v1%29.md?raw=1#overview "Guide title")
            [angle](<docs/Guide (v1).md#overview> 'Guide title')
            ![asset](docs/Guide%20%28v1%29.md?download=1)
            """,
        )

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 0
        assert result.warning_counts["path-traversal"] == 0

    def test_query_fragment_does_not_hide_missing_or_wrong_case_path(self, skill_dir: Path):
        docs = skill_dir / "docs"
        docs.mkdir()
        (docs / "Guide.md").write_text("# Guide\n", encoding="utf-8")
        self.write_body(
            skill_dir,
            """
            [missing](docs/missing.md?raw=1#overview)
            [wrong case](docs/guide.md?raw=1#overview)
            """,
        )

        result = validate_skill(skill_dir)

        assert result.warning_counts["broken-internal-reference"] == 2

    def test_optional_title_is_not_part_of_missing_path(self, skill_dir: Path):
        self.write_body(skill_dir, '[missing](docs/missing.md "Human title")')

        result = validate_skill(skill_dir)

        assert result.warnings == [
            "SKILL.md: Broken internal reference: [missing](docs/missing.md)"
        ]

    def test_nested_markdown_links_resolve_from_their_source_directory(self, skill_dir: Path):
        references = skill_dir / "references"
        references.mkdir()
        assets = skill_dir / "assets"
        assets.mkdir()
        (assets / "sample.txt").write_text("sample\n", encoding="utf-8")
        (references / "guide.md").write_text(
            "[skill](../SKILL.md)\n"
            "[asset](../assets/sample.txt)\n"
            "[missing](missing.md?raw=1#example)\n",
            encoding="utf-8",
        )

        result = validate_skill(skill_dir)

        assert result.warnings == [
            "references/guide.md: Broken internal reference: [missing](missing.md?raw=1#example)"
        ]

    def test_nested_markdown_traversal_is_bounded_by_skill_root(self, skill_dir: Path):
        nested = skill_dir / "references" / "nested"
        nested.mkdir(parents=True)
        (nested / "guide.md").write_text(
            "[outside](../../../outside.md#example)\n", encoding="utf-8"
        )

        result = validate_skill(skill_dir)

        assert result.warnings == [
            "references/nested/guide.md: Path traversal detected: "
            "[outside](../../../outside.md#example) resolves outside skill directory"
        ]

    def test_markdown_sources_and_warnings_are_deterministically_ordered(self, skill_dir: Path):
        self.write_body(skill_dir, "[skill missing](skill-missing.md)")
        references = skill_dir / "references"
        references.mkdir()
        (references / "z.md").write_text("[z](z-missing.md)\n", encoding="utf-8")
        (references / "a.md").write_text("[a](a-missing.md)\n", encoding="utf-8")

        result = validate_skill(skill_dir)

        assert result.warnings == [
            "SKILL.md: Broken internal reference: [skill missing](skill-missing.md)",
            "references/a.md: Broken internal reference: [a](a-missing.md)",
            "references/z.md: Broken internal reference: [z](z-missing.md)",
        ]

    def test_markdown_source_symlink_cannot_escape_skill_root(
        self, skill_dir: Path, tmp_path: Path
    ):
        outside = tmp_path / "outside.md"
        outside.write_text("[external content](not-inside-skill.md)\n", encoding="utf-8")
        references = skill_dir / "references"
        references.mkdir()
        link = references / "outside.md"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            pytest.skip(f"symlinks are unavailable: {exc}")

        result = validate_skill(skill_dir)

        assert result.warning_counts["path-traversal"] == 1
        assert result.warning_counts["broken-internal-reference"] == 0
        assert result.warnings == [
            "references/outside.md: Markdown source resolves outside skill directory"
        ]

    def test_link_target_symlink_cannot_escape_skill_root(self, skill_dir: Path, tmp_path: Path):
        outside = tmp_path / "outside.txt"
        outside.write_text("external\n", encoding="utf-8")
        assets = skill_dir / "assets"
        assets.mkdir()
        link = assets / "outside.txt"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            pytest.skip(f"symlinks are unavailable: {exc}")
        self.write_body(skill_dir, "[outside](assets/outside.txt)")

        result = validate_skill(skill_dir)

        assert result.warning_counts["path-traversal"] == 1
        assert result.warnings == [
            "SKILL.md: Path traversal detected: [outside](assets/outside.txt) "
            "resolves outside skill directory"
        ]

    def test_nested_markdown_keeps_exact_case_checks(self, skill_dir: Path):
        references = skill_dir / "references"
        references.mkdir()
        (references / "Guide.md").write_text("# Guide\n", encoding="utf-8")
        (references / "index.md").write_text("[guide](guide.md)\n", encoding="utf-8")

        result = validate_skill(skill_dir)

        assert result.warnings == [
            "references/index.md: Broken internal reference: [guide](guide.md)"
        ]

    def test_encoded_and_windows_style_traversal_are_detected(self, skill_dir: Path):
        self.write_body(
            skill_dir,
            r"""
            [encoded](%2e%2e/secrets.md?raw=1#token)
            [windows](..\secrets.md#token)
            """,
        )

        result = validate_skill(skill_dir)

        assert result.warning_counts["path-traversal"] == 2
        assert result.warning_counts["broken-internal-reference"] == 0


# ---------------------------------------------------------------------------
# Path traversal detection
# ---------------------------------------------------------------------------


class TestPathTraversal:
    def test_relative_traversal_detected(self, skill_dir: Path):
        """A link like [x](../../etc/passwd) that resolves outside the skill dir should warn."""
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nSee [secret](../../../etc/passwd) for details.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert any("Path traversal" in w for w in result.warnings)

    def test_dotdot_escape_detected(self, skill_dir: Path):
        """A link like [x](../../other-skill/file.md) that escapes the skill root should warn."""
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nSee [other](../../other-skill/SKILL.md) for info.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert any("Path traversal" in w for w in result.warnings)

    def test_internal_link_within_skill_ok(self, skill_dir: Path):
        """A link to a file that exists inside the skill directory should not warn."""
        subdir = skill_dir / "docs"
        subdir.mkdir()
        (subdir / "guide.md").write_text("# Guide\n\nHello.\n", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nSee [guide](docs/guide.md) for details.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        # Should not have a path traversal warning
        assert not any("Path traversal" in w for w in result.warnings)

    def test_internal_link_case_must_match_on_all_filesystems(self, skill_dir: Path):
        docs = skill_dir / "docs"
        docs.mkdir()
        guide = docs / "Guide.md"
        guide.write_text("# Guide\n", encoding="utf-8")
        assert path_exists_with_exact_case(guide, skill_dir.resolve())
        assert not path_exists_with_exact_case(docs / "guide.md", skill_dir.resolve())

        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nSee [guide](docs/guide.md) for details.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert any("Broken internal reference" in warning for warning in result.warnings)

    def test_external_url_not_flagged(self, skill_dir: Path):
        """External URLs (http/https) should not be checked for path traversal."""
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nSee [example](https://example.com) for details.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert not any("Path traversal" in w for w in result.warnings)

    def test_mailto_link_not_flagged(self, skill_dir: Path):
        """mailto: links should not be checked for path traversal."""
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nContact [us](mailto:admin@example.com).\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert not any("Path traversal" in w for w in result.warnings)

    def test_anchor_link_not_flagged(self, skill_dir: Path):
        """Anchor links (#section) should not be checked for path traversal."""
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test\nlicense: MIT\ntags: [a]\n---\n\n"
            "# Test\n\nJump to [section](#overview).\n\n## Overview\n\nHere.\n",
            encoding="utf-8",
        )
        result = validate_skill(skill_dir)
        assert not any("Path traversal" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# File size validation
# ---------------------------------------------------------------------------


class TestFileSize:
    def test_large_non_asset_warns(self, skill_dir: Path):
        """A non-asset file exceeding 100KB should produce a warning."""
        large_content = "# Skill\n\n" + "x" * (100 * 1024 + 1)
        (skill_dir / "README.md").write_text(large_content, encoding="utf-8")
        result = validate_skill(skill_dir)
        assert any("exceeds 100KB" in w for w in result.warnings)

    def test_asset_file_not_warned(self, skill_dir: Path):
        """Asset files (e.g. .png) exceeding 100KB should not warn."""
        large_asset = b"\x00" * (100 * 1024 + 1)
        (skill_dir / "screenshot.png").write_bytes(large_asset)
        result = validate_skill(skill_dir)
        assert not any("exceeds 100KB" in w for w in result.warnings)
