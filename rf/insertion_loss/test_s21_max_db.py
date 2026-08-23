"""One block: worst S21 over band."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Through path; port extensions optional.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vna_id = FILL_IN_HERE
start_hz = FILL_IN_HERE
stop_hz = FILL_IN_HERE
points = FILL_IN_HERE
s21_max_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.vna.set_start_frequency(vna_id=vna_id, frequency_hz=start_hz)
    col.equipment.vna.set_stop_frequency(vna_id=vna_id, frequency_hz=stop_hz)
    col.equipment.vna.set_points(vna_id=vna_id, points=points)
    col.equipment.vna.set_trace_parameters(vna_id=vna_id, trace=1, parameter="S21")
    col.equipment.vna.single_sweep(vna_id=vna_id)
    col.shared.signal.measure_s21_max(vna_id=vna_id, trace=1, key="s21_max")
    col.shared.verify.verify_field(key="s21_max", expected_val=s21_max_db, tolerance=0.0)


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
