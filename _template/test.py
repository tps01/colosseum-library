"""Library test template (copy and rename).

Required plugins:
  - colosseum-core
  - colosseum-equipment   # when using autoconfig or instruments
  # - colosseum-shared
  # - colosseum-host

Instruments (example):
  - PSU / DMM / … as required by the procedure

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test.py
    colosseum run test.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# --- bench wiring ---
USE_AUTOCONFIG = True  # False: load sibling config.toml (copy from config.toml.example)

# --- procedure (replace every FILL_IN_HERE) ---
example_id = FILL_IN_HERE  # int; instrument id from autoconfig export or config.toml
example_limit = FILL_IN_HERE  # float; units depend on the check


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        # Optional: col.equipment.autoconfig(export_path="config.toml")
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()

    # TODO: Replace with measure / command / verify calls (one col.* per line).
    _ = example_id
    _ = example_limit


if __name__ == "__main__":
    main()
    col.endex()
