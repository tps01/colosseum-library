"""One block: throughput."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   iperf3 server on DUT.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
dut_ip = FILL_IN_HERE
min_throughput_mbps = FILL_IN_HERE
iperf_duration_s = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=f"iperf3 -c {dut_ip} -t {iperf_duration_s}", key="iperf")
    col.shared.regex.verify_match(key="iperf", pattern=r"Gbits/sec")


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
