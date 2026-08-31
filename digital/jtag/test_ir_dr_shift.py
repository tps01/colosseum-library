"""One block: JTAG DR readback."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Known IR loaded.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
jtag_id = FILL_IN_HERE
ir_hex = FILL_IN_HERE
expected_dr = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.jtag.shift_dr(jtag_id=jtag_id, ir=ir_hex, key="dr")
    col.shared.verify.verify_field(key="dr", expected_val=expected_dr)


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
