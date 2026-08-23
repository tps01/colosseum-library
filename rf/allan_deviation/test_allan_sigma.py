"""One block: Allan deviation at tau."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   FS740 reference input.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
fs740_id = FILL_IN_HERE
tau_s = FILL_IN_HERE
allan_max = FILL_IN_HERE
measurement_duration_s = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.fs740.measure_allan(fs740_id=fs740_id, tau_s=tau_s, duration_s=measurement_duration_s, key="allan_sigma")
    col.shared.verify.verify_field(key="allan_sigma", expected_val=allan_max, tolerance=0.0)


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
