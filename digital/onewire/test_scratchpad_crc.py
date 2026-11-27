"""Same externally powered single-drop fixture. Verify a full DS18B20 scratchpad after conversion."""

from pathlib import Path

import colosseum as col

from reference_common import required
from digital.onewire.onewire_reference import onewire_scratchpad

SETTINGS = {
    "onewire_id": FILL_IN_HERE,
    "expected_rom_hex": FILL_IN_HERE,
}


def main() -> None:
    required(
        key="scratchpad_crc",
        collect=onewire_scratchpad,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
