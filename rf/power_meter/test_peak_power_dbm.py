"""One block: peak/instantaneous power."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Averaging off.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
pwrmeter_id = FILL_IN_HERE
freq_hz = FILL_IN_HERE
max_peak_dbm = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.pwrmeter.set_frequency(pwrmeter_id=pwrmeter_id, frequency=freq_hz)
    col.equipment.pwrmeter.set_averaging_count(pwrmeter_id=pwrmeter_id, count=1)
    col.equipment.pwrmeter.measure_power(pwrmeter_id=pwrmeter_id, key="peak_dbm")
    col.shared.verify.verify_field(key="peak_dbm", expected_val=max_peak_dbm, tolerance=0.0)


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
