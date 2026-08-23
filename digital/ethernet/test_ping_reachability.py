"""One block: ping reachability."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   DUT reachable on LAN.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
dut_ip = FILL_IN_HERE
ping_count = FILL_IN_HERE
max_loss = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=f"ping -c {ping_count} {dut_ip}", key="ping")
    col.shared.regex.verify_match(key="ping", pattern=r"0% packet loss")


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
