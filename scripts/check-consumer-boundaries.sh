#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

violations="$(
  grep -RInE \
    --include='*.py' --include='*.md' --include='*.json' --include='*.yaml' --include='*.yml' --include='*.toml' \
    'github\.com/GrayCodeAI/(graycode-router|harrier|shrike|swift|kestrel|merlin)(/|")|github\.com/GrayCodeAI/graycode-cli/(internal/|shared/types)' \
    README.md docs api tests tools .claude-plugin .codex-plugin .cursor-plugin 2>/dev/null || true
)"

if [[ -n "${violations}" ]]; then
  echo "forbidden Graycode consumer references found:"
  echo "${violations}"
  echo
  echo "graycode-skills must target Graycode public skill/plugin surfaces only; do not reference support engine repos, graycode-cli/internal, or removed graycode/shared/types"
  exit 1
fi

echo "consumer boundary guard passed"
