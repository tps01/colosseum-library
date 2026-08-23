"""One block: GPIO output high."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   DIO line as output.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
dio_id = FILL_IN_HERE
line = FILL_IN_HERE
direction_mask = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.dio.configure(dio_id=dio_id, direction=direction_mask)
    col.io.dio.write_pin(dio_id=dio_id, line=line, value=True)
    col.io.dio.read_pin(dio_id=dio_id, line=line, key="pin_high")
    col.shared.verify.verify_field(key="pin_high", expected_val=True)


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
