"""One block: bit error rate."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   DUT PHY self-test command.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
ber_max = FILL_IN_HERE
dut_ber_command = FILL_IN_HERE  # str


def main() -> None:
    _load_bench()
    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=dut_ber_command, key="ber")
    col.shared.regex.verify_match(key="ber", pattern=r"BER")


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
