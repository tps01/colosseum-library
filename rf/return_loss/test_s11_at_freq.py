"""One block: S11 at spot frequency."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Marker at spot_freq_hz.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vna_id = FILL_IN_HERE
spot_freq_hz = FILL_IN_HERE
s11_at_freq_db = FILL_IN_HERE
tolerance_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.vna.set_marker(vna_id=vna_id, marker=1, frequency_hz=spot_freq_hz, trace=1)
    col.equipment.vna.measure_marker_value(vna_id=vna_id, marker=1, key="s11_spot", trace=1)
    col.equipment.vna.verify_marker_value(key="s11_spot", expected_val=s11_at_freq_db, tolerance=tolerance_db)


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
