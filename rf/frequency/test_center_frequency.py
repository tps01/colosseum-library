"""One block: center frequency from smoothed trace."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Wideband stimulus; save trace first.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
trace_path = "traces/wideband.csv"
sg_window_length = FILL_IN_HERE
sg_polyorder = FILL_IN_HERE
analysis_start_hz = FILL_IN_HERE
analysis_stop_hz = FILL_IN_HERE
expected_cf_hz = FILL_IN_HERE
cf_tolerance_hz = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)
    col.shared.signal.measure_center_frequency(trace_path=trace_path, key="cf_hz", sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, start_hz=analysis_start_hz, stop_hz=analysis_stop_hz)
    col.shared.verify.verify_field(key="cf_hz", expected_val=expected_cf_hz, tolerance=cf_tolerance_hz)


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
