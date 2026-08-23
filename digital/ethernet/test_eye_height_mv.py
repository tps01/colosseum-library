"""One block: SI eye height."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Diff probe on TX pair.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
min_eye_mv = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_eye_height(oscope_id=oscope_id, key="eye_mv")
    col.shared.verify.verify_field(key="eye_mv", expected_val=min_eye_mv, tolerance=0.0)


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
