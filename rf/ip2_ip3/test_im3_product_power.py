"""One block: IM3 product power at 2f2-f1."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Dual-tone on air.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
f1_hz = FILL_IN_HERE
f2_hz = FILL_IN_HERE
max_im3_dbm = FILL_IN_HERE


def main() -> None:
    _load_bench()
    im3_hz = 2 * f2_hz - f1_hz
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=im3_hz)
    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="im3_dbm")
    col.shared.verify.verify_field(key="im3_dbm", expected_val=max_im3_dbm, tolerance=0.0)


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
