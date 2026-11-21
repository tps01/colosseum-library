"""Same scope acquisition on A and B, with calibrated deskew and matching edges. Limits apply to B minus A."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.waveform_reference import skew

SETTINGS = {
    "oscope_id": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
    "probe_valid_v": FILL_IN_HERE,
    "window_s": FILL_IN_HERE,
    "max_sample_spacing_s": FILL_IN_HERE,
    "hysteresis_v": FILL_IN_HERE,
    "min_cycles": FILL_IN_HERE,
    "period_bounds_s": FILL_IN_HERE,
    "channels": FILL_IN_HERE,
    "thresholds_v": FILL_IN_HERE,
    "pair_window_s": FILL_IN_HERE,
    "nominal_period_s": FILL_IN_HERE,
    "limits_s": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="alignment_skew",
        collect=skew,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
