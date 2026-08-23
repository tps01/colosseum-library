"""One block: minimum margin below mask."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Mask file path in FILL_IN_HERE.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
trace_path = "traces/mask.csv"
mask_file = FILL_IN_HERE
sg_window_length = FILL_IN_HERE
sg_polyorder = FILL_IN_HERE
min_margin_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)
    col.shared.signal.measure_mask_margin_db(trace_path=trace_path, mask_path=mask_file, sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, key="margin_db")
    col.shared.verify.verify_field(key="margin_db", expected_val=min_margin_db, tolerance=0.0)


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
