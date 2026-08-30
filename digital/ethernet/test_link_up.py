"""One block: link up."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Cable to DUT NIC.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
dut_iface = FILL_IN_HERE  # str e.g. eth0


def main() -> None:
    _load_bench()
    col.host.net.measure_operstate(key="link", iface=dut_iface)
    col.host.net.verify_operstate_up(key="link", expected="up")


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
