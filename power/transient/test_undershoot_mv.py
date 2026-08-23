"""One block: rail undershoot."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Load step release.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
psu_id = FILL_IN_HERE
eload_id = FILL_IN_HERE
oscope_id = FILL_IN_HERE
rail_v = FILL_IN_HERE
load_step_a = FILL_IN_HERE
max_undershoot_mv = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=rail_v)
    col.equipment.eload.set_current(eload_id=eload_id, current=load_step_a)
    col.equipment.eload.disengage(eload_id=eload_id)
    col.equipment.oscope.measure_undershoot_mv(oscope_id=oscope_id, key="undershoot_mv")
    col.shared.verify.verify_field(key="undershoot_mv", expected_val=max_undershoot_mv, tolerance=0.0)


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
