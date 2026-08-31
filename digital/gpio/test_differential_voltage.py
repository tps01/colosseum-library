"""One block: differential voltage."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Diff probe on pair.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
vdiff_expected = FILL_IN_HERE
vdiff_tolerance = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_differential(oscope_id=oscope_id, key="vdiff")
    col.shared.verify.verify_field(key="vdiff", expected_val=vdiff_expected, tolerance=vdiff_tolerance)


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
