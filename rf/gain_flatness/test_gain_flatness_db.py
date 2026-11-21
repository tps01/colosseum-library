"""Use a calibrated, linear VNA S21 fixture. Bench owns VNA stimulus. Preconfigure sweep, IFBW, point count, source level and calibration."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import gain_flatness

SETTINGS = {
    "vna_id": FILL_IN_HERE,
    "band_hz": FILL_IN_HERE,
    "max_spacing_hz": FILL_IN_HERE,
    "maximum_db": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="gain_flatness_db",
        collect=gain_flatness,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
