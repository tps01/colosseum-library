"""One block: averaged RF power."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Set sensor frequency.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
pwrmeter_id = FILL_IN_HERE
freq_hz = FILL_IN_HERE
avg_count = FILL_IN_HERE
expected_power_dbm = FILL_IN_HERE
tolerance_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.pwrmeter.set_frequency(pwrmeter_id=pwrmeter_id, frequency=freq_hz)
    col.equipment.pwrmeter.set_averaging_count(pwrmeter_id=pwrmeter_id, count=avg_count)
    col.equipment.pwrmeter.measure_power(pwrmeter_id=pwrmeter_id, key="avg_dbm")
    col.equipment.pwrmeter.verify_power(key="avg_dbm", expected_val=expected_power_dbm, tolerance=tolerance_db)


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
