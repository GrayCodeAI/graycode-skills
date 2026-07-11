"""Tests for tools/check_changed_scripts.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from check_changed_scripts import changed_tls_docs, find_insecure_tls, main


def test_changed_tls_docs_includes_markdown_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    doc = Path("categories/example/SKILL.md")
    doc.parent.mkdir(parents=True)
    doc.write_text("# Skill\n", encoding="utf-8")

    paths = ["categories/example/SKILL.md", "categories/example/scripts/agent.py"]
    assert changed_tls_docs(paths) == [doc]


def test_find_insecure_tls_reports_markdown_examples(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    doc = Path("categories/example/SKILL.md")
    doc.parent.mkdir(parents=True)
    doc.write_text("requests.get(url, verify=False)\n", encoding="utf-8")

    findings = find_insecure_tls([doc])
    assert findings == [f"{doc}:1: do not disable TLS certificate verification"]


def test_main_accepts_doc_only_changes_without_python_lint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.chdir(tmp_path)
    doc = Path("categories/example/SKILL.md")
    doc.parent.mkdir(parents=True)
    doc.write_text("# Safe Skill\nrequests.get(url, verify=True)\n", encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["check_changed_scripts.py", str(doc)])
    assert main() == 0
