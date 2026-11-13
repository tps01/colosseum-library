#!/usr/bin/env bash
# Download latest Colosseum release wheels and linter VSIX from GitHub Releases.
# Requires python3. Assets are saved in the shared tools directory.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

python3 - "$TOOLS_DIR" <<'PY'
import json
import sys
import urllib.request
from pathlib import Path

out_dir = Path(sys.argv[1])
headers = {
    "User-Agent": "colosseum-download-releases",
    "Accept": "application/vnd.github+json",
}
targets = [
    ("tps01/colosseum-core", "colosseum_core-*-py3-none-any.whl"),
    ("tps01/colosseum-extensions", "colosseum_extensions-*-py3-none-any.whl"),
    ("tps01/colosseum-shared", "colosseum_shared-*-py3-none-any.whl"),
    ("tps01/colosseum-gui", "colosseum_gui-*-py3-none-any.whl"),
    ("tps01/colosseum-host", "colosseum_host-*-py3-none-any.whl"),
    ("tps01/colosseum-messaging", "colosseum_messaging-*-py3-none-any.whl"),
    ("tps01/colosseum-equipment", "colosseum_equipment-*-py3-none-any.whl"),
    ("tps01/colosseum-linter", "colosseum-linter-*.vsix"),
]

for repo, pattern in targets:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases/latest", headers=headers
    )
    with urllib.request.urlopen(request) as response:
        release = json.load(response)
    prefix, suffix = pattern.split("*", 1)
    asset = next(
        (item for item in release.get("assets", [])
         if item["name"].startswith(prefix) and item["name"].endswith(suffix)),
        None,
    )
    if asset is None:
        raise SystemExit(
            f"No asset matching {pattern!r} in {repo} release {release.get('tag_name')}."
        )
    destination = out_dir / asset["name"]
    print(f"Downloading {asset['name']} from {repo} {release.get('tag_name')} ...")
    request = urllib.request.Request(asset["browser_download_url"], headers=headers)
    with urllib.request.urlopen(request) as response, destination.open("wb") as output:
        output.write(response.read())
    print(f"  -> {destination}")

print(f"Done. Downloaded {len(targets)} assets to {out_dir}")
PY
