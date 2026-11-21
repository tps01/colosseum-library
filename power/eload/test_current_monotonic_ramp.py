"""Capture DUT rail first and calibrated independent current monitor second. Trigger on the ramp and include both settled endpoints."""

from pathlib import Path

import colosseum as col

from reference_common import required
from power.eload.ramp_reference import ramp

SETTINGS = {
    "oscope_id": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
    "probe_valid_v": FILL_IN_HERE,
    "window_s": FILL_IN_HERE,
    "max_sample_spacing_s": FILL_IN_HERE,
    "channels": FILL_IN_HERE,
    "arm_delay_s": FILL_IN_HERE,
    "psu_id": FILL_IN_HERE,
    "eload_id": FILL_IN_HERE,
    "initial_a": FILL_IN_HERE,
    "final_a": FILL_IN_HERE,
    "current_v_per_a": FILL_IN_HERE,
    "current_zero_v": FILL_IN_HERE,
    "slew_a_per_s": FILL_IN_HERE,
    "supply_v": FILL_IN_HERE,
    "current_limit_a": FILL_IN_HERE,
    "settle_s": FILL_IN_HERE,
    "endpoint_samples": FILL_IN_HERE,
    "endpoint_tolerance_a": FILL_IN_HERE,
    "noise_allowance_a": FILL_IN_HERE,
    "min_transition_samples": FILL_IN_HERE,
    "compliance_min_v": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="current_monotonic_ramp",
        collect=ramp,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
