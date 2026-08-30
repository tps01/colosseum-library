"""One block: monotonic current ramp."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Simulate inductive load profile.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
eload_id = FILL_IN_HERE
i_start_a = FILL_IN_HERE
i_stop_a = FILL_IN_HERE
ramp_rate_a_per_s = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.shared.signal.ramp_eload_current(eload_id=eload_id, i_start_a=i_start_a, i_stop_a=i_stop_a, rate_a_per_s=ramp_rate_a_per_s, key="ramp_ok")
    col.shared.verify.verify_field(key="ramp_ok", expected_val=True)


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
