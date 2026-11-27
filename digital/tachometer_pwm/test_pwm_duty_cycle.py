"""Prepare repetitive active-high PWM and the required pull-up. Measure multiple complete cycles."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.waveform_reference import pwm

SETTINGS = {
    "oscope_id": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
    "probe_valid_v": FILL_IN_HERE,
    "window_s": FILL_IN_HERE,
    "max_sample_spacing_s": FILL_IN_HERE,
    "hysteresis_v": FILL_IN_HERE,
    "min_cycles": FILL_IN_HERE,
    "period_bounds_s": FILL_IN_HERE,
    "channel": FILL_IN_HERE,
    "threshold_v": FILL_IN_HERE,
    "limits_pct": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="pwm_duty_cycle",
        collect=pwm,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
