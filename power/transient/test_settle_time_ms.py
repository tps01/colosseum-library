"""One block: rail settle time."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   After load step.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
max_settle_ms = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_settle_time(oscope_id=oscope_id, key="settle_ms")
    col.shared.verify.verify_field(key="settle_ms", expected_val=max_settle_ms, tolerance=0.0)


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
