"""One block: ping reachability."""

from __future__ import annotations

from pathlib import Path
from ipaddress import ip_address
from math import isfinite
import re
from shlex import quote
from colosseum.context import get_context
from colosseum.decorators import VerificationResult

import colosseum as col

# SETUP:
#   DUT reachable on LAN.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
dut_ip = FILL_IN_HERE
ping_count = FILL_IN_HERE
max_loss = FILL_IN_HERE  # percent, 0..100


@col.verification
def verify_packet_loss(*, key: str, maximum: float) -> VerificationResult:
    """Verify one Linux/iputils packet-loss summary, in percent, after exit 0."""
    if not isfinite(maximum) or not 0 <= maximum <= 100:
        raise ValueError("maximum packet loss must be 0..100 percent")
    row = get_context().db.get_measurement("messaging", "ssh.exec", key, row_index=0)
    if row is None or not isinstance(row.value, dict):
        raise ValueError("Missing SSH command result")
    result = row.value
    if type(result.get("exit_code")) is not int:
        raise ValueError("SSH result has no integer exit_code")
    if result["exit_code"] != 0:
        return VerificationResult(status="FAIL", message=f"Remote command failed: {result}")
    matches = re.findall(r"(?m)^.*?\b(\d+(?:\.\d+)?)% packet loss(?:,.*)?$", result["stdout"])
    if len(matches) != 1:
        raise ValueError("Expected exactly one iputils packet-loss summary")
    actual = float(matches[0])
    if not 0 <= actual <= 100:
        raise ValueError("Packet loss is outside 0..100 percent")
    return VerificationResult(status="PASS" if actual <= maximum else "FAIL", message=f"Packet loss {actual}% <= {maximum}%", actual=actual)


def main() -> None:
    _load_bench()
    if type(ping_count) is not int or ping_count < 1:
        raise ValueError("ping_count must be a positive integer")
    address = quote(str(ip_address(dut_ip)))
    col.messaging.ssh.exec(ssh_id=ssh_id, command=f"LC_ALL=C ping -n -c {ping_count} -- {address}", timeout=ping_count + 15.0, key="ping")
    verify_packet_loss(key="ping", maximum=max_loss)


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
