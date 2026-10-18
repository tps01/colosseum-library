"""One block: bit error rate."""

from __future__ import annotations

from pathlib import Path
import json
from math import isfinite
from colosseum.context import get_context
from colosseum.decorators import VerificationResult

import colosseum as col

# SETUP:
#   DUT PHY self-test command.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
ber_max = FILL_IN_HERE
dut_ber_command = FILL_IN_HERE  # str; stdout JSON {"ber": <fraction 0..1>}, exit 0


@col.verification
def verify_ber(*, key: str, maximum: float) -> VerificationResult:
    """DUT command must return exit 0 and a JSON object with numeric `ber`."""
    if not isfinite(maximum) or not 0 <= maximum <= 1:
        raise ValueError("maximum BER must be a fraction in 0..1")
    row = get_context().db.get_measurement("messaging", "ssh.exec", key, row_index=0)
    if row is None or not isinstance(row.value, dict):
        raise ValueError("Missing SSH command result")
    result = row.value
    if type(result.get("exit_code")) is not int:
        raise ValueError("SSH result has no integer exit_code")
    if result["exit_code"] != 0:
        return VerificationResult(status="FAIL", message=f"Remote command failed: {result}")
    payload = json.loads(result["stdout"])
    value = payload["ber"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("ber must be a JSON number")
    actual = float(value)
    if not isfinite(actual) or not 0 <= actual <= 1:
        raise ValueError("BER must be finite and in 0..1")
    return VerificationResult(status="PASS" if actual <= maximum else "FAIL", message=f"BER {actual} <= {maximum}", actual=actual)


def main() -> None:
    _load_bench()
    col.messaging.ssh.exec(ssh_id=ssh_id, command=dut_ber_command, key="ber")
    verify_ber(key="ber", maximum=ber_max)


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
