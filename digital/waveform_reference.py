"""Analysis of same-acquisition scope exports from a prequalified scope setup."""

from bisect import bisect_left, bisect_right
from math import isclose, sqrt
from statistics import fmean

import colosseum as col

from reference_common import bounds, number, output_path, trace, window


def acquire(s, channels, stem, stimulus=None):
    scope = s["oscope_id"]
    timeout = number(s["timeout_s"], "scope timeout")
    if timeout <= 0 or len(set(channels)) != len(channels):
        raise col.ProceduralFault("Use a positive timeout and distinct scope channels")
    col.equipment.oscope.arm_single(oscope_id=scope)
    try:
        if stimulus is not None:
            col.shared.wait(duration=s["arm_delay_s"])
            stimulus()
        col.equipment.oscope.wait_complete(oscope_id=scope, timeout_s=timeout)
        result = []
        for channel in channels:
            path = f"traces/{stem}_ch{channel}.csv"
            col.equipment.oscope.save_waveform(
                oscope_id=scope,
                channel=channel,
                path=str(output_path(path)),
                key=f"{stem}_ch{channel}",
            )
            samples = trace(path, "time_s", "voltage_v")
            if not all(bounds(v, s["probe_valid_v"]) for _, v in samples):
                raise col.ProceduralFault("Waveform exceeds the qualified unclipped probe range")
            result.append(samples)
        if any([t for t, _ in rows] != [t for t, _ in result[0]] for rows in result[1:]):
            raise col.ProceduralFault("Scope exports do not share a common time axis")
        return result
    finally:
        col.equipment.oscope.abort(oscope_id=scope)


def selected(rows, s):
    start, stop = s["window_s"]
    return window(rows, start, stop, s["max_sample_spacing_s"])


def edges(rows, threshold, hysteresis):
    """Arm beyond the hysteresis limits and timestamp the interpolated midpoint."""
    threshold = number(threshold, "threshold")
    half = number(hysteresis, "hysteresis") / 2
    if half <= 0:
        raise col.ProceduralFault("Use positive edge hysteresis")
    low, high = threshold - half, threshold + half
    state = None
    crossing = None
    result = []
    for (t0, v0), (t1, v1) in zip(rows, rows[1:]):
        if state is None:
            state = "low" if v0 <= low else "high" if v0 >= high else None
        if state == "low":
            if v0 < threshold <= v1:
                crossing = t0 + (t1 - t0) * (threshold - v0) / (v1 - v0)
            if v1 <= low:
                crossing = None
            if v1 >= high and crossing is not None:
                result.append((crossing, "rise"))
                state, crossing = "high", None
        elif state == "high":
            if v0 > threshold >= v1:
                crossing = t0 + (t1 - t0) * (threshold - v0) / (v1 - v0)
            if v1 >= high:
                crossing = None
            if v1 <= low and crossing is not None:
                result.append((crossing, "fall"))
                state, crossing = "low", None
    return result


def rising(rows, threshold, s):
    times = [t for t, kind in edges(rows, threshold, s["hysteresis_v"]) if kind == "rise"]
    if s["min_cycles"] < 2 or len(times) < s["min_cycles"] + 1:
        raise col.ProceduralFault("Too few complete cycles")
    periods = [b - a for a, b in zip(times, times[1:])]
    if not all(bounds(p, s["period_bounds_s"]) for p in periods):
        raise col.ProceduralFault("Missing or extra clock edges")
    return times, periods


def paired(a, b, pairing, nominal):
    if not 0 < pairing < nominal / 2:
        raise col.ProceduralFault("Pairing window must be shorter than half a period")
    differences = []
    used = set()
    for x in a:
        i = bisect_left(b, x - pairing)
        end = bisect_right(b, x + pairing)
        if end - i == 1 and i not in used:
            used.add(i)
            differences.append((x, b[i], b[i] - x))
        elif x >= b[0] - pairing and x <= b[-1] + pairing:
            raise col.ProceduralFault("Missing or ambiguous corresponding clock edge")
    if differences:
        lo, hi = differences[0][1], differences[-1][1]
        if any(i not in used for i, y in enumerate(b) if lo <= y <= hi):
            raise col.ProceduralFault("Unexpected reference edge inside paired record")
    return differences


def clock_pair(s):
    channels = s["channels"]
    a, b = acquire(s, channels, "clock_pair")
    a, _ = rising(selected(a, s), s["thresholds_v"][0], s)
    b, _ = rising(selected(b, s), s["thresholds_v"][1], s)
    pairs = paired(a, b, s["pair_window_s"], s["nominal_period_s"])
    if len(pairs) < s["min_cycles"] + 1:
        raise col.ProceduralFault("Too few paired clock edges")
    return pairs


def skew(s):
    pairs = clock_pair(s)
    value = fmean(p[2] for p in pairs)
    return {"seconds": value, "paired_edges_s": pairs, "passed": bounds(value, s["limits_s"])}


def jitter(s):
    (samples,) = acquire(s, [s["channel"]], "jitter")
    times, periods = rising(selected(samples, s), s["threshold_v"], s)
    mean = fmean(periods)
    value = sqrt(fmean((p - mean) ** 2 for p in periods))
    return {
        "seconds_rms": value,
        "rising_edges_s": times,
        "passed": bounds(value, (0, s["maximum_s"])),
    }


def pwm(s):
    (samples,) = acquire(s, [s["channel"]], "pwm")
    rows = selected(samples, s)
    _, periods = rising(rows, s["threshold_v"], s)
    cycles = edges(rows, s["threshold_v"], s["hysteresis_v"])
    start = next(i for i, (_, kind) in enumerate(cycles) if kind == "rise")
    values = []
    for i in range(start, start + 2 * len(periods), 2):
        (a, first), (b, middle), (c, last) = cycles[i : i + 3]
        if (first, middle, last) != ("rise", "fall", "rise") or not a < b < c:
            raise col.ProceduralFault("Missing or invalid PWM pulse")
        values.append(100 * (b - a) / (c - a))
    value = fmean(values)
    return {
        "duty_pct": value,
        "per_cycle_pct": values,
        "edges_s": cycles,
        "passed": bounds(value, s["limits_pct"]),
    }


def allan_rows(pairs, nominal, tau_limits, min_pairs):
    if nominal <= 0 or not tau_limits or min_pairs < 2:
        raise col.ProceduralFault("Invalid Allan deviation settings")
    x = [p[2] for p in pairs]
    result = []
    for tau, limit in tau_limits:
        m = round(tau / nominal)
        if not m >= 1 or not isclose(tau, m * nominal, rel_tol=1e-9, abs_tol=0):
            raise col.ProceduralFault("Tau must be an integer multiple of the nominal period")
        n = len(x) - 2 * m
        if n < min_pairs:
            raise col.ProceduralFault("Insufficient records for requested tau")
        value = sqrt(fmean((x[i + 2 * m] - 2 * x[i + m] + x[i]) ** 2 for i in range(n)) / 2) / tau
        result.append(
            {"tau_s": tau, "sigma_y": value, "terms": n, "passed": bounds(value, (0, limit))}
        )
    return result


def allan(s):
    pairs = clock_pair(s)
    rows = allan_rows(pairs, s["nominal_period_s"], s["tau_limits"], s["min_terms_per_tau"])
    return {"paired_edges_s": pairs, "allan": rows, "passed": all(row["passed"] for row in rows)}


def gpio_voltage(s, common_mode):
    a, b = acquire(s, s["channels"], "gpio_voltage")
    a, b = selected(a, s), selected(b, s)
    if common_mode:
        value = fmean((vp + vn) / 2 for (_, vp), (_, vn) in zip(a, b, strict=True))
    else:
        value = fmean(vp - vn for (_, vp), (_, vn) in zip(a, b, strict=True))
    return {"mean_v": value, "window_s": s["window_s"], "passed": bounds(value, s["limits_v"])}


def gpio_common(s):
    return gpio_voltage(s, common_mode=True)


def gpio_diff(s):
    return gpio_voltage(s, common_mode=False)
