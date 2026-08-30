"""One block: rail voltage at load."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Steady I_load.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
psu_id = FILL_IN_HERE
eload_id = FILL_IN_HERE
rail_v = FILL_IN_HERE
load_current_a = FILL_IN_HERE
min_voltage_v = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=rail_v)
    col.equipment.psu.set_output(psu_id=psu_id, enabled=True)
    col.equipment.eload.set_current(eload_id=eload_id, current=load_current_a)
    col.equipment.eload.engage(eload_id=eload_id)
    col.equipment.psu.measure_voltage(psu_id=psu_id, key="vrail")
    col.equipment.psu.verify_voltage(key="vrail", expected_val=min_voltage_v, tolerance=0.1)


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
