"""One block: parasitic power read."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   No explicit Vdd; strong pull-up.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
onewire_id = FILL_IN_HERE
expected_byte = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.onewire.read_byte(onewire_id=onewire_id, key="parasitic_byte")
    col.shared.verify.verify_field(key="parasitic_byte", expected_val=expected_byte)


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
