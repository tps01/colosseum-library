"""Click a desktop control via UIA AutomationId (pywinauto / sim).

Required plugins:
  - colosseum-core
  - colosseum-gui


Drivers:
  - ``driver = pywinauto`` (**Windows only**) or ``sim`` for CI

Run::

    colosseum run test_uia_click.py --config bench.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

USE_AUTOCONFIG = False

desktop_id = FILL_IN_HERE  # int
automation_id = FILL_IN_HERE  # str; UIA AutomationId
expected_text = FILL_IN_HERE  # str; text after click


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("bench.toml")))


def main() -> None:
    _load_bench()
    col.gui.desktop.click(desktop_id=desktop_id, automation_id=automation_id)
    col.gui.desktop.verify_text(
        desktop_id=desktop_id,
        key="after_click",
        expected=expected_text,
        automation_id=automation_id,
    )


if __name__ == "__main__":
    main()
    col.endex()
