"""One block: worst S11 over band."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Input port; cal kit.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vna_id = FILL_IN_HERE
start_hz = FILL_IN_HERE
stop_hz = FILL_IN_HERE
points = FILL_IN_HERE
s11_max_db = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.vna.set_trace_parameters(vna_id=vna_id, trace=1, parameter="S11")
    col.equipment.vna.single_sweep(vna_id=vna_id)
    col.shared.signal.measure_s11_max(vna_id=vna_id, trace=1, key="s11_max")
    col.shared.verify.verify_field(key="s11_max", expected_val=s11_max_db, tolerance=0.0)


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
