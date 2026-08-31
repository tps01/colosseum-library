"""One block: clock frequency."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Scope or counter on CLK_OUT.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
freqcounter_id = FILL_IN_HERE
expected_freq_hz = FILL_IN_HERE
freq_tolerance_hz = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.freqcounter.measure_frequency(freqcounter_id=freqcounter_id, key="clk_hz")
    col.equipment.freqcounter.verify_frequency(key="clk_hz", expected_val=expected_freq_hz, tolerance=freq_tolerance_hz)


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
