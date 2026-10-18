"""One block: S11 at spot frequency."""

from __future__ import annotations

from pathlib import Path
from math import isfinite

import colosseum as col

# SETUP:
#   Marker at spot_freq_hz.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
vna_id = FILL_IN_HERE
start_hz = FILL_IN_HERE
stop_hz = FILL_IN_HERE
points = FILL_IN_HERE
source_power_dbm = FILL_IN_HERE
if_bw_hz = FILL_IN_HERE
spot_freq_hz = FILL_IN_HERE
s11_at_freq_db = FILL_IN_HERE  # signed MLOG S11 dB, not positive return loss
tolerance_db = FILL_IN_HERE


def main() -> None:
    if not all(isfinite(v) for v in (start_hz, stop_hz, spot_freq_hz, source_power_dbm, if_bw_hz, s11_at_freq_db, tolerance_db)) or if_bw_hz <= 0 or tolerance_db < 0 or type(points) is not int or points < 2:
        raise ValueError("Invalid VNA spot settings")
    if not 0 < start_hz <= spot_freq_hz <= stop_hz or start_hz == stop_hz:
        raise ValueError("Spot frequency must lie inside a positive sweep band")
    _load_bench()
    col.equipment.vna.set_trace_count(vna_id=vna_id, count=1)
    col.equipment.vna.set_trace_parameters(vna_id=vna_id, trace=1, parameter="S11", format="MLOG")
    col.equipment.vna.set_start_frequency(vna_id=vna_id, frequency_hz=start_hz)
    col.equipment.vna.set_stop_frequency(vna_id=vna_id, frequency_hz=stop_hz)
    col.equipment.vna.set_points(vna_id=vna_id, count=points)
    col.equipment.vna.set_tx_power(vna_id=vna_id, power_dbm=source_power_dbm, port=1)
    col.equipment.vna.set_if_bw(vna_id=vna_id, bandwidth_hz=if_bw_hz)
    col.equipment.vna.configure_trigger(vna_id=vna_id, source="IMM", continuous=False)
    col.equipment.vna.single_sweep(vna_id=vna_id)
    col.equipment.vna.set_marker(vna_id=vna_id, marker=1, frequency_hz=spot_freq_hz, trace=1)
    col.equipment.vna.measure_marker_value(vna_id=vna_id, marker=1, key="s11_spot")
    col.equipment.vna.verify_marker_value(key="s11_spot", expected_val=s11_at_freq_db, tolerance=tolerance_db)


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
