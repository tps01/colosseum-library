"""One block: maximum C/N0 (dB-Hz) across the recent sky view.

Required plugins:
  - colosseum-core
  - colosseum-equipment
  - colosseum-shared

Instruments:
  - GNSS (``equipment.gnss``) with usable sky or a repeater

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_max_cn0_dbhz.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Antenna / repeater with usable GNSS signal. Prefer sibling config.toml with
#   model omitted so MON-VER can select ublox-m9.

USE_AUTOCONFIG = False  # True only when COM/VISA autoconfig is the bench path

# --- procedure (replace every FILL_IN_HERE) ---
gnss_id = FILL_IN_HERE  # int; [equipment.gnss] id from config.toml
soak_s = FILL_IN_HERE  # seconds; allow GSV/NAV sky view to populate (e.g. 20)
min_cn0_dbhz = FILL_IN_HERE  # dB-Hz lower bound (e.g. 20 with usable sky)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.equipment.gnss.start_logging(gnss_id=gnss_id, path="gnss/max_cn0.nmea", key="max_cn0")
    try:
        col.shared.wait(duration=soak_s)
        col.equipment.gnss.get_constellations_present(gnss_id=gnss_id)
        col.equipment.gnss.get_satellite_snapshot(gnss_id=gnss_id)
        col.equipment.gnss.get_fix_type(gnss_id=gnss_id)
        col.equipment.gnss.measure_max_cn0_dbhz(gnss_id=gnss_id, key="max_cn0")
        col.equipment.gnss.verify_max_cn0_dbhz(key="max_cn0", limit=min_cn0_dbhz)
        col.equipment.gnss.save_skyplot(gnss_id=gnss_id, path="gnss/max_cn0_sky.png")
        col.equipment.gnss.save_quality_plot(gnss_id=gnss_id, path="gnss/max_cn0_quality.png")
    finally:
        col.equipment.gnss.stop_logging(gnss_id=gnss_id)


if __name__ == "__main__":
    main()
    col.endex()
