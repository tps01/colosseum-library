"""One block: power in band."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Band limits in FILL_IN_HERE.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
band_start_hz = FILL_IN_HERE
band_stop_hz = FILL_IN_HERE
max_band_power_dbm = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.shared.signal.measure_band_power_dbm(speca_id=speca_id, start_hz=band_start_hz, stop_hz=band_stop_hz, key="band_dbm")
    col.shared.verify.verify_field(key="band_dbm", expected_val=max_band_power_dbm, tolerance=0.0)


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
