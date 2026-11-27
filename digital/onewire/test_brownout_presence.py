"""Put actual DUT VDD on the first channel and the bus on the second. Verify the bus cannot back-power the DUT. Trigger on reset, with a full post-reset window and supply recovery."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.onewire.brownout_reference import brownout

SETTINGS = {
    "oscope_id": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
    "probe_valid_v": FILL_IN_HERE,
    "window_s": FILL_IN_HERE,
    "max_sample_spacing_s": FILL_IN_HERE,
    "channels": FILL_IN_HERE,
    "arm_delay_s": FILL_IN_HERE,
    "psu_id": FILL_IN_HERE,
    "onewire_id": FILL_IN_HERE,
    "levels_v": FILL_IN_HERE,
    "repeats": FILL_IN_HERE,
    "threshold_v": FILL_IN_HERE,
    "hysteresis_v": FILL_IN_HERE,
    "reset_width_s": FILL_IN_HERE,
    "presence_delay_s": FILL_IN_HERE,
    "presence_width_s": FILL_IN_HERE,
    "current_limit_a": FILL_IN_HERE,
    "settle_s": FILL_IN_HERE,
    "step_tolerance_v": FILL_IN_HERE,
    "threshold_limits_v": FILL_IN_HERE,
    "maximum_bracket_width_v": FILL_IN_HERE,
    "recovery_off_s": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="brownout_presence",
        collect=brownout,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
