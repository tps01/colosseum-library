"""One block: throughput."""

from __future__ import annotations

from pathlib import Path
from ipaddress import ip_address
import json
from math import isfinite
from shlex import quote
from colosseum.context import get_context
from colosseum.decorators import VerificationResult

import colosseum as col

# SETUP:
#   iperf3 server on DUT.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
dut_ip = FILL_IN_HERE
min_throughput_mbps = FILL_IN_HERE
iperf_duration_s = FILL_IN_HERE


@col.verification
def verify_throughput(*, key: str, minimum: float) -> VerificationResult:
    """Compare iperf3 TCP receiver aggregate goodput to a decimal Mbit/s limit."""
    if not isfinite(minimum) or minimum < 0:
        raise ValueError("minimum throughput must be finite and nonnegative")
    row = get_context().db.get_measurement("messaging", "ssh.exec", key, row_index=0)
    if row is None or not isinstance(row.value, dict):
        raise ValueError("Missing SSH command result")
    result = row.value
    if type(result.get("exit_code")) is not int:
        raise ValueError("SSH result has no integer exit_code")
    if result["exit_code"] != 0:
        return VerificationResult(status="FAIL", message=f"Remote command failed: {result}")
    payload = json.loads(result["stdout"])
    if "error" in payload:
        return VerificationResult(status="FAIL", message=str(payload["error"]))
    value = payload["end"]["sum_received"]["bits_per_second"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("bits_per_second must be a JSON number")
    actual = float(value) / 1e6
    if not isfinite(actual) or actual < 0:
        raise ValueError("Throughput must be finite and nonnegative")
    return VerificationResult(status="PASS" if actual >= minimum else "FAIL", message=f"Receiver throughput {actual} Mbit/s >= {minimum}", actual=actual)


def main() -> None:
    _load_bench()
    if type(iperf_duration_s) is not int or iperf_duration_s < 1:
        raise ValueError("iperf_duration_s must be a positive integer")
    address = quote(str(ip_address(dut_ip)))
    col.messaging.ssh.exec(ssh_id=ssh_id, command=f"iperf3 -J -c {address} -t {iperf_duration_s}", timeout=iperf_duration_s + 15.0, key="iperf")
    verify_throughput(key="iperf", minimum=min_throughput_mbps)


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
