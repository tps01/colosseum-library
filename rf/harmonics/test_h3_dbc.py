"""Fixture owns stable CW stimulus, bias and generator power. Characterize source distortion and analyzer residual harmonics. Supply a path correction spanning the fundamental and harmonic."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import h3

SETTINGS = {
    "speca_id": FILL_IN_HERE,
    "output_correction": FILL_IN_HERE,
    "span_hz": FILL_IN_HERE,
    "rbw_hz": FILL_IN_HERE,
    "vbw_hz": FILL_IN_HERE,
    "attenuation_db": FILL_IN_HERE,
    "reference_dbm": FILL_IN_HERE,
    "settle_s": FILL_IN_HERE,
    "fundamental_hz": FILL_IN_HERE,
    "carrier_bounds_dbm": FILL_IN_HERE,
    "drift_max_db": FILL_IN_HERE,
    "harmonic_detection_dbm": FILL_IN_HERE,
    "maximum_dbc": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="h3_dbc", collect=h3, settings=SETTINGS, config=Path(__file__).with_name("config.toml")
    )


if __name__ == "__main__":
    main()
    col.endex()
