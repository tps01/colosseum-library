"""One block: gain flatness over band."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Through DUT path; cable loss table optional.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
freq_start_hz = FILL_IN_HERE
freq_stop_hz = FILL_IN_HERE
freq_step_hz = FILL_IN_HERE
gain_flatness_max_db = FILL_IN_HERE
sg_window_length = FILL_IN_HERE
sg_polyorder = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.shared.signal.measure_gain_flatness(vsg_id=vsg_id, speca_id=speca_id, freq_start_hz=freq_start_hz, freq_stop_hz=freq_stop_hz, freq_step_hz=freq_step_hz, sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, key="flatness_db")
    col.shared.verify.verify_field(key="flatness_db", expected_val=gain_flatness_max_db, tolerance=0.0)


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
