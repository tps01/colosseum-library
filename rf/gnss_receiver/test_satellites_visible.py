"""One block: satellites visible in the recent sky view (no fix required).

Required plugins:
  - colosseum-core
  - colosseum-equipment
  - colosseum-shared

Instruments:
  - GNSS (``equipment.gnss``) with usable sky or a repeater

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_satellites_visible.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Antenna / repeater with usable GNSS signal.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
gnss_id = FILL_IN_HERE  # int; [equipment.gnss] id from config.toml
soak_s = FILL_IN_HERE  # seconds; allow GSV to populate (e.g. 20)
min_sats_visible = FILL_IN_HERE  # lower bound (e.g. 4 with usable sky)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.equipment.gnss.start_logging(gnss_id=gnss_id, path="gnss/sats_visible.nmea", key="sats_visible", messages="default")
    try:
        col.shared.wait(duration=soak_s)
        col.equipment.gnss.get_satellite_snapshot(gnss_id=gnss_id)
        col.equipment.gnss.measure_satellites_visible(gnss_id=gnss_id, key="sats_visible")
        col.equipment.gnss.verify_satellites_visible(key="sats_visible", limit=min_sats_visible)
        col.equipment.gnss.save_skyplot(gnss_id=gnss_id, path="gnss/sats_visible_sky.png")
        col.equipment.gnss.save_signal_levels_plot(gnss_id=gnss_id, path="gnss/sats_visible_signals.png")
    finally:
        col.equipment.gnss.stop_logging(gnss_id=gnss_id)


if __name__ == "__main__":
    main()
    col.endex()
