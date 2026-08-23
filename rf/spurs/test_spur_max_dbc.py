"""One block: worst non-harmonic spur."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Single tone; max-hold trace.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
trace_path = "traces/spurs.csv"
fundamental_hz = FILL_IN_HERE
sg_window_length = FILL_IN_HERE
sg_polyorder = FILL_IN_HERE
max_spur_dbc = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)
    col.shared.signal.measure_spur_max_dbc(trace_path=trace_path, fundamental_hz=fundamental_hz, sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, key="spur_dbc")
    col.shared.verify.verify_field(key="spur_dbc", expected_val=max_spur_dbc, tolerance=0.0)


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
