"""One block: SPI master transfer."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   SPI to DUT or EEPROM.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
spi_id = FILL_IN_HERE
cs = FILL_IN_HERE
mosi_hex = FILL_IN_HERE
read_len = FILL_IN_HERE
expected_hex = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.spi.transfer(spi_id=spi_id, cs=cs, mosi=mosi_hex, read_len=read_len, key="spi_miso")
    col.shared.verify.verify_field(key="spi_miso", expected_val=expected_hex)


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
