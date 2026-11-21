"""Use independently calibrated input and output taps/meters; qualify analyzer and source linearity and DUT power, current, recovery and thermal conditions across the sweep."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import p1db

SETTINGS = {
    "vsg_id": FILL_IN_HERE,
    "pwrmeter_ids": FILL_IN_HERE,
    "generator_steps_dbm": FILL_IN_HERE,
    "qualified_generator_bounds_dbm": FILL_IN_HERE,
    "input_correction": FILL_IN_HERE,
    "output_correction": FILL_IN_HERE,
    "frequency_hz": FILL_IN_HERE,
    "settle_s": FILL_IN_HERE,
    "small_signal_points": FILL_IN_HERE,
    "max_fit_residual_db": FILL_IN_HERE,
    "small_signal_slope_bounds": FILL_IN_HERE,
    "limits_dbm": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="p1db_compression_dbm",
        collect=p1db,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
