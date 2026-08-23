"""One block: tone f2 power."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   f2 = f1 + 1 MHz.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
f2_hz = FILL_IN_HERE
expected_f2_dbm = FILL_IN_HERE
tolerance_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=f2_hz)
    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="f2_dbm")
    col.equipment.speca.verify_marker_power(key="f2_dbm", expected_val=expected_f2_dbm, tolerance=tolerance_db)


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
