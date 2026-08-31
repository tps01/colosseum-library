"""One block: GPIO rise time."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope on edge.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
scope_channel = FILL_IN_HERE
rise_max_ns = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_rise_time(oscope_id=oscope_id, channel=scope_channel, key="rise_ns")
    col.shared.verify.verify_field(key="rise_ns", expected_val=rise_max_ns, tolerance=0.0)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


if __name__ == "__main__":
    main()
    col.endex()
