"""Acquire and qualify one unsmoothed analyzer trace for wideband measurements."""

import csv
from math import isfinite
from pathlib import Path

import colosseum as col
from colosseum.context import get_context


def capture_trace(
    *, speca_id, sweep_center_hz, sweep_span_hz, sweep_points, rbw_hz,
    vbw_hz, detector, attenuation_db, reference_dbm, key,
):
    if get_context().no_artifacts:
        raise col.ProceduralFault("Wideband trace analysis requires persisted artifacts")
    col.equipment.speca.preset(speca_id=speca_id)
    col.equipment.speca.set_continuous_sweep(speca_id=speca_id, enabled=False)
    col.equipment.speca.set_trigger_source(speca_id=speca_id, source="IMM")
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=sweep_center_hz)
    col.equipment.speca.set_span(speca_id=speca_id, span=sweep_span_hz)
    col.equipment.speca.set_sweep_points(speca_id=speca_id, count=sweep_points)
    col.equipment.speca.set_rbw(speca_id=speca_id, rbw=rbw_hz)
    col.equipment.speca.set_vbw(speca_id=speca_id, vbw=vbw_hz)
    col.equipment.speca.set_auto_attenuation(speca_id=speca_id, enabled=False)
    col.equipment.speca.set_attenuation_db(speca_id=speca_id, attenuation_db=attenuation_db)
    col.equipment.speca.toggle_preamp(speca_id=speca_id, enabled=False)
    col.equipment.speca.set_reference_level(speca_id=speca_id, level_dbm=reference_dbm)
    col.equipment.speca.set_detector(speca_id=speca_id, detector=detector)
    col.equipment.speca.set_trace_mode(speca_id=speca_id, trace=1, mode="WRIT")
    col.equipment.speca.single_sweep(speca_id=speca_id)
    relative_path = f"traces/{key}.csv"
    col.equipment.speca.save_trace_data(speca_id=speca_id, path=relative_path, trace=1, key=key)
    return str(Path(get_context().output_dir) / relative_path)


@col.command
def qualify_trace(*, path, start_hz, stop_hz, guard_hz, min_peak_dbm, max_guard_dbm):
    """Reject a missing, truncated, or unqualified trace before calculating a result."""
    limits = (start_hz, stop_hz, guard_hz, min_peak_dbm, max_guard_dbm)
    if (
        not all(isfinite(value) for value in limits)
        or not 0 < 2 * guard_hz < stop_hz - start_hz
        or max_guard_dbm >= min_peak_dbm
    ):
        raise col.ProceduralFault("Supply valid analysis bounds, guard widths and signal levels")

    with Path(path).open(encoding="utf-8", newline="") as handle:
        trace = [(float(row["frequency_hz"]), float(row["amplitude_dbm"])) for row in csv.DictReader(handle)]
    if not trace or not all(isfinite(f) and isfinite(p) for f, p in trace):
        raise col.ProceduralFault("The trace must contain finite frequency and power samples")
    if any(left[0] >= right[0] for left, right in zip(trace, trace[1:])):
        raise col.ProceduralFault("Trace frequencies must be strictly increasing")
    if trace[0][0] > start_hz or trace[-1][0] < stop_hz:
        raise col.ProceduralFault("The trace does not cover the analysis window")

    lower = [p for f, p in trace if start_hz <= f <= start_hz + guard_hz]
    upper = [p for f, p in trace if stop_hz - guard_hz <= f <= stop_hz]
    signal = [p for f, p in trace if start_hz + guard_hz < f < stop_hz - guard_hz]
    if not lower or not upper or not signal:
        raise col.ProceduralFault("The trace grid must sample the signal and both guard bands")
    if max(signal) < min_peak_dbm:
        raise col.ProceduralFault("No signal meets the minimum peak level inside the guard bands")
    if max(max(lower), max(upper)) > max_guard_dbm:
        raise col.ProceduralFault("Signal or interference exceeds the guard-band limit")
