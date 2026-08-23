"""One block: tachometer RPM."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Tach wire on scope; know pulses/rev.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
tach_channel = FILL_IN_HERE
pulses_per_rev = FILL_IN_HERE
max_rpm = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_frequency(oscope_id=oscope_id, channel=tach_channel, key="tach_hz")
    col.shared.signal.measure_rpm_from_frequency(key="tach_hz", pulses_per_rev=pulses_per_rev, out_key="rpm")
    col.shared.verify.verify_field(key="rpm", expected_val=max_rpm, tolerance=0.0)


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
