"""Measure web navigation duration.

Required plugins:
  - colosseum-core
  - colosseum-gui
  - colosseum-shared

Drivers:
  - ``playwright`` (or ``sim`` for canned timing)

Run::

    colosseum run test_navigation_ms.py --config bench.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

USE_AUTOCONFIG = False

web_id = FILL_IN_HERE  # int
url = FILL_IN_HERE  # str
max_ms = FILL_IN_HERE  # float; upper bound for navigation


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    col.config.load_config(str(Path(__file__).with_name("bench.toml")))


def main() -> None:
    _load_bench()
    col.gui.web.navigate(web_id=web_id, url=url)
    col.gui.web.measure_navigation_ms(web_id=web_id, key="nav_ms")
    # Pass if measured time is within [0, max_ms].
    col.shared.verify.verify_field(key="nav_ms", expected_val=0.0, tolerance=max_ms)


if __name__ == "__main__":
    main()
    col.endex()
