"""One block: CW peak marker frequency."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   VSG CW into DUT; SA on output.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
center_freq_hz = FILL_IN_HERE
freq_tolerance_hz = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=center_freq_hz)
    col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)
    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
    col.equipment.speca.measure_marker_frequency(speca_id=speca_id, marker=1, key="peak_f")
    col.equipment.speca.verify_marker_frequency(key="peak_f", expected_val=center_freq_hz, tolerance=freq_tolerance_hz)


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
