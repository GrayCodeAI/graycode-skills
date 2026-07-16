"""Tests for tools/sandbox_run_changed_scripts.py.

Real Docker execution was verified manually against the corpus during
development (see the module docstring) — these tests cover the
command-construction and pass/fail-classification logic in isolation,
without requiring Docker to be installed/running in the test environment.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from sandbox_run_changed_scripts import (
    TIMEOUT_EXIT_CODE,
    ScriptResult,
    classify,
    has_main_block,
    last_stderr_line,
    sandbox_command,
)


def write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


class TestHasMainBlock:
    def test_detects_dunder_main(self, tmp_path: Path):
        f = write(tmp_path, "agent.py", "def main(): pass\nif __name__ == '__main__':\n    main()\n")
        assert has_main_block(f)

    def test_absent_when_no_entrypoint(self, tmp_path: Path):
        f = write(tmp_path, "lib.py", "def helper():\n    return 1\n")
        assert not has_main_block(f)


class TestSandboxCommand:
    def test_includes_all_isolation_flags(self, tmp_path: Path):
        script = write(tmp_path, "agent.py", "if __name__ == '__main__':\n    pass\n")
        cmd = sandbox_command(script, "sandbox:test", 20)

        assert cmd[0:3] == ["docker", "run", "--rm"]
        assert "--network=none" in cmd
        assert "--read-only" in cmd
        assert "--cap-drop=ALL" in cmd
        assert "--security-opt=no-new-privileges" in cmd
        assert "1000:1000" in cmd
        assert "sandbox:test" in cmd
        assert cmd[-3:] == ["python3", "/skill/agent.py", "--help"]

    def test_mounts_the_scripts_own_directory_read_only(self, tmp_path: Path):
        script = write(tmp_path, "agent.py", "if __name__ == '__main__':\n    pass\n")
        cmd = sandbox_command(script, "sandbox:test", 20)
        mount_idx = cmd.index("-v") + 1
        assert cmd[mount_idx] == f"{tmp_path.resolve()}:/skill:ro"

    def test_uses_the_given_timeout(self, tmp_path: Path):
        script = write(tmp_path, "agent.py", "if __name__ == '__main__':\n    pass\n")
        cmd = sandbox_command(script, "sandbox:test", 42)
        assert "timeout" in cmd
        assert cmd[cmd.index("timeout") + 1] == "42"


class TestClassify:
    def make(self, exit_code=None, docker_error=None) -> ScriptResult:
        return ScriptResult(Path("x.py"), exit_code, "", "", docker_error=docker_error)

    def test_docker_infra_error_fails(self):
        assert classify(self.make(docker_error="docker not found")) == "fail"

    def test_clean_exit_is_ok(self):
        assert classify(self.make(exit_code=0)) == "ok"

    def test_timeout_exit_code_fails(self):
        assert classify(self.make(exit_code=TIMEOUT_EXIT_CODE)) == "fail"

    def test_crash_signal_fails(self):
        # SIGSEGV
        assert classify(self.make(exit_code=139)) == "fail"
        # SIGABRT
        assert classify(self.make(exit_code=134)) == "fail"

    def test_ordinary_nonzero_exit_is_informational(self):
        # ModuleNotFoundError / OSError / argparse usage errors and similar
        # ordinary script failures — expected, not a containment problem.
        assert classify(self.make(exit_code=1)) == "info"
        assert classify(self.make(exit_code=2)) == "info"


class TestLastStderrLine:
    def test_returns_last_nonempty_line(self):
        result = ScriptResult(Path("x.py"), 1, "", "Traceback...\n  File x\nValueError: bad\n\n")
        assert last_stderr_line(result) == "ValueError: bad"

    def test_empty_stderr_returns_empty_string(self):
        result = ScriptResult(Path("x.py"), 0, "", "")
        assert last_stderr_line(result) == ""


class TestMainNoScriptsChanged:
    def test_returns_zero_when_nothing_relevant_changed(self, capsys):
        # main() reads argv-style paths via argparse; call directly with no paths.
        import sandbox_run_changed_scripts as mod

        old_argv = sys.argv
        sys.argv = ["sandbox_run_changed_scripts.py"]
        try:
            assert mod.main() == 0
        finally:
            sys.argv = old_argv
        out = capsys.readouterr().out
        assert "No changed skill scripts" in out


class TestMainAggregatesFailures:
    def test_fails_when_any_script_fails_containment(self, tmp_path, monkeypatch, capsys):
        import sandbox_run_changed_scripts as mod

        skill_dir = tmp_path / "categories" / "general" / "some-skill" / "scripts"
        skill_dir.mkdir(parents=True)
        script_ok = skill_dir / "agent.py"
        script_ok.write_text("if __name__ == '__main__':\n    pass\n", encoding="utf-8")

        monkeypatch.setattr(
            mod,
            "changed_scripts",
            lambda paths: [script_ok],
        )

        def fake_run(script, image, timeout):
            return ScriptResult(script, TIMEOUT_EXIT_CODE, "", "")

        monkeypatch.setattr(mod, "run_in_sandbox", fake_run)

        old_argv = sys.argv
        sys.argv = ["sandbox_run_changed_scripts.py", str(script_ok)]
        try:
            assert mod.main() == 1
        finally:
            sys.argv = old_argv
        out = capsys.readouterr().out
        assert "failed sandbox containment checks" in out

    def test_passes_when_all_scripts_are_ok_or_informational(self, tmp_path, monkeypatch):
        import sandbox_run_changed_scripts as mod

        skill_dir = tmp_path / "categories" / "general" / "some-skill" / "scripts"
        skill_dir.mkdir(parents=True)
        script = skill_dir / "agent.py"
        script.write_text("if __name__ == '__main__':\n    pass\n", encoding="utf-8")

        monkeypatch.setattr(mod, "changed_scripts", lambda paths: [script])
        monkeypatch.setattr(
            mod, "run_in_sandbox", lambda s, image, timeout: ScriptResult(s, 1, "", "ModuleNotFoundError")
        )

        old_argv = sys.argv
        sys.argv = ["sandbox_run_changed_scripts.py", str(script)]
        try:
            assert mod.main() == 0
        finally:
            sys.argv = old_argv
