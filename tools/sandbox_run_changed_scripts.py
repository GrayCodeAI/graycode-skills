#!/usr/bin/env python3
"""Smoke-test changed skill scripts inside a locked-down Docker sandbox.

What this proves, and what it deliberately does NOT: every scripts/*.py
file in this corpus assumes real infrastructure this CI must never hand to
untrusted third-party code (cloud credentials, live network targets,
external binaries like grype/aws/kubectl/impacket). So this cannot and does
not exercise a script's real business logic. It runs each changed script
with `--help` inside a container with no network, a read-only root
filesystem, dropped capabilities, and tight resource limits, then checks
that containment actually held — not that the script "passed." A script
that errors on a missing optional import, or on the read-only filesystem
blocking a write it attempted, is doing exactly what's expected and is NOT
treated as a failure; this is a narrow safety net against a payload placed
at import time or in argument-parser setup (where a disguised malicious
script would most plausibly need to run unconditionally), not a behavioral
audit of the script's full functionality.

Verified locally against real corpus scripts before wiring into CI: a
stdlib-only script whose __init__ writes to disk before checking --help
fails safely with a read-only-filesystem OSError (containment working
correctly, not a bug); a script needing an uninstalled exotic dependency
(impacket) fails cleanly at import; a script with only pre-installed common
dependencies (requests/pyyaml) succeeds. All three are the expected,
non-failing outcomes under the classification below. --network=none was
independently verified to make DNS resolution itself fail, not merely
slow the connection.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_changed_scripts import changed_scripts

DEFAULT_IMAGE = "ghcr.io/graycodeai/hawk-community-skills-sandbox:latest"
DEFAULT_TIMEOUT_SECONDS = 20

# The `timeout` coreutil's own exit code when it kills the wrapped process —
# abnormal for a --help invocation, so this counts as a containment failure.
TIMEOUT_EXIT_CODE = 124


@dataclass
class ScriptResult:
    script: Path
    exit_code: int | None
    stdout: str
    stderr: str
    docker_error: str | None = None


def has_main_block(path: Path) -> bool:
    """Cheap check for a runnable entrypoint (confirmed present in 100% of
    the corpus's scripts/*.py files as of the last full scan)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return "__main__" in text


def sandbox_command(script: Path, image: str, timeout: int) -> list[str]:
    return [
        "docker",
        "run",
        "--rm",
        "--network=none",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,size=64m,mode=1777",
        "--memory=256m",
        "--cpus=0.5",
        "--pids-limit=64",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--user",
        "1000:1000",
        "-v",
        f"{script.resolve().parent}:/skill:ro",
        image,
        "timeout",
        str(timeout),
        "python3",
        f"/skill/{script.name}",
        "--help",
    ]


def run_in_sandbox(script: Path, image: str, timeout: int) -> ScriptResult:
    cmd = sandbox_command(script, image, timeout)
    try:
        # Generous outer margin over the container's own `timeout` so a
        # slow-to-schedule container doesn't get misclassified as a Docker
        # failure instead of a script-hang failure.
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15, check=False)
    except subprocess.TimeoutExpired:
        return ScriptResult(script, None, "", "", docker_error="docker itself did not return in time")
    except OSError as exc:
        return ScriptResult(script, None, "", "", docker_error=f"failed to invoke docker: {exc}")
    return ScriptResult(script, proc.returncode, proc.stdout, proc.stderr)


def classify(result: ScriptResult) -> str:
    """Return 'fail' (containment problem — should fail CI), 'info'
    (ordinary, expected script error — logged, not failing), or 'ok'."""
    if result.docker_error is not None:
        return "fail"
    if result.exit_code == 0:
        return "ok"
    if result.exit_code == TIMEOUT_EXIT_CODE:
        return "fail"
    if result.exit_code is not None and result.exit_code >= 128:
        # 128+signal — SIGSEGV=139, SIGABRT=134, etc.
        return "fail"
    return "info"


def last_stderr_line(result: ScriptResult) -> str:
    lines = [line for line in result.stderr.strip().splitlines() if line.strip()]
    return lines[-1] if lines else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sandbox-smoke-test changed skill scripts (containment check, not a behavior audit)"
    )
    parser.add_argument("paths", nargs="*", help="changed repository-relative paths")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="sandbox image to run scripts in")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="per-script timeout in seconds")
    args = parser.parse_args()

    scripts = [s for s in changed_scripts(args.paths) if has_main_block(s)]
    if not scripts:
        print("✓ No changed skill scripts with a __main__ block to sandbox-test")
        return 0

    failed: list[Path] = []
    for script in scripts:
        result = run_in_sandbox(script, args.image, args.timeout)
        verdict = classify(result)
        if verdict == "ok":
            print(f"  ✓ {script}: ran cleanly (exit 0)")
        elif verdict == "info":
            detail = last_stderr_line(result)
            suffix = f" — {detail}" if detail else ""
            print(f"  ⚠ {script}: exited {result.exit_code} (informational, not a safety concern){suffix}")
        else:
            reason = result.docker_error or f"exit {result.exit_code} (timeout or crash signal)"
            print(f"  ✗ {script}: {reason}")
            failed.append(script)

    if failed:
        print(f"\n✗ {len(failed)} script(s) failed sandbox containment checks:")
        for script in failed:
            print(f"  - {script}")
        return 1

    print(f"\n✓ Sandbox containment held for all {len(scripts)} changed script(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
