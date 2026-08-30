"""One block: PWM duty cycle."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope on PWM pin.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
oscope_id = FILL_IN_HERE
pwm_channel = FILL_IN_HERE
expected_duty_pct = FILL_IN_HERE
duty_tolerance_pct = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.oscope.measure_duty_cycle(oscope_id=oscope_id, channel=pwm_channel, key="duty_pct")
    col.shared.verify.verify_field(key="duty_pct", expected_val=expected_duty_pct, tolerance=duty_tolerance_pct)


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
