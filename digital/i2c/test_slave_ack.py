"""One block: I2C address ACK."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Device on bus.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
i2c_id = FILL_IN_HERE
device_address = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.i2c.probe(i2c_id=i2c_id, address=device_address, key="i2c_ack")
    col.shared.verify.verify_field(key="i2c_ack", expected_val=True)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


if __name__ == "__main__":
    main()
    col.endex()
