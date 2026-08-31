"""Capture a desktop screenshot and compare to a baseline.

Required plugins:
  - colosseum-core
  - colosseum-gui

Run::

    colosseum run test_screenshot_match.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

USE_AUTOCONFIG = False

desktop_id = FILL_IN_HERE  # int
screenshot_path = FILL_IN_HERE  # str
baseline_path = FILL_IN_HERE  # str
max_diff_ratio = FILL_IN_HERE  # float


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.gui.desktop.capture_screenshot(desktop_id=desktop_id, path=screenshot_path)
    col.gui.desktop.verify_visual(
        key="visual",
        path=screenshot_path,
        baseline=baseline_path,
        max_diff_ratio=max_diff_ratio,
    )


if __name__ == "__main__":
    main()
    col.endex()
