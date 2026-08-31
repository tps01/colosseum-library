"""One block: occupied bandwidth from smoothed trace."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Wideband trace required.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
trace_path = "traces/wideband.csv"
sg_window_length = FILL_IN_HERE
sg_polyorder = FILL_IN_HERE
analysis_start_hz = FILL_IN_HERE
analysis_stop_hz = FILL_IN_HERE
threshold_db = FILL_IN_HERE
max_obw_hz = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)
    col.shared.signal.measure_occupied_bandwidth(trace_path=trace_path, key="obw_hz", sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, start_hz=analysis_start_hz, stop_hz=analysis_stop_hz, threshold_db=threshold_db)
    col.shared.verify.verify_field(key="obw_hz", expected_val=max_obw_hz, tolerance=0.0)


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
