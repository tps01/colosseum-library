"""Aardvark master and passive Beagle. Isolate one 7-bit target, qualify pull-ups and verify address-only STOP with no payload."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.i2c.i2c_reference import i2c_probe

SETTINGS = {
    "i2c_id": FILL_IN_HERE,
    "analyzer_id": FILL_IN_HERE,
    "address": FILL_IN_HERE,
    "clock_hz": FILL_IN_HERE,
    "sample_rate_hz": FILL_IN_HERE,
    "capture_settle_s": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="slave_ack",
        collect=i2c_probe,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
