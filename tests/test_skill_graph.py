"""Tests for the public community-skill graph projection."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import skill_graph

NOW = "2026-07-25T12:00:00Z"


def _entries() -> list[dict]:
    return [
        {
            "name": "python-test",
            "description": "Test Python projects",
            "category": "python",
            "tags": ["testing", "python"],
            "path": "categories/python/python-test",
            "file_count": 2,
            "has_scripts": True,
        },
        {
            "name": "api-review",
            "description": "Review API contracts",
            "category": "quality",
            "tags": ["testing"],
            "path": "categories/quality/api-review",
            "file_count": 1,
            "has_scripts": False,
        },
    ]


def test_build_skill_graph_has_stable_topology():
    first = skill_graph.build_skill_graph(_entries(), generated_at=NOW, version="0.1.0")
    second = skill_graph.build_skill_graph(
        list(reversed(_entries())), generated_at=NOW, version="0.1.0"
    )

    assert first == second
    assert first["schema_version"] == "community-skills.graph/v1"
    assert len(first["events"]) == 1

    node_by_id = {node["id"]: node for node in first["nodes"]}
    assert len(node_by_id) == len(first["nodes"])
    assert {
        node["attributes"]["entity"] for node in first["nodes"] if "entity" in node["attributes"]
    } == {"category", "skill", "tag"}

    for edge in first["edges"]:
        assert edge["from"]["id"] in node_by_id
        assert edge["to"]["id"] in node_by_id
        assert node_by_id[edge["from"]["id"]]["kind"] == edge["from"]["kind"]
        assert node_by_id[edge["to"]["id"]]["kind"] == edge["to"]["kind"]

    event = first["events"][0]
    assert event["subject"]["id"] in node_by_id
    assert event["idempotency_key"] == first["query_sha256"]


def test_build_skill_graph_limit_is_deterministic():
    graph = skill_graph.build_skill_graph(_entries(), generated_at=NOW, version="0.1.0", limit=1)
    skill_nodes = [node for node in graph["nodes"] if node["attributes"].get("entity") == "skill"]
    assert [node["attributes"]["name"] for node in skill_nodes] == ["api-review"]


def test_build_skill_graph_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="limit"):
        skill_graph.build_skill_graph(_entries(), generated_at=NOW, version="0.1.0", limit=-1)

    invalid = _entries()
    invalid[0]["name"] = "bad skill name"
    with pytest.raises(ValueError, match="invalid registry entries"):
        skill_graph.build_skill_graph(invalid, generated_at=NOW, version="0.1.0")


def test_main_writes_graph(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    output = tmp_path / "skill-graph.json"
    monkeypatch.setattr(skill_graph, "build_registry", _entries)
    monkeypatch.setattr(skill_graph, "REPO_ROOT", tmp_path)
    (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")

    assert skill_graph.main(["--output", str(output), "--limit", "1", "--generated-at", NOW]) == 0
    graph = json.loads(output.read_text(encoding="utf-8"))
    assert graph["generated_at"] == NOW
    assert graph["nodes"][0]["provenance"]["version"] == "9.9.9"
