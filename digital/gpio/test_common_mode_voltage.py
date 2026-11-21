"""Use qualified isolated probes for Vp and Vn on the same timebase. Select a settled DC window."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.waveform_reference import gpio_common

SETTINGS = {
    "oscope_id": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
    "probe_valid_v": FILL_IN_HERE,
    "window_s": FILL_IN_HERE,
    "max_sample_spacing_s": FILL_IN_HERE,
    "channels": FILL_IN_HERE,
    "limits_v": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="common_mode_voltage",
        collect=gpio_common,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
