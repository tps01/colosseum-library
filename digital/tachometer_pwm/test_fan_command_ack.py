"""One block: fan setpoint command ack."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   SSH to DUT fan controller.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
fan_set_command = FILL_IN_HERE  # str shell command


def main() -> None:
    _load_bench()
    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=fan_set_command, key="fan_ack")
    col.shared.regex.verify_match(key="fan_ack", pattern=r"OK")


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
