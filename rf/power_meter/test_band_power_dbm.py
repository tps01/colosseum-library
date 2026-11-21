"""Preconfigure a supported analyzer in native channel-power mode with the stated integration bandwidth. Verify in-band and out-of-band references. Use a qualified flat path, and keep the mode through a completed acquisition."""

from pathlib import Path

import colosseum as col

from reference_common import required
from rf.rf_reference import channel_power

SETTINGS = {
    "speca_id": FILL_IN_HERE,
    "flat_path_loss_db": FILL_IN_HERE,
    "verified_center_hz": FILL_IN_HERE,
    "verified_bandwidth_hz": FILL_IN_HERE,
    "limits_dbm": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="band_power_dbm",
        collect=channel_power,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
