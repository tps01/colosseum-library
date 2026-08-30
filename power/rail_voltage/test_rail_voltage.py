"""Set a PSU rail, measure with a DMM, and verify voltage.

Required plugins:
  - colosseum-core
  - colosseum-equipment

Instruments:
  - PSU (``equipment.psu``)
  - DMM (``equipment.dmm``)

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_rail_voltage.py
    colosseum run test_rail_voltage.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# --- bench wiring ---
USE_AUTOCONFIG = True  # False: load sibling config.toml (copy from config.toml.example)

# --- procedure (replace every FILL_IN_HERE) ---
psu_id = FILL_IN_HERE  # int; [[equipment.psu]] id from autoconfig or config.toml
dmm_id = FILL_IN_HERE  # int; [[equipment.dmm]] id
dmm_channel = FILL_IN_HERE  # int; DMM input channel
set_voltage_v = FILL_IN_HERE  # V; PSU setpoint
current_limit_a = FILL_IN_HERE  # A; PSU current limit
expected_voltage_v = FILL_IN_HERE  # V; verification target
voltage_tolerance_v = FILL_IN_HERE  # V; absolute tolerance, e.g. 0.1


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

    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=set_voltage_v)
    col.equipment.psu.set_current_limit(psu_id=psu_id, current=current_limit_a)
    col.equipment.psu.set_output(psu_id=psu_id, enabled=True)
    col.equipment.dmm.measure_voltage(dmm_id=dmm_id, channel=dmm_channel, key="rail_v")
    col.equipment.dmm.verify_voltage(
        key="rail_v",
        expected_val=expected_voltage_v,
        tolerance=voltage_tolerance_v,
    )


if __name__ == "__main__":
    main()
    col.endex()
