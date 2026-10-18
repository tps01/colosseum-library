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
from math import isfinite
from time import monotonic, sleep

from colosseum.context import get_context
from colosseum_gui.visual import pixel_diff_ratio

import colosseum as col

USE_AUTOCONFIG = False

desktop_id = FILL_IN_HERE  # int
image_path = FILL_IN_HERE  # str; click target PNG
baseline_path = FILL_IN_HERE  # str; independently approved POST-action PNG
max_diff_ratio = FILL_IN_HERE  # fraction 0..1, sensitive to the status region
timeout_s = FILL_IN_HERE  # business-result deadline
poll_s = FILL_IN_HERE  # screenshot polling cadence
capture_path = "captures/after_click.png"


@col.command
def wait_for_visual() -> None:
    """Poll artifacts without recording intermediate failed verifications."""
    if not all(isfinite(v) and v > 0 for v in (timeout_s, poll_s)):
        raise ValueError("Use finite positive timeout_s and poll_s")
    if not isfinite(max_diff_ratio) or not 0 <= max_diff_ratio <= 1:
        raise ValueError("max_diff_ratio must be a fraction in [0, 1]")
    output_dir = get_context().output_dir
    if output_dir is None:
        raise ValueError("Visual checks require screenshot artifacts")
    deadline = monotonic() + timeout_s
    while True:
        col.gui.desktop.capture_screenshot(desktop_id=desktop_id, path=capture_path)
        ratio = pixel_diff_ratio(Path(output_dir) / capture_path, Path(baseline_path), threshold=16)
        remaining = deadline - monotonic()
        if ratio <= max_diff_ratio or remaining <= 0:
            return  # the single final verification records PASS or FAIL
        sleep(min(poll_s, remaining))


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.gui.desktop.click(desktop_id=desktop_id, image=image_path)
    wait_for_visual()
    col.gui.desktop.verify_visual(key="after_click", path=capture_path, baseline=baseline_path, max_diff_ratio=max_diff_ratio, threshold=16)


if __name__ == "__main__":
    main()
    col.endex()
