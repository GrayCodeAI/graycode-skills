"""Tests for tools/bump_version.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from bump_version import bump


@pytest.mark.parametrize(
    "version,part,expected",
    [
        ("1.2.3", "patch", "1.2.4"),
        ("1.2.3", "minor", "1.3.0"),
        ("1.2.3", "major", "2.0.0"),
        ("0.0.0", "patch", "0.0.1"),
        ("0.0.0", "minor", "0.1.0"),
        ("0.0.0", "major", "1.0.0"),
    ],
)
def test_bump_three_segment(version, part, expected):
    assert bump(version, part) == expected


@pytest.mark.parametrize(
    "version,part,expected",
    [
        ("1.0", "patch", "1.0.1"),
        ("1.0", "minor", "1.1.0"),
        ("1.0", "major", "2.0.0"),
        ("1", "patch", "1.0.1"),
        ("1", "minor", "1.1.0"),
        ("1", "major", "2.0.0"),
        ("10.20", "patch", "10.20.1"),
    ],
)
def test_bump_short_version_does_not_crash(version, part, expected):
    # Two-segment and one-segment versions must not raise ValueError.
    assert bump(version, part) == expected
