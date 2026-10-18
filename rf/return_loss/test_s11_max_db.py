"""Worst passive-path return_loss_db over the requested band, from signed MLOG data.
Equipment + Shared required. Calibrate at DUT connector reference planes first.
VNA port 1 -> DUT input, port 2 -> DUT output (terminate output for S11 as specified).
"""
from pathlib import Path
from math import isfinite, isclose
import csv
import colosseum as col
from colosseum.context import get_context

USE_AUTOCONFIG = False
vna_id = FILL_IN_HERE
start_hz = FILL_IN_HERE
stop_hz = FILL_IN_HERE
points = FILL_IN_HERE
source_power_dbm = FILL_IN_HERE  # VNA source port dBm
if_bw_hz = FILL_IN_HERE  # Hz
min_return_loss_db = FILL_IN_HERE  # positive dB loss convention


@col.measurement
def measure_return_loss_db(*, key: str, vna_id: int, start_hz: float, stop_hz: float, points: int, source_power_dbm: float, if_bw_hz: float) -> float:
    if not all(isfinite(v) for v in (start_hz, stop_hz, source_power_dbm, if_bw_hz)) or not 0 < start_hz < stop_hz or if_bw_hz <= 0 or type(points) is not int or points < 2:
        raise ValueError("Invalid VNA band, point count or source settings")
    ctx = get_context()
    if ctx.output_dir is None:
        raise ValueError("VNA band analysis requires persisted CSV output")
    path = Path(ctx.output_dir)/f"{key}.csv"
    col.equipment.vna.set_trace_count(vna_id=vna_id, count=1)
    col.equipment.vna.set_trace_parameters(vna_id=vna_id, trace=1, parameter="S11", format="MLOG")
    col.equipment.vna.set_start_frequency(vna_id=vna_id, frequency_hz=start_hz)
    col.equipment.vna.set_stop_frequency(vna_id=vna_id, frequency_hz=stop_hz)
    col.equipment.vna.set_points(vna_id=vna_id, count=points)
    col.equipment.vna.set_if_bw(vna_id=vna_id, bandwidth_hz=if_bw_hz)
    col.equipment.vna.set_tx_power(vna_id=vna_id, power_dbm=source_power_dbm, port=1)
    col.equipment.vna.configure_trigger(vna_id=vna_id, source="IMM", continuous=False)
    # Export performs and waits for its own new sweep; do not add a second sweep.
    col.equipment.vna.save_trace_data(vna_id=vna_id, path=str(path), trace=1, file_format="csv", parameter="S11")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [(float(r["frequency_hz"]), float(r["value"])) for r in csv.DictReader(handle)]
    if len(rows) != points or not all(isfinite(x) for row in rows for x in row):
        raise ValueError("Incomplete or non-finite VNA trace")
    if any(b[0] <= a[0] for a, b in zip(rows, rows[1:])) or not isclose(rows[0][0], start_hz, rel_tol=1e-9, abs_tol=1e-6) or not isclose(rows[-1][0], stop_hz, rel_tol=1e-9, abs_tol=1e-6):
        raise ValueError("Trace does not match the requested sweep band")
    values = [v for _, v in rows]
    return -max(values)


def main() -> None:
    if not isfinite(min_return_loss_db) or min_return_loss_db < 0:
        raise ValueError("Use the positive-loss dB limit convention")
    _load_bench()
    measure_return_loss_db(key="return_loss_db", vna_id=vna_id, start_hz=start_hz, stop_hz=stop_hz, points=points, source_power_dbm=source_power_dbm, if_bw_hz=if_bw_hz)
    col.shared.verify.verify_field(key="return_loss_db", minimum=min_return_loss_db)


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
