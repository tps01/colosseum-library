"""Use two isolated sources and a combiner. Qualify both generator levels at DUT input, path corrections at all four output frequencies, and analyzer/sources for linearity. Both levels must stay within DUT ratings."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import oip3

SETTINGS = {
    "speca_id": FILL_IN_HERE,
    "output_correction": FILL_IN_HERE,
    "span_hz": FILL_IN_HERE,
    "rbw_hz": FILL_IN_HERE,
    "vbw_hz": FILL_IN_HERE,
    "attenuation_db": FILL_IN_HERE,
    "reference_dbm": FILL_IN_HERE,
    "settle_s": FILL_IN_HERE,
    "vsg1_id": FILL_IN_HERE,
    "vsg2_id": FILL_IN_HERE,
    "f1_hz": FILL_IN_HERE,
    "f2_hz": FILL_IN_HERE,
    "low_generator_dbm": FILL_IN_HERE,
    "level_step_db": FILL_IN_HERE,
    "slope_tolerance_db": FILL_IN_HERE,
    "balance_max_db": FILL_IN_HERE,
    "im3_detection_dbm": FILL_IN_HERE,
    "minimum_dbm": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="oip3_dbm",
        collect=oip3,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
