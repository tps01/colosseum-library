"""One block: common-mode voltage."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Diff probe; CM measurement.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
vcm_max = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_common_mode(oscope_id=oscope_id, key="vcm")
    col.shared.verify.verify_field(key="vcm", expected_val=vcm_max, tolerance=0.0)


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
