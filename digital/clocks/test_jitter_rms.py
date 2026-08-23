"""One block: RMS jitter."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope on clock; TIE measurement.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
clock_channel = FILL_IN_HERE
max_jitter_ps = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_jitter(oscope_id=oscope_id, channel=clock_channel, key="jitter_ps")
    col.shared.verify.verify_field(key="jitter_ps", expected_val=max_jitter_ps, tolerance=0.0)


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
