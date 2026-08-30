"""One block: JTAG IDCODE."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   JTAG adapter to DUT.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
jtag_id = FILL_IN_HERE
expected_idcode = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.io.jtag.read_idcode(jtag_id=jtag_id, key="idcode")
    col.shared.verify.verify_field(key="idcode", expected_val=expected_idcode)


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
