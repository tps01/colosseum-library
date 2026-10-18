"""One-shot load responses; Equipment 0.5.0+ and Shared 0.5.0+.

Rail and current-monitor CSVs must be from the same acquisition. Event time is
the measured load-current threshold crossing, not the host command timestamp.
"""
from pathlib import Path
from math import isfinite
import csv

import colosseum as col
from colosseum.context import get_context
from colosseum.decorators import VerificationResult


def analyze_response(rail_path, current_path, *, metric, target_v, trigger_v, increasing, pre_s, observation_s, steady_tolerance_v, settle_band_v, hold_s, initial_a, final_a, current_v_per_a, current_zero_v, current_tolerance_a):
    def read(path):
        with Path(path).open(encoding="utf-8", newline="") as handle:
            points = [(float(r["time_s"]), float(r["voltage_v"])) for r in csv.DictReader(handle)]
        if len(points) < 4 or not all(isfinite(x) for point in points for x in point):
            raise ValueError("Waveforms must contain finite samples")
        if any(b[0] <= a[0] for a, b in zip(points, points[1:])):
            raise ValueError("Waveform time must increase strictly")
        return points
    rail, current = read(rail_path), read(current_path)
    if [p[0] for p in rail] != [p[0] for p in current]:
        raise ValueError("Rail and current captures must share a time axis; deskew probes first")
    crossings = []
    for (ta, a), (tb, b) in zip(current, current[1:]):
        crossed = (a < trigger_v <= b) if increasing else (a > trigger_v >= b)
        if crossed:
            crossings.append(ta + (tb-ta) * (trigger_v-a) / (b-a))
    if len(crossings) != 1:
        raise ValueError("Expected exactly one load-current threshold crossing")
    event = crossings[0]
    if rail[0][0] > event-pre_s or rail[-1][0] < event+observation_s:
        raise ValueError("Capture does not cover the required pre/post-event windows")
    pre = [v for t, v in rail if event-pre_s <= t < event]
    post = [(t-event, v) for t, v in rail if event <= t <= event+observation_s]
    if len(pre) < 2 or len(post) < 2:
        raise ValueError("Insufficient samples to resolve the response")
    if any(abs(v-target_v) > steady_tolerance_v for v in pre):
        raise ValueError("Rail was not stable at its required target before the step")
    for start, stop, expected, include_stop in ((event-pre_s, event, initial_a, False), (event+observation_s-hold_s, event+observation_s, final_a, True)):
        measured = [(v-current_zero_v)/current_v_per_a for t, v in current if start <= t and (t <= stop if include_stop else t < stop)]
        if len(measured) < 2 or any(abs(a-expected) > current_tolerance_a for a in measured):
            raise ValueError("Current monitor does not confirm the requested load level")
    if metric == "overshoot_mv":
        return {"value": max(0.0, (max(v for _, v in post)-target_v)*1000), "unit": "mV"}
    if metric == "undershoot_mv":
        return {"value": max(0.0, (target_v-min(v for _, v in post))*1000), "unit": "mV"}
    if metric != "settle_ms":
        raise ValueError("Unknown response metric")
    outside = [i for i, (_, v) in enumerate(post) if abs(v-target_v) > settle_band_v]
    candidate = outside[-1]+1 if outside else 0
    settled = candidate < len(post) and post[-1][0]-post[candidate][0] >= hold_s
    return {"settled": settled, "value": post[candidate][0]*1000 if settled else None, "unit": "ms"}


@col.measurement
def measure_response(*, key: str, metric: str, settings: dict) -> dict:
    """Record a response metric plus raw same-capture rail/current waveforms."""
    s = settings
    if metric not in ("overshoot_mv", "undershoot_mv", "settle_ms"):
        raise ValueError("Unknown response metric")
    if not all(not isinstance(value, bool) and isfinite(value) for value in s.values()):
        raise ValueError("All response settings must be finite numbers")
    if s["rail_channel"] == s["current_channel"] or s["initial_a"] == s["final_a"]:
        raise ValueError("Use distinct channels and a nonzero load step")
    if min(s["supply_v"], s["current_limit_a"], s["target_v"], s["slew_a_per_s"], s["pre_s"], s["observation_s"], s["hold_s"], s["settle_band_v"], s["steady_tolerance_v"], s["timebase_s_per_div"], s["acquire_timeout_s"], s["current_v_per_a"], s["current_tolerance_a"], s["rail_probe_ratio"], s["current_probe_ratio"], s["rail_scale_v"], s["current_scale_v"]) <= 0 or min(s["initial_a"], s["final_a"], s["settle_s"], s["arm_delay_s"]) < 0:
        raise ValueError("Invalid source, timing or load limits")
    if type(s["record_points"]) is not int or s["record_points"] < 4 or any(type(s[k]) is not int or s[k] < 1 for k in ("rail_channel", "current_channel")):
        raise ValueError("Use integer scope channels and a sufficient record length")
    monitor_levels = [s["current_zero_v"] + s["current_v_per_a"]*s[k] for k in ("initial_a", "final_a")]
    if not min(monitor_levels) < s["trigger_v"] < max(monitor_levels):
        raise ValueError("Current trigger threshold must lie strictly between the two load levels")
    if s["hold_s"] > s["observation_s"]:
        raise ValueError("Hold duration exceeds the observation window")
    increasing = s["final_a"] > s["initial_a"]
    if (metric == "overshoot_mv" and increasing) or (metric == "undershoot_mv" and not increasing):
        raise ValueError("Overshoot uses load release; undershoot uses increasing load")
    ctx = get_context()
    if ctx.output_dir is None:
        raise ValueError("Response capture requires persisted output (no-artifacts is unsupported)")
    rail_path = str(Path(ctx.output_dir)/f"{key}_rail.csv")
    current_path = str(Path(ctx.output_dir)/f"{key}_current.csv")
    psu, load, scope = s["psu_id"], s["eload_id"], s["oscope_id"]
    try:
        col.equipment.eload.disengage(eload_id=load)
        col.equipment.psu.set_output(psu_id=psu, enabled=False)
        col.equipment.eload.preset(eload_id=load)
        col.equipment.psu.set_current_limit(psu_id=psu, current=s["current_limit_a"])
        col.equipment.psu.set_voltage(psu_id=psu, voltage=s["supply_v"])
        col.equipment.eload.set_mode(eload_id=load, mode="CC")
        col.equipment.eload.set_slew_rate(eload_id=load, amps_per_s=s["slew_a_per_s"])
        col.equipment.eload.set_current(eload_id=load, current=s["initial_a"])
        col.equipment.psu.set_output(psu_id=psu, enabled=True)
        col.equipment.psu.wait_for_voltage(psu_id=psu, voltage=s["supply_v"], timeout_s=s["acquire_timeout_s"])
        col.equipment.eload.engage(eload_id=load)
        col.shared.wait(duration=s["settle_s"])
        col.equipment.oscope.preset(oscope_id=scope)
        for channel, ratio, scale, offset in ((s["rail_channel"], s["rail_probe_ratio"], s["rail_scale_v"], s["rail_offset_v"]), (s["current_channel"], s["current_probe_ratio"], s["current_scale_v"], 0.0)):
            col.equipment.oscope.set_channel_display(oscope_id=scope, channel=channel, enabled=True)
            col.equipment.oscope.set_channel_coupling(oscope_id=scope, channel=channel, coupling="DC")
            col.equipment.oscope.set_channel_impedance(oscope_id=scope, channel=channel, ohms=1e6)
            col.equipment.oscope.set_channel_probe_attenuation(oscope_id=scope, channel=channel, attenuation=ratio)
            col.equipment.oscope.set_channel_scale_v(oscope_id=scope, channel=channel, volts_per_div=scale)
            col.equipment.oscope.set_channel_offset_v(oscope_id=scope, channel=channel, offset_v=offset)
        col.equipment.oscope.set_timebase_scale(oscope_id=scope, seconds_per_div=s["timebase_s_per_div"])
        col.equipment.oscope.set_record_length(oscope_id=scope, points=s["record_points"])
        col.equipment.oscope.set_acquire_mode(oscope_id=scope, mode="sample")
        col.equipment.oscope.set_trigger_source(oscope_id=scope, source=f"CH{s['current_channel']}")
        col.equipment.oscope.set_trigger_level_v(oscope_id=scope, level_v=s["trigger_v"])
        col.equipment.oscope.set_trigger_slope(oscope_id=scope, slope="rising" if increasing else "falling")
        col.equipment.oscope.set_trigger_mode(oscope_id=scope, mode="normal")
        col.equipment.oscope.arm_single(oscope_id=scope)
        col.shared.wait(duration=s["arm_delay_s"])
        col.equipment.eload.set_current(eload_id=load, current=s["final_a"])
        col.equipment.oscope.wait_complete(oscope_id=scope, timeout_s=s["acquire_timeout_s"])
        col.equipment.oscope.save_waveform(oscope_id=scope, channel=s["rail_channel"], path=rail_path)
        col.equipment.oscope.save_waveform(oscope_id=scope, channel=s["current_channel"], path=current_path)
        return analyze_response(rail_path, current_path, metric=metric, target_v=s["target_v"], trigger_v=s["trigger_v"], increasing=increasing, pre_s=s["pre_s"], observation_s=s["observation_s"], steady_tolerance_v=s["steady_tolerance_v"], settle_band_v=s["settle_band_v"], hold_s=s["hold_s"], initial_a=s["initial_a"], final_a=s["final_a"], current_v_per_a=s["current_v_per_a"], current_zero_v=s["current_zero_v"], current_tolerance_a=s["current_tolerance_a"])
    finally:
        try:
            col.equipment.oscope.abort(oscope_id=scope)
        finally:
            try:
                col.equipment.eload.disengage(eload_id=load)
            finally:
                col.equipment.psu.set_output(psu_id=psu, enabled=False)


@col.verification
def verify_response(*, key: str, maximum: float) -> VerificationResult:
    if not isfinite(maximum) or maximum < 0:
        raise ValueError("Response limit must be finite and nonnegative")
    row = get_context().db.get_measurement("core", "measure_response", key, row_index=0)
    if row is None or not isinstance(row.value, dict):
        raise ValueError("Missing response evidence")
    if row.value.get("settled") is False:
        return VerificationResult(status="FAIL", message="Rail did not settle for the required hold within the observation window")
    actual = float(row.value["value"])
    if not isfinite(actual) or actual < 0:
        raise ValueError("Invalid response metric")
    return VerificationResult(status="PASS" if actual <= maximum else "FAIL", actual=actual, message=f"{actual} {row.value['unit']} <= {maximum}")
