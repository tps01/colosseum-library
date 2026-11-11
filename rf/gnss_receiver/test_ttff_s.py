"""One block: time to first fix after mark_acquisition_start (seconds).

Required plugins:
  - colosseum-core
  - colosseum-equipment
  - colosseum-shared

Instruments:
  - GNSS (``equipment.gnss``) with usable sky or a repeater

Does not issue cold_start; marks T0 then waits for a valid fix.

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_ttff_s.py --config config.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Antenna / repeater with usable GNSS signal. Warm/hot start expected.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
gnss_id = FILL_IN_HERE  # int; [equipment.gnss] id from config.toml
fix_timeout_s = FILL_IN_HERE  # seconds; wait_for_fix budget (e.g. 120)
max_ttff_s = FILL_IN_HERE  # seconds; upper bound on measured TTFF (e.g. 120)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


def main() -> None:
    _load_bench()
    col.equipment.gnss.start_logging(gnss_id=gnss_id, path="gnss/ttff.nmea", key="ttff")
    try:
        col.equipment.gnss.mark_acquisition_start(gnss_id=gnss_id)
        col.equipment.gnss.wait_for_fix(gnss_id=gnss_id, timeout_s=fix_timeout_s)
        col.equipment.gnss.measure_ttff_s(gnss_id=gnss_id, key="ttff")
        col.shared.verify.verify_field(key="ttff", maximum=max_ttff_s)
        col.equipment.gnss.get_fix_type(gnss_id=gnss_id)
    finally:
        col.equipment.gnss.stop_logging(gnss_id=gnss_id)


if __name__ == "__main__":
    main()
    col.endex()
