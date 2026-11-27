"""Prepare a stable DUT and fixed qualified analyzer sweep. Use a frequency JSON mask with absolute Hz and dBm keep_below regions."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import mask_margin

SETTINGS = {
    "speca_id": FILL_IN_HERE,
    "mask_path": FILL_IN_HERE,
    "output_correction": FILL_IN_HERE,
    "max_spacing_hz": FILL_IN_HERE,
    "minimum_db": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="mask_margin_db",
        collect=mask_margin,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
