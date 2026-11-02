"""One block: horizontal dilution of precision after a valid fix.

Required plugins:
  - colosseum-core
  - colosseum-equipment
  - colosseum-shared

Instruments:
  - GNSS (``equipment.gnss``) with usable sky or a repeater

Supporting evidence: position, sats used, horizontal accuracy, track/sky/quality plots.

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_hdop.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Antenna / repeater with usable GNSS signal.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
gnss_id = FILL_IN_HERE  # int; [equipment.gnss] id from config.toml
fix_timeout_s = FILL_IN_HERE  # seconds; wait_for_fix budget (e.g. 120)
max_hdop = FILL_IN_HERE  # upper bound (e.g. 5)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.equipment.gnss.save_config(gnss_id=gnss_id, path="gnss/baseline.txt")
    col.equipment.gnss.start_logging(gnss_id=gnss_id, path="gnss/hdop.nmea", key="hdop")
    try:
        col.equipment.gnss.wait_for_fix(gnss_id=gnss_id, timeout_s=fix_timeout_s)
        col.equipment.gnss.measure_latitude(gnss_id=gnss_id, key="hdop_lat")
        col.equipment.gnss.measure_longitude(gnss_id=gnss_id, key="hdop_lon")
        col.equipment.gnss.measure_altitude_m(gnss_id=gnss_id, key="hdop_alt")
        col.equipment.gnss.measure_satellites(gnss_id=gnss_id, key="hdop_sats")
        col.equipment.gnss.measure_h_acc_m(gnss_id=gnss_id, key="hdop_h_acc")
        col.equipment.gnss.measure_hdop(gnss_id=gnss_id, key="hdop")
        col.equipment.gnss.verify_hdop(key="hdop", limit=max_hdop)
        col.equipment.gnss.save_track_plot(gnss_id=gnss_id, path="gnss/hdop_track.png")
        col.equipment.gnss.save_skyplot(gnss_id=gnss_id, path="gnss/hdop_sky.png")
        col.equipment.gnss.save_quality_plot(gnss_id=gnss_id, path="gnss/hdop_quality.png")
    finally:
        col.equipment.gnss.stop_logging(gnss_id=gnss_id)


if __name__ == "__main__":
    main()
    col.endex()
