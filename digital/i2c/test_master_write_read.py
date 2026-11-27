"""Same isolated Aardvark/Beagle fixture. Use a documented read-only register address and known bytes. Capture repeated START."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.i2c.i2c_reference import i2c_register

SETTINGS = {
    "i2c_id": FILL_IN_HERE,
    "analyzer_id": FILL_IN_HERE,
    "address": FILL_IN_HERE,
    "clock_hz": FILL_IN_HERE,
    "sample_rate_hz": FILL_IN_HERE,
    "capture_settle_s": FILL_IN_HERE,
    "timeout_s": FILL_IN_HERE,
    "register_hex": FILL_IN_HERE,
    "expected_hex": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="master_write_read",
        collect=i2c_register,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
