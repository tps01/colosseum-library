#!/usr/bin/env bash
# Create a Linux .venv and pip-install local Colosseum release wheels.
# Expects wheels from download_releases.sh in the shared tools directory.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"
mapfile -t WHEELS < <(find "$TOOLS_DIR" -maxdepth 1 -type f -name '*.whl' -print | sort)

if ((${#WHEELS[@]} == 0)); then
    printf 'No .whl files found in %s. Run linux/download_releases.sh first.\n' "$TOOLS_DIR" >&2
    exit 1
fi

PYTHON_CMD="$(command -v python3 || true)"
if [[ -z "$PYTHON_CMD" ]]; then
    printf "'python3' was not found on PATH.\n" >&2
    exit 1
fi

if [[ ! -x "$VENV_PATH/bin/python" ]]; then
    if [[ -e "$VENV_PATH" ]]; then
        printf 'Virtual environment exists but has no executable Python: %s\n' "$VENV_PATH" >&2
        exit 1
    fi
    printf 'Creating virtual environment: %s\n' "$VENV_PATH"
    "$PYTHON_CMD" -m venv "$VENV_PATH"
else
    printf 'Using existing virtual environment: %s\n' "$VENV_PATH"
fi

VENV_PYTHON="$VENV_PATH/bin/python"
printf 'Upgrading pip ...\n'
"$VENV_PYTHON" -m pip install --upgrade pip
printf 'Installing %d wheel(s) from %s ...\n' "${#WHEELS[@]}" "$TOOLS_DIR"
printf '  %s\n' "${WHEELS[@]##*/}"
"$VENV_PYTHON" -m pip install "${WHEELS[@]}"

VSIX_COUNT="$(find "$TOOLS_DIR" -maxdepth 1 -type f -name '*.vsix' -printf . | wc -c)"
if ((VSIX_COUNT > 0)); then
    printf 'Note: %d .vsix file(s) were left for manual Cursor/VS Code install (not pip).\n' "$VSIX_COUNT"
fi

printf 'Done. Activate with: source "%s/bin/activate"\n' "$VENV_PATH"
