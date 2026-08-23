"""Click a web button and verify a status becomes visible.

Required plugins:
  - colosseum-core
  - colosseum-gui

Drivers:
  - ``[[gui.web]]`` with ``driver = sim`` or ``playwright``

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_button_visible.py --config bench.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# --- bench wiring ---
USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
web_id = FILL_IN_HERE  # int; [[gui.web]] web_id
button_role = FILL_IN_HERE  # str; e.g. "button"
button_name = FILL_IN_HERE  # str; e.g. "Start"
status_role = FILL_IN_HERE  # str; e.g. "status"
status_name = FILL_IN_HERE  # str; e.g. "Running"


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("bench.toml")))


def main() -> None:
    _load_bench()
    col.gui.web.click(web_id=web_id, role=button_role, name=button_name)
    col.gui.web.verify_visible(
        web_id=web_id, key="status_visible", role=status_role, name=status_name
    )


if __name__ == "__main__":
    main()
    col.endex()
