"""One block: fan setpoint command ack."""

from __future__ import annotations

from pathlib import Path
from colosseum.context import get_context
from colosseum.decorators import VerificationResult

import colosseum as col

# SETUP:
#   SSH to DUT fan controller.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
ssh_id = FILL_IN_HERE
fan_set_command = FILL_IN_HERE  # str shell command


@col.verification
def verify_fan_ack(*, key: str) -> VerificationResult:
    """Require an exact OK acknowledgement and successful command exit."""
    row = get_context().db.get_measurement("messaging", "ssh.exec", key, row_index=0)
    if row is None or not isinstance(row.value, dict):
        raise ValueError("Missing SSH command result")
    result = row.value
    if type(result.get("exit_code")) is not int:
        raise ValueError("SSH result has no integer exit_code")
    if result["exit_code"] != 0:
        return VerificationResult(status="FAIL", message=f"Remote command failed: {result}")
    actual = result["stdout"].strip()
    return VerificationResult(status="PASS" if actual == "OK" else "FAIL", message=f"Expected exact OK acknowledgement, got {actual!r}", actual=actual)


def main() -> None:
    _load_bench()
    col.messaging.ssh.exec(ssh_id=ssh_id, command=fan_set_command, key="fan_ack")
    verify_fan_ack(key="fan_ack")


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
