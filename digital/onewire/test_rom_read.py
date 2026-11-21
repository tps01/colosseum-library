"""Externally powered single DS18B20, DS9481R and standard-speed pull-up. Use the full eight-byte ROM in wire order."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.onewire.onewire_reference import onewire_rom

SETTINGS = {
    "onewire_id": FILL_IN_HERE,
    "expected_rom_hex": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="rom_read",
        collect=onewire_rom,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
