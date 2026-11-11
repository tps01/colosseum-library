"""Fixture loopback continuity/stuck-level check, not a DUT functional-output test.
Required plugins: Equipment + Shared. Jumper output line -> independent input;
compatible common reference. Connect through the intended passive fixture path.
"""
from pathlib import Path
from math import isfinite
import colosseum as col

USE_AUTOCONFIG = False
dio_id = FILL_IN_HERE
out_line = FILL_IN_HERE
in_line = FILL_IN_HERE
settle_s = FILL_IN_HERE  # seconds per transition
PATTERN = [False, True, False, True]  # two full cycles reject stuck-low/high


@col.measurement
def measure_loopback(*, key: str, dio_id: int, out_line: int, in_line: int, settle_s: float) -> dict:
    if out_line == in_line or not isfinite(settle_s) or settle_s < 0:
        raise ValueError("Use distinct output/input lines and a nonnegative settling delay")
    col.io.dio.configure_pin(dio_id=dio_id, line=in_line, output=False)
    col.io.dio.configure_pin(dio_id=dio_id, line=out_line, output=True)
    observed = []
    try:
        for index, level in enumerate(PATTERN):
            col.io.dio.write_pin(dio_id=dio_id, line=out_line, value=level)
            col.shared.wait(duration=settle_s)
            value = col.io.dio.read_pin(dio_id=dio_id, line=in_line, key=f"{key}_{index}")
            observed.append(value)
        return {"expected": list(PATTERN), "observed": observed}
    finally:
        try:
            col.io.dio.write_pin(dio_id=dio_id, line=out_line, value=False)
        finally:
            col.io.dio.configure_pin(dio_id=dio_id, line=out_line, output=False)


def main() -> None:
    _load_bench()
    measure_loopback(key="loopback", dio_id=dio_id, out_line=out_line, in_line=in_line, settle_s=settle_s)
    col.shared.verify.verify_field(key="loopback", field="observed", expected_val=PATTERN)


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
