"""One block: output IP3."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Measures f1, f2, IM3 then computes OIP3.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
f1_hz = FILL_IN_HERE
f2_hz = FILL_IN_HERE
oip3_min_dbm = FILL_IN_HERE


def main() -> None:
    _load_bench()
    im3_hz = 2 * f2_hz - f1_hz
    col.shared.signal.measure_oip3(vsg_id=vsg_id, speca_id=speca_id, f1_hz=f1_hz, f2_hz=f2_hz, im3_hz=im3_hz, key="oip3_dbm")
    col.shared.verify.verify_field(key="oip3_dbm", expected_val=oip3_min_dbm, tolerance=0.0)


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
