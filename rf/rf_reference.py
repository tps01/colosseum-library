"""Calibrated RF copy-outs for known, separately qualified fixtures."""

from statistics import fmean
from time import perf_counter

import colosseum as col

from reference_common import bounds, number, trace, window


def spectrum(s, stem, correction=None):
    analyzer = s["speca_id"]
    relative = f"traces/{stem}.csv"
    col.equipment.speca.single_sweep(speca_id=analyzer)
    col.equipment.speca.save_trace_data(
        speca_id=analyzer, path=relative, trace=1, key=stem, calibration=correction
    )
    return trace(relative, "frequency_hz", "amplitude_dbm")


def calibrate(s, file_key, name):
    col.equipment.calibration.load_calibration(filename=s[file_key], key=name)
    return name


def gain_flatness(s):
    vna = s["vna_id"]
    col.equipment.vna.configure_trigger(vna_id=vna, source="IMM", continuous=False)
    col.equipment.vna.set_trace_count(vna_id=vna, count=1)
    col.equipment.vna.set_trace_parameters(vna_id=vna, trace=1, parameter="S21", format="MLOG")
    col.equipment.vna.single_sweep(vna_id=vna)
    relative = "traces/calibrated_s21.csv"
    col.equipment.vna.save_trace_data(vna_id=vna, path=relative, trace=1, parameter="S21")
    a, b = s["band_hz"]
    rows = window(trace(relative, "frequency_hz", "value"), a, b, s["max_spacing_hz"])
    low, high = min(rows, key=lambda p: p[1]), max(rows, key=lambda p: p[1])
    value = high[1] - low[1]
    return {
        "flatness_db": value,
        "minimum": low,
        "maximum": high,
        "passed": bounds(value, (0, s["maximum_db"])),
    }


def component(s, frequency, key, correction):
    from rf.ip2_ip3.two_tone import capture_component

    analyzer = s["speca_id"]
    capture_component(
        speca_id=analyzer,
        frequency_hz=frequency,
        span_hz=s["span_hz"],
        rbw_hz=s["rbw_hz"],
        vbw_hz=s["vbw_hz"],
        attenuation_db=s["attenuation_db"],
        reference_dbm=s["reference_dbm"],
        settle_s=s["settle_s"],
    )
    col.equipment.speca.save_trace_data(
        speca_id=analyzer, path=f"traces/{key}.csv", trace=1, key=f"{key}_trace"
    )
    return number(
        col.equipment.speca.measure_marker_power(
            speca_id=analyzer,
            marker=1,
            key=key,
            calibration=correction,
        ),
        "corrected component power",
    )


def harmonic(s, order):
    correction = calibrate(s, "output_correction", "harmonic_output")
    f = number(s["fundamental_hz"], "fundamental")
    if not 0 < s["span_hz"] < f:
        raise col.ProceduralFault("Span must isolate each harmonic")
    first = component(s, f, "fundamental_before", correction)
    harmonic_power = component(s, order * f, f"h{order}", correction)
    last = component(s, f, "fundamental_after", correction)
    if (
        not all(bounds(x, s["carrier_bounds_dbm"]) for x in (first, last))
        or abs(first - last) > s["drift_max_db"]
    ):
        raise col.ProceduralFault("Fundamental is absent or unstable")
    if harmonic_power < s["harmonic_detection_dbm"]:
        raise col.ProceduralFault("Harmonic is below the qualified detection level")
    value = harmonic_power - fmean((first, last))
    return {
        "dbc": value,
        "fundamental_before_dbm": first,
        "fundamental_after_dbm": last,
        "harmonic_dbm": harmonic_power,
        "passed": value <= number(s["maximum_dbc"], "harmonic limit"),
    }


def h2(s):
    return harmonic(s, 2)


def h3(s):
    return harmonic(s, 3)


def oip3(s):
    from rf.ip2_ip3.two_tone import prepare_two_tone

    a, b = s["vsg1_id"], s["vsg2_id"]
    f, g = s["f1_hz"], s["f2_hz"]
    if a == b or not 0 < s["span_hz"] < g - f or 2 * f <= g:
        raise col.ProceduralFault(
            "Use distinct generators and isolated positive component frequencies"
        )
    step = number(s["level_step_db"], "level step")
    if step <= 0:
        raise col.ProceduralFault("Use a positive input-level step")
    correction = calibrate(s, "output_correction", "ip3_output")
    p, q = s["low_generator_dbm"]
    try:
        col.equipment.vsg.set_output(vsg_id=a, enabled=False)
        col.equipment.vsg.set_output(vsg_id=b, enabled=False)
        prepare_two_tone(vsg1_id=a, vsg2_id=b, f1_hz=f, f2_hz=g, power1_dbm=p, power2_dbm=q)

        def capture(label):
            return [
                component(s, hz, f"{label}_{name}", correction)
                for name, hz in (
                    ("f1", f),
                    ("f2", g),
                    ("im3_left", 2 * f - g),
                    ("im3_right", 2 * g - f),
                )
            ]

        low = capture("low")
        col.equipment.vsg.set_power(vsg_id=a, power_dbm=p + step)
        col.equipment.vsg.set_power(vsg_id=b, power_dbm=q + step)
        high = capture("high")
        tol = s["slope_tolerance_db"]
        if any(
            abs(y - x - (step if i < 2 else 3 * step)) > tol
            for i, (x, y) in enumerate(zip(low, high))
        ):
            raise col.ProceduralFault(
                "Carrier and product levels do not show the qualified linear and cubic slopes"
            )
        if any(
            abs(row[0] - row[1]) > s["balance_max_db"]
            or min(row[2:]) < s["im3_detection_dbm"]
            or any(c <= p for c, p in zip(row[:2], row[2:]))
            for row in (low, high)
        ):
            raise col.ProceduralFault(
                "Carriers are unbalanced or IM3 products are outside the usable range"
            )
        sides = [carrier + (carrier - product) / 2 for carrier, product in zip(high[:2], high[2:])]
        return {
            "low_dbm": low,
            "high_dbm": high,
            "sides_dbm": sides,
            "worst_dbm": min(sides),
            "passed": min(sides) >= number(s["minimum_dbm"], "OIP3 limit"),
        }
    finally:
        try:
            col.equipment.vsg.set_output(vsg_id=a, enabled=False)
        finally:
            col.equipment.vsg.set_output(vsg_id=b, enabled=False)


def mask_result(rows, mask, max_spacing):
    if mask.get("domain") != "frequency" or not mask.get("regions"):
        raise col.ProceduralFault("Use a nonempty frequency mask with Hz and dBm")
    worst = None
    for region in mask["regions"]:
        if region["kind"] != "keep_below":
            raise col.ProceduralFault("Only keep_below regions define this upper-mask margin")
        selected = window(rows, region["x0"], region["x1"], max_spacing)
        f, value = max(selected, key=lambda p: p[1])
        margin = region["y1"] - value
        if worst is None or margin < worst["margin_db"]:
            worst = {"margin_db": margin, "frequency_hz": f, "region": region.get("id")}
    return worst


def mask_margin(s):
    mask = col.equipment.tools.load_mask(path=s["mask_path"])
    spectrum(s, "mask_raw")
    # Export the same held sweep again with its qualified path correction.
    relative = "traces/mask_corrected.csv"
    correction = calibrate(s, "output_correction", "mask_output")
    col.equipment.speca.save_trace_data(
        speca_id=s["speca_id"], path=relative, trace=1, key="mask_corrected", calibration=correction
    )
    result = mask_result(
        trace(relative, "frequency_hz", "amplitude_dbm"), mask, s["max_spacing_hz"]
    )
    return result | {"passed": result["margin_db"] >= number(s["minimum_db"], "mask margin limit")}


def compression_crossing(rows, fit_points, max_baseline_residual):
    if not 2 <= fit_points < len(rows) - 1 or any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise col.ProceduralFault(
            "Use increasing measured input powers and a separately bracketed fit"
        )
    baseline = rows[:fit_points]
    x, y = fmean(p[0] for p in baseline), fmean(p[1] for p in baseline)
    slope = sum((a - x) * (b - y) for a, b in baseline) / sum((a - x) ** 2 for a, _ in baseline)
    intercept = y - slope * x
    residual = [(a, slope * a + intercept - b) for a, b in rows]
    if any(abs(b) > max_baseline_residual for _, b in residual[:fit_points]):
        raise col.ProceduralFault("Small-signal points do not fit the linear reference")
    for (a, c), (b, d) in zip(residual[fit_points - 1 :], residual[fit_points:]):
        if c < 1 <= d:
            return a + (b - a) * (1 - c) / (d - c), slope, intercept
    raise col.ProceduralFault("The measured sweep did not bracket first 1 dB compression")


def p1db(s):
    source = s["vsg_id"]
    meters = s["pwrmeter_ids"]
    levels = s["generator_steps_dbm"]
    if (
        len(meters) != 2
        or len(set(meters)) != 2
        or len(levels) < 4
        or any(b <= a for a, b in zip(levels, levels[1:]))
        or any(not bounds(p, s["qualified_generator_bounds_dbm"]) for p in levels)
    ):
        raise col.ProceduralFault("Invalid or unsafe source sweep or power-meter mapping")
    correction = [
        calibrate(s, f"{plane}_correction", f"p1db_{plane}") for plane in ("input", "output")
    ]
    f = s["frequency_hz"]
    rows = []
    try:
        col.equipment.vsg.set_output(vsg_id=source, enabled=False)
        col.equipment.vsg.set_modulation(vsg_id=source, enabled=False)
        col.equipment.vsg.set_frequency(vsg_id=source, frequency=f)
        col.equipment.vsg.set_power(vsg_id=source, power_dbm=levels[0])
        for meter in meters:
            col.equipment.pwrmeter.set_frequency(pwrmeter_id=meter, frequency_hz=f)
        col.equipment.vsg.set_output(vsg_id=source, enabled=True)
        for i, level in enumerate(levels):
            col.equipment.vsg.set_power(vsg_id=source, power_dbm=level)
            col.shared.wait(duration=s["settle_s"])
            point = []
            for j, (meter, cal) in enumerate(zip(meters, correction)):
                col.equipment.pwrmeter.acquire(pwrmeter_id=meter)
                point.append(
                    number(
                        col.equipment.pwrmeter.measure_power_avg_dbm(
                            pwrmeter_id=meter,
                            calibration=cal,
                            key=f"point_{i}_plane_{j}",
                        ),
                        "power at DUT plane",
                    )
                )
            rows.append(point)
        value, slope, intercept = compression_crossing(
            rows, s["small_signal_points"], s["max_fit_residual_db"]
        )
        if not bounds(slope, s["small_signal_slope_bounds"]):
            raise col.ProceduralFault("Small-signal gain fit is outside the qualified slope range")
        return {
            "input_p1db_dbm": value,
            "slope": slope,
            "intercept_dbm": intercept,
            "powers_dbm": rows,
            "passed": bounds(value, s["limits_dbm"]),
        }
    finally:
        col.equipment.vsg.set_output(vsg_id=source, enabled=False)


def channel_power(s):
    analyzer = s["speca_id"]
    col.equipment.speca.single_sweep(speca_id=analyzer)
    raw = number(
        col.equipment.speca.measure_channel_power_dbm(
            speca_id=analyzer, key="native_channel_power"
        ),
        "native channel power",
    )
    value = raw + number(s["flat_path_loss_db"], "flat path loss")
    return {
        "power_dbm": value,
        "center_hz": s["verified_center_hz"],
        "bandwidth_hz": s["verified_bandwidth_hz"],
        "passed": bounds(value, s["limits_dbm"]),
    }


def spur(s):
    correction = calibrate(s, "output_correction", "spur_output")
    start, stop = s["band_hz"]
    guards = s["exclude_hz"]
    carrier_start, carrier_stop = s["carrier_window_hz"]
    duration = number(s["observation_s"], "observation time")
    if (
        duration <= 0
        or s["min_sweeps"] < 2
        or s["max_sweeps"] < s["min_sweeps"]
        or not any(a <= carrier_start < carrier_stop <= b for a, b in guards)
    ):
        raise col.ProceduralFault("Supply a bounded observation and exclude the carrier window")
    deadline = perf_counter() + duration
    axis, worst = None, None
    carriers = []
    for i in range(s["max_sweeps"]):
        raw = spectrum(s, f"spur_raw_{i}")
        path = f"traces/spur_corrected_{i}.csv"
        col.equipment.speca.save_trace_data(
            speca_id=s["speca_id"],
            path=path,
            trace=1,
            key=f"spur_corrected_{i}",
            calibration=correction,
        )
        rows = trace(path, "frequency_hz", "amplitude_dbm")
        grid = [f for f, _ in rows]
        if axis is not None and grid != axis or grid != [f for f, _ in raw]:
            raise col.ProceduralFault("Spur traces do not share the same frequency grid")
        axis = grid
        bins = window(rows, start, stop, s["max_spacing_hz"])
        carriers.append(
            max(p for _, p in window(rows, carrier_start, carrier_stop, s["max_spacing_hz"]))
        )
        included = [(f, p) for f, p in bins if not any(a <= f <= b for a, b in guards)]
        if not included:
            raise col.ProceduralFault("Exclusions remove the entire spur band")
        candidate = max(included, key=lambda p: p[1])
        if worst is None or candidate[1] > worst[1]:
            worst = candidate
        if i + 1 >= s["min_sweeps"] and perf_counter() >= deadline:
            break
    if (
        perf_counter() < deadline
        or max(carriers) - min(carriers) > s["carrier_drift_db"]
        or not all(bounds(p, s["carrier_bounds_dbm"]) for p in carriers)
    ):
        raise col.ProceduralFault("Observation duration or carrier stability was not established")
    floor = number(s["detection_dbm"], "worst-case corrected detection level")
    upper_bound = worst[1] < floor
    value = max(worst[1], floor) - fmean(carriers)
    limit = number(s["maximum_dbc"], "spur limit")
    if upper_bound and value > limit:
        raise col.ProceduralFault(
            f"Detection-limited spur bound {value:g} dBc cannot establish compliance"
        )
    return {
        "dbc": value,
        "worst_bin_hz": worst[0],
        "carrier_dbm": carriers,
        "upper_bound": upper_bound,
        "passed": value <= limit,
    }
