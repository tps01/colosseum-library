"""One block: 2nd harmonic dBc."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   Span covers 2×f0.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
speca_id = FILL_IN_HERE
fundamental_hz = FILL_IN_HERE
max_h2_dbc = FILL_IN_HERE


def main() -> None:
    _load_bench()
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=2 * fundamental_hz)
    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
    col.shared.signal.measure_harmonic_dbc(speca_id=speca_id, fundamental_hz=fundamental_hz, harmonic=2, key="h2_dbc")
    col.shared.verify.verify_field(key="h2_dbc", expected_val=max_h2_dbc, tolerance=0.0)


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
