"""One block: Allan deviation at tau."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Long capture; counter or FS740.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
tau_s = FILL_IN_HERE
allan_max = FILL_IN_HERE
sample_duration_s = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.fs740.measure_allan(fs740_id=FILL_IN_HERE, tau_s=tau_s, duration_s=sample_duration_s, key="allan")
    col.shared.verify.verify_field(key="allan", expected_val=allan_max, tolerance=0.0)


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
