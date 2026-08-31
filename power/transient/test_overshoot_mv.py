"""One block: rail overshoot after load step."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope AC on rail; Kelvin sense.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
psu_id = FILL_IN_HERE
eload_id = FILL_IN_HERE
oscope_id = FILL_IN_HERE
rail_v = FILL_IN_HERE
load_step_a = FILL_IN_HERE
max_overshoot_mv = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=rail_v)
    col.equipment.psu.set_output(psu_id=psu_id, enabled=True)
    col.equipment.eload.set_current(eload_id=eload_id, current=load_step_a)
    col.equipment.eload.engage(eload_id=eload_id)
    col.equipment.oscope.measure_overshoot_mv(oscope_id=oscope_id, key="overshoot_mv")
    col.shared.verify.verify_field(key="overshoot_mv", expected_val=max_overshoot_mv, tolerance=0.0)


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
