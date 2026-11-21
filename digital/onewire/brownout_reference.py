"""Measure 1-Wire presence across an externally powered supply sweep."""

from statistics import fmean

import colosseum as col

from digital.waveform_reference import acquire, edges, selected
from reference_common import bounds


def presence(rows, s):
    transitions = edges(rows, s["threshold_v"], s["hysteresis_v"])
    if len(transitions) not in (2, 4) or [kind for _, kind in transitions] != ["fall", "rise"] * (
        len(transitions) // 2
    ):
        raise col.ProceduralFault("Missing reset or ambiguous bus transitions")
    t = [x for x, _ in transitions]
    if not bounds(t[1] - t[0], s["reset_width_s"]) or rows[-1][0] - t[1] < sum(
        (s["presence_delay_s"][1], s["presence_width_s"][1])
    ):
        raise col.ProceduralFault("Reset pulse or following acquisition window is invalid")
    if len(t) == 2:
        return {"present": False, "reset_width_s": t[1] - t[0]}
    delay, width = t[2] - t[1], t[3] - t[2]
    if not bounds(delay, s["presence_delay_s"]) or not bounds(width, s["presence_width_s"]):
        raise col.ProceduralFault("Pulse lies outside the qualified presence timing")
    return {"present": True, "delay_s": delay, "width_s": width}


def brownout(s):
    psu, device = s["psu_id"], s["onewire_id"]
    levels = s["levels_v"]
    if len(levels) < 2 or any(a <= b for a, b in zip(levels, levels[1:])) or s["repeats"] < 2:
        raise col.ProceduralFault("Use descending voltage steps and repeated observations")
    facts = []

    def reset():
        col.io.onewire.reset(onewire_id=device, required=False)

    def measure_leg(sequence, label):
        results = []
        for i, volts in enumerate(sequence):
            col.equipment.psu.set_voltage(psu_id=psu, voltage=volts)
            col.shared.wait(duration=s["settle_s"])
            rows = []
            for attempt in range(s["repeats"]):
                rail, bus = acquire(s, s["channels"], f"{label}_{i}_{attempt}", reset)
                verdict = presence(selected(bus, s), s)
                rail = selected(rail, s)
                if any(abs(v - volts) > s["step_tolerance_v"] for _, v in rail):
                    raise col.ProceduralFault(
                        "Measured supply did not hold the requested step level"
                    )
                rows.append(verdict | {"volts": fmean(v for _, v in rail)})
            facts.append({"leg": label, "setpoint_v": volts, "samples": rows})
            states = {row["present"] for row in rows}
            if len(states) != 1:
                raise col.ProceduralFault("Presence is inconsistent at a supply step")
            results.append((fmean(row["volts"] for row in rows), states.pop()))
        return results

    def bracket(rows):
        transitions = [(a, b) for a, b in zip(rows, rows[1:]) if a[1] != b[1]]
        if len(transitions) != 1:
            raise col.ProceduralFault("Supply sweep did not bracket one presence transition")
        a, b = transitions[0]
        interval = sorted([a[0], b[0]])
        if interval[1] - interval[0] > s["maximum_bracket_width_v"]:
            raise col.ProceduralFault("Measured threshold bracket is too wide")
        return interval

    try:
        col.equipment.psu.set_output(psu_id=psu, enabled=False)
        col.equipment.psu.set_voltage(psu_id=psu, voltage=levels[0])
        col.equipment.psu.set_current_limit(psu_id=psu, current=s["current_limit_a"])
        col.io.onewire.configure(onewire_id=device, speed="standard")
        col.equipment.psu.set_output(psu_id=psu, enabled=True)
        down = measure_leg(levels, "down")
        up = measure_leg(list(reversed(levels)), "up")
        if not down[0][1] or down[-1][1] or up[0][1]:
            raise col.ProceduralFault("Fixture did not produce a qualified brownout starting state")
        down_window = bracket(down)
        recovered = up[-1][1]
        up_window = bracket(up) if recovered else None
        passed = recovered and all(
            bounds(v, s["threshold_limits_v"]) for v in down_window + up_window
        )
        col.equipment.psu.set_output(psu_id=psu, enabled=False)
        col.shared.wait(duration=s["recovery_off_s"])
        col.equipment.psu.set_voltage(psu_id=psu, voltage=levels[0])
        col.equipment.psu.set_output(psu_id=psu, enabled=True)
        cycle = measure_leg([levels[0]], "power_cycle")
        return {
            "falling_bracket_v": down_window,
            "rising_bracket_v": up_window,
            "observations": facts,
            "passed": bool(passed and cycle[0][1]),
        }
    finally:
        col.equipment.psu.set_output(psu_id=psu, enabled=False)
