"""One block: tone f1 power."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Dual-tone stimulus active.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
f1_hz = FILL_IN_HERE
expected_f1_dbm = FILL_IN_HERE
tolerance_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.vsg.set_multicarrier(vsg_id=vsg_id, num_tones=2, spacing_hz=1e6)
    col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=f1_hz)
    col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=f1_hz)
    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="f1_dbm")
    col.equipment.speca.verify_marker_power(key="f1_dbm", expected_val=expected_f1_dbm, tolerance=tolerance_db)


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
