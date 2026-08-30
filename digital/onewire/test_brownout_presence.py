"""One block: presence above brownout V."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   PSU on 1-Wire Vdd.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
onewire_id = FILL_IN_HERE
psu_id = FILL_IN_HERE
min_presence_v = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=min_presence_v)
    col.io.onewire.verify_presence(onewire_id=onewire_id, key="presence")
    col.shared.verify.verify_measurement_exists(key="presence")


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
