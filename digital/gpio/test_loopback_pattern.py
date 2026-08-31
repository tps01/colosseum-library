"""One block: GPIO loopback pattern."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Loopback jumper J_GPIO_LB.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
dio_id = FILL_IN_HERE
out_line = FILL_IN_HERE
in_line = FILL_IN_HERE
direction_mask = FILL_IN_HERE
expected_read = FILL_IN_HERE  # bool


def main() -> None:
    _load_bench()
    col.io.dio.configure(dio_id=dio_id, direction=direction_mask)
    col.io.dio.write_pin(dio_id=dio_id, line=out_line, value=True)
    col.io.dio.read_pin(dio_id=dio_id, line=in_line, key="loopback")
    col.shared.verify.verify_field(key="loopback", expected_val=expected_read)


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
