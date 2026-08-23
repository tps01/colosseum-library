"""One block: I2C master write-read."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   SCK/SDA on header.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
i2c_id = FILL_IN_HERE
device_address = FILL_IN_HERE
write_hex = FILL_IN_HERE
read_len = FILL_IN_HERE
expected_hex = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.i2c.write_read(i2c_id=i2c_id, address=device_address, write=write_hex, read_len=read_len, key="i2c_data")
    col.shared.verify.verify_field(key="i2c_data", expected_val=expected_hex)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("bench.toml")))


if __name__ == "__main__":
    main()
    col.endex()
