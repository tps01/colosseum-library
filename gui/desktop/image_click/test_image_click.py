"""Click a desktop control via image template (generic / sim).

Required plugins:
  - colosseum-core
  - colosseum-gui

Drivers:
  - ``driver = generic`` (Linux X11 or Windows mouse) or ``sim``

Run::

    colosseum run test_image_click.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

USE_AUTOCONFIG = False

desktop_id = FILL_IN_HERE  # int
image_path = FILL_IN_HERE  # str; template PNG path


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.gui.desktop.click(desktop_id=desktop_id, image=image_path)
    col.gui.desktop.capture_screenshot(desktop_id=desktop_id, path="captures/after_click.png")


if __name__ == "__main__":
    main()
    col.endex()
