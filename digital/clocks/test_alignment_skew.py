"""One block: clock alignment skew."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   CH1=REF CH2=DUT.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
ref_channel = FILL_IN_HERE
dut_channel = FILL_IN_HERE
max_skew_ns = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_phase_delay(oscope_id=oscope_id, ref_channel=ref_channel, dut_channel=dut_channel, key="skew_ns")
    col.shared.verify.verify_field(key="skew_ns", expected_val=max_skew_ns, tolerance=0.0)


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
