"""Guards for the GitHub Actions workflows and the publish job's lock files.

These pin down supply-chain and signing properties that a YAML edit could
silently undo: every action is pinned to a commit SHA, the registry is signed
with Ed25519 only, the signature is verified with the committed public key
before upload, and the job that holds the signing key installs only
hash-locked dependencies.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
PUBLISH = REPO_ROOT / ".github" / "workflows" / "publish-registry.yml"
SHA_PINNED_USES = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")


def _load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    # PyYAML (YAML 1.1) parses the bare `on:` key as boolean True.
    if True in data:
        data["on"] = data.pop(True)
    return data


def _steps(job: dict) -> list[dict]:
    return job.get("steps", [])


def _step_index(steps: list[dict], predicate) -> int:
    for index, step in enumerate(steps):
        if predicate(step):
            return index
    raise AssertionError("step not found")


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=lambda p: p.name)
def test_every_action_is_pinned_to_a_commit_sha(workflow: Path):
    for job_name, job in _load(workflow)["jobs"].items():
        for step in _steps(job):
            uses = step.get("uses")
            if uses is None or uses.startswith("./"):
                continue
            assert SHA_PINNED_USES.match(uses), f"{workflow.name}:{job_name}: unpinned action {uses!r}"


def test_publish_registry_has_a_non_cancelling_concurrency_group():
    concurrency = _load(PUBLISH)["concurrency"]
    assert concurrency["group"] == "publish-registry"
    assert concurrency["cancel-in-progress"] is False


def test_publish_registry_triggers_cover_its_inputs():
    paths = _load(PUBLISH)["on"]["push"]["paths"]
    for required in (
        "categories/**",
        "tools/**",
        "keys/**",
        "manifest-schema.toml",
        ".github/workflows/publish-registry.yml",
    ):
        assert required in paths


def test_publish_registry_is_ed25519_only():
    text = PUBLISH.read_text(encoding="utf-8")
    for forbidden in ("SKILLS_SIGNING_KEY", "dev-fallback", "hmac", "HMAC", "SIGNING_KEY:"):
        assert forbidden not in text, forbidden


def test_only_the_signing_job_sees_the_secret_or_can_write():
    jobs = _load(PUBLISH)["jobs"]
    assert jobs["build"]["permissions"] == {"contents": "read"}
    assert "secrets." not in yaml.safe_dump(jobs["build"])
    sign = jobs["sign-and-publish"]
    assert sign["needs"] == "build"
    assert sign["permissions"] == {"contents": "write"}
    secret_steps = [s for s in _steps(sign) if "SKILLS_ED25519_PRIVATE_KEY" in yaml.safe_dump(s)]
    assert len(secret_steps) == 1
    assert secret_steps[0]["env"] == {
        "SKILLS_ED25519_PRIVATE_KEY": "${{ secrets.SKILLS_ED25519_PRIVATE_KEY }}"
    }


def test_signing_fails_when_the_secret_is_unset():
    sign_steps = _steps(_load(PUBLISH)["jobs"]["sign-and-publish"])
    step = sign_steps[_step_index(sign_steps, lambda s: "sign registry.json" in s.get("run", ""))]
    script = step["run"]
    assert 'if [ -z "${SKILLS_ED25519_PRIVATE_KEY}" ]' in script
    assert "exit 1" in script
    assert "sign_manifest.py sign registry.json --ed25519" in script


def test_signature_is_verified_with_the_committed_key_before_upload():
    steps = _steps(_load(PUBLISH)["jobs"]["sign-and-publish"])
    sign = _step_index(steps, lambda s: "sign registry.json" in s.get("run", ""))
    verify = _step_index(steps, lambda s: "sign_manifest.py verify" in s.get("run", ""))
    upload = _step_index(steps, lambda s: "upload-artifact" in s.get("uses", ""))
    publish = _step_index(steps, lambda s: "gh release upload" in s.get("run", ""))
    assert sign < verify < upload < publish
    verify_run = steps[verify]["run"]
    assert "--signature-file registry-signature.json" in verify_run
    assert "--key keys/registry-ed25519.pub" in verify_run
    assert (REPO_ROOT / "keys" / "registry-ed25519.pub").is_file()


def test_publish_installs_only_hash_locked_dependencies():
    jobs = _load(PUBLISH)["jobs"]
    expected = {"build": "tools/requirements.lock", "sign-and-publish": "tools/requirements-sign.lock"}
    for job_name, lock in expected.items():
        installs = [s["run"] for s in _steps(jobs[job_name]) if "pip install" in s.get("run", "")]
        assert installs == [f"python -m pip install --require-hashes --no-deps -r {lock}"]


def test_publish_validation_uses_the_warning_budget():
    runs = " ".join(s.get("run", "") for s in _steps(_load(PUBLISH)["jobs"]["build"]))
    assert "validate_skill.py --all --warning-budget tools/validation_warning_budget.json" in runs


def _locked_packages(lock: Path) -> dict[str, list[str]]:
    """Map package name -> hashes for a `uv pip compile --generate-hashes` file."""
    packages: dict[str, list[str]] = {}
    current = None
    for raw in lock.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("--hash=sha256:"):
            assert current is not None, f"{lock.name}: hash before any requirement"
            packages[current].append(line.split(":", 1)[1].rstrip(" \\"))
            continue
        match = re.match(r"^([A-Za-z0-9_.-]+)==[0-9][^ ]*( \\)?$", line)
        assert match, f"{lock.name}: not an exact pin: {raw!r}"
        current = match.group(1).lower().replace("_", "-")
        packages[current] = []
    return packages


@pytest.mark.parametrize("lock_name", ["requirements.lock", "requirements-sign.lock"])
def test_lock_files_pin_exact_versions_with_hashes(lock_name: str):
    packages = _locked_packages(REPO_ROOT / "tools" / lock_name)
    assert packages
    for name, hashes in packages.items():
        assert hashes, f"{lock_name}: {name} has no --hash"
        assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in hashes), name


def test_requirements_lock_covers_requirements_txt():
    wanted = {
        line.strip().lower()
        for line in (REPO_ROOT / "tools" / "requirements.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
    assert wanted <= set(_locked_packages(REPO_ROOT / "tools" / "requirements.lock"))


def test_signing_lock_is_only_the_cryptography_stack():
    assert set(_locked_packages(REPO_ROOT / "tools" / "requirements-sign.lock")) == {
        "cryptography",
        "cffi",
        "pycparser",
    }
