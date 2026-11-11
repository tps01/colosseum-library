"""Set a PSU rail, measure with a DMM, and verify voltage.

Required plugins:
  - colosseum-core
  - colosseum-equipment
  - colosseum-shared

Instruments:
  - PSU (``equipment.psu``)
  - DMM (``equipment.dmm``)

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_rail_voltage.py
    colosseum run test_rail_voltage.py --config config.toml
    colosseum run test_rail_voltage.py --config config.toml --parameters parameters.toml
    colosseum run test_rail_voltage.py --config config.toml --report junit
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# --- bench wiring ---
USE_AUTOCONFIG = True  # False: load sibling config.toml (copy from config.toml.example)

# --- procedure (replace every FILL_IN_HERE) ---
psu_id = FILL_IN_HERE  # int; [equipment.psu] id from autoconfig or config.toml
dmm_id = FILL_IN_HERE  # int; [equipment.dmm] id
dmm_channel = FILL_IN_HERE  # int; DMM input channel
set_voltage_v = FILL_IN_HERE  # V; PSU setpoint
current_limit_a = FILL_IN_HERE  # A; PSU current limit
source_timeout_s = FILL_IN_HERE
source_tolerance_v = FILL_IN_HERE
dut_settle_s = FILL_IN_HERE  # qualified startup allowance after source settles
# Copy parameters.toml.example to parameters.toml and fill [rail_v], or pass
# --parameters. Limits come from that file, not an implicit inline fallback.


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
    try:
        col.equipment.psu.set_output(psu_id=psu_id, enabled=False)
        col.equipment.psu.set_voltage(psu_id=psu_id, voltage=set_voltage_v)
        col.equipment.psu.set_current_limit(psu_id=psu_id, current=current_limit_a)
        col.equipment.psu.set_output(psu_id=psu_id, enabled=True)
        col.equipment.psu.wait_for_voltage(psu_id=psu_id, voltage=set_voltage_v, timeout_s=source_timeout_s, tolerance=source_tolerance_v)
        col.shared.wait(duration=dut_settle_s)
        col.equipment.dmm.measure_voltage(dmm_id=dmm_id, channel=dmm_channel, key="rail_v")
        # With --parameters / sibling parameters.toml, omit expected_val/tolerance here
        # so the [rail_v] table fills them. File fields override matching call kwargs
        # when both are present.
        col.equipment.dmm.verify_voltage(key="rail_v")
    finally:
        col.equipment.psu.set_output(psu_id=psu_id, enabled=False)


if __name__ == "__main__":
    main()
    col.endex()
