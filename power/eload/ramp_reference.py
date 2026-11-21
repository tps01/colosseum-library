"""Measure load-current ramp monotonicity from independent scope evidence."""

from statistics import fmean

import colosseum as col

from digital.waveform_reference import acquire, selected
from reference_common import number


def ramp(s):
    psu, load = s["psu_id"], s["eload_id"]
    initial, final = s["initial_a"], s["final_a"]
    scale = number(s["current_v_per_a"], "current monitor sensitivity")
    if not 0 <= initial < final or scale <= 0 or s["slew_a_per_s"] <= 0:
        raise col.ProceduralFault(
            "Use increasing current setpoints and positive sensitivity and slew"
        )
    try:
        col.equipment.psu.set_output(psu_id=psu, enabled=False)
        col.equipment.eload.disengage(eload_id=load)
        col.equipment.psu.set_voltage(psu_id=psu, voltage=s["supply_v"])
        col.equipment.psu.set_current_limit(psu_id=psu, current=s["current_limit_a"])
        col.equipment.eload.set_mode(eload_id=load, mode="CC")
        col.equipment.eload.set_slew_rate(eload_id=load, amps_per_s=s["slew_a_per_s"])
        col.equipment.eload.set_current(eload_id=load, current=initial)
        col.equipment.psu.set_output(psu_id=psu, enabled=True)
        col.equipment.psu.wait_for_voltage(
            psu_id=psu, voltage=s["supply_v"], timeout_s=s["timeout_s"]
        )
        col.equipment.eload.engage(eload_id=load)
        col.shared.wait(duration=s["settle_s"])

        def step():
            col.equipment.eload.set_current(eload_id=load, current=final)

        rail, monitor = acquire(s, s["channels"], "ramp", step)
        rail, monitor = selected(rail, s), selected(monitor, s)
        amps = [(v - s["current_zero_v"]) / scale for _, v in monitor]
        n = s["endpoint_samples"]
        if not 2 <= n or len(amps) <= 2 * n:
            raise col.ProceduralFault("Missing distinct start, ramp, and final samples")
        low, high = fmean(amps[:n]), fmean(amps[-n:])
        tolerance, noise = s["endpoint_tolerance_a"], s["noise_allowance_a"]
        if not 0 <= tolerance < (final - initial) / 2 or not 0 <= noise < final - initial:
            raise col.ProceduralFault("Endpoint and noise limits must resolve the ramp")
        interior = [i for i, a in enumerate(amps) if initial + tolerance < a < final - tolerance]
        endpoints = all(abs(a - initial) <= tolerance for a in amps[:n]) and all(
            abs(a - final) <= tolerance for a in amps[-n:]
        )
        if endpoints and len(interior) < s["min_transition_samples"]:
            raise col.ProceduralFault("Scope record does not resolve the current ramp")
        reversal = max(a - b for a, b in zip(amps, amps[1:]))
        floor = min(v for _, v in rail)
        return {
            "initial_a": low,
            "final_a": high,
            "largest_reverse_step_a": reversal,
            "minimum_rail_v": floor,
            "passed": endpoints and reversal <= noise and floor >= s["compliance_min_v"],
        }
    finally:
        try:
            col.equipment.eload.disengage(eload_id=load)
        finally:
            col.equipment.psu.set_output(psu_id=psu, enabled=False)
