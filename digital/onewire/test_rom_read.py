"""One block: read 1-Wire ROM and verify."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   DQ on J_OW; powered bus.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
onewire_id = FILL_IN_HERE
expected_rom_hex = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.onewire.read_rom(onewire_id=onewire_id, key="rom")
    col.shared.verify.verify_field(key="rom", expected_val=expected_rom_hex)


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
