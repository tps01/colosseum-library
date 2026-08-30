"""Capture a web screenshot and compare to a baseline PNG.

Required plugins:
  - colosseum-core
  - colosseum-gui

Drivers:
  - ``[[gui.web]]`` with ``driver = sim`` or ``playwright``

Baselines are environment-locked (OS, scale, headed vs headless).

Run::

    colosseum run test_screenshot_match.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

USE_AUTOCONFIG = False

web_id = FILL_IN_HERE  # int
screenshot_path = FILL_IN_HERE  # str; e.g. "captures/page.png"
baseline_path = FILL_IN_HERE  # str; path to golden PNG
max_diff_ratio = FILL_IN_HERE  # float; e.g. 0.01


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.gui.web.capture_screenshot(web_id=web_id, path=screenshot_path)
    col.gui.web.verify_visual(
        key="visual",
        path=screenshot_path,
        baseline=baseline_path,
        max_diff_ratio=max_diff_ratio,
    )


if __name__ == "__main__":
    main()
    col.endex()
