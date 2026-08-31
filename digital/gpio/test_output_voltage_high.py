"""One block: GPIO high voltage."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope on pin; drive high first.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
dio_id = FILL_IN_HERE
line = FILL_IN_HERE
oscope_id = FILL_IN_HERE
scope_channel = FILL_IN_HERE
v_high_min = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.dio.write_pin(dio_id=dio_id, line=line, value=True)
    col.equipment.oscope.measure_vpp(oscope_id=oscope_id, channel=scope_channel, key="v_high")
    col.equipment.oscope.verify_vpp(key="v_high", expected_val=v_high_min, tolerance=0.1)


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
