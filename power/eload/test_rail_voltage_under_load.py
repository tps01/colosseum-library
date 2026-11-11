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
supply_v = FILL_IN_HERE  # DUT input supply, not regulated output
current_limit_a = FILL_IN_HERE
dmm_id = FILL_IN_HERE  # HI/LO at DUT output
dmm_channel = FILL_IN_HERE
source_timeout_s = FILL_IN_HERE
source_tolerance_v = FILL_IN_HERE
dut_startup_s = FILL_IN_HERE
load_settle_s = FILL_IN_HERE
load_current_a = FILL_IN_HERE
load_current_tolerance_a = FILL_IN_HERE
slew_a_per_s = FILL_IN_HERE
min_voltage_v = FILL_IN_HERE


def main() -> None:
    _load_bench()
    try:
        col.equipment.psu.set_output(psu_id=psu_id, enabled=False)
        col.equipment.eload.disengage(eload_id=eload_id)
        col.equipment.eload.preset(eload_id=eload_id)
        col.equipment.psu.set_voltage(psu_id=psu_id, voltage=supply_v)
        col.equipment.psu.set_current_limit(psu_id=psu_id, current=current_limit_a)
        col.equipment.psu.set_output(psu_id=psu_id, enabled=True)
        col.equipment.psu.wait_for_voltage(psu_id=psu_id, voltage=supply_v, timeout_s=source_timeout_s, tolerance=source_tolerance_v)
        col.shared.wait(duration=dut_startup_s)
        col.equipment.eload.set_mode(eload_id=eload_id, mode="CC")
        col.equipment.eload.set_slew_rate(eload_id=eload_id, amps_per_s=slew_a_per_s)
        col.equipment.eload.set_current(eload_id=eload_id, current=load_current_a)
        col.equipment.eload.engage(eload_id=eload_id)
        col.shared.wait(duration=load_settle_s)
        col.equipment.eload.measure_current(eload_id=eload_id, key="actual_load_a")
        col.shared.verify.verify_field(key="actual_load_a", expected_val=load_current_a, tolerance=load_current_tolerance_a)
        col.equipment.dmm.measure_voltage(dmm_id=dmm_id, channel=dmm_channel, key="vrail")
        col.shared.verify.verify_field(key="vrail", minimum=min_voltage_v)
    finally:
        try:
            col.equipment.eload.disengage(eload_id=eload_id)
        finally:
            col.equipment.psu.set_output(psu_id=psu_id, enabled=False)


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
