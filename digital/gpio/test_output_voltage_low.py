"""One block: GPIO low voltage."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope on pin; drive low.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
dio_id = FILL_IN_HERE
line = FILL_IN_HERE
oscope_id = FILL_IN_HERE
scope_channel = FILL_IN_HERE
v_low_max = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.dio.write_pin(dio_id=dio_id, line=line, value=False)
    col.equipment.oscope.measure_vpp(oscope_id=oscope_id, channel=scope_channel, key="v_low")
    col.shared.verify.verify_field(key="v_low", expected_val=v_low_max, tolerance=0.05)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("bench.toml")))


if __name__ == "__main__":
    main()
    col.endex()
