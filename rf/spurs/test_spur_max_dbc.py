"""Preconfigure the analyzer for repeatable single sweeps with a fixed grid, RBW and detector. Qualify the output path, detector and worst-case detection level. Explicitly exclude the carrier, harmonic and modulation windows."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import spur

SETTINGS = {
    "speca_id": FILL_IN_HERE,
    "output_correction": FILL_IN_HERE,
    "band_hz": FILL_IN_HERE,
    "exclude_hz": FILL_IN_HERE,
    "carrier_window_hz": FILL_IN_HERE,
    "observation_s": FILL_IN_HERE,
    "min_sweeps": FILL_IN_HERE,
    "max_sweeps": FILL_IN_HERE,
    "max_spacing_hz": FILL_IN_HERE,
    "carrier_drift_db": FILL_IN_HERE,
    "carrier_bounds_dbm": FILL_IN_HERE,
    "detection_dbm": FILL_IN_HERE,
    "maximum_dbc": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="spur_max_dbc",
        collect=spur,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
