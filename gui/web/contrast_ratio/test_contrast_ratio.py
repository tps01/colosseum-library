"""Measure WCAG contrast between two rectangles on a web screenshot.

Required plugins:
  - colosseum-core
  - colosseum-gui

Run::

    colosseum run test_contrast_ratio.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

USE_AUTOCONFIG = False

web_id = FILL_IN_HERE  # int
screenshot_path = FILL_IN_HERE  # str
fg_x = FILL_IN_HERE  # int
fg_y = FILL_IN_HERE  # int
fg_w = FILL_IN_HERE  # int
fg_h = FILL_IN_HERE  # int
bg_x = FILL_IN_HERE  # int
bg_y = FILL_IN_HERE  # int
bg_w = FILL_IN_HERE  # int
bg_h = FILL_IN_HERE  # int
min_contrast = FILL_IN_HERE  # float; e.g. 4.5


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.gui.web.capture_screenshot(web_id=web_id, path=screenshot_path)
    col.gui.web.measure_contrast_ratio(
        web_id=web_id,
        key="contrast",
        path=screenshot_path,
        fg_x=fg_x,
        fg_y=fg_y,
        fg_w=fg_w,
        fg_h=fg_h,
        bg_x=bg_x,
        bg_y=bg_y,
        bg_w=bg_w,
        bg_h=bg_h,
    )
    col.gui.web.verify_contrast(key="contrast", minimum=min_contrast)


if __name__ == "__main__":
    main()
    col.endex()
