"""One block: fundamental power."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   CW tone at fundamental_hz.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
fundamental_hz = FILL_IN_HERE
expected_power_dbm = FILL_IN_HERE
power_tolerance_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=fundamental_hz)
    col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=fundamental_hz)
    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="fund_dbm")
    col.equipment.speca.verify_marker_power(key="fund_dbm", expected_val=expected_power_dbm, tolerance=power_tolerance_db)


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
