"""One block: 1 dB compression point."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Power sweep at output tap.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
pin_start_dbm = FILL_IN_HERE
pin_stop_dbm = FILL_IN_HERE
pin_step_db = FILL_IN_HERE
p1db_min_dbm = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.shared.signal.measure_p1db(vsg_id=vsg_id, speca_id=speca_id, pin_start_dbm=pin_start_dbm, pin_stop_dbm=pin_stop_dbm, pin_step_db=pin_step_db, key="p1db_dbm")
    col.shared.verify.verify_field(key="p1db_dbm", expected_val=p1db_min_dbm, tolerance=0.0)


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
