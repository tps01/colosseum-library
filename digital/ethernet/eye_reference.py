"""Fold saved Ethernet waveform samples and evaluate a shared Colosseum mask."""

from dataclasses import asdict
from math import isfinite, ulp
from pathlib import Path

from colosseum_equipment.tools import evaluate_mask, load_mask
from colosseum_equipment.tools.mask_verify import read_trace_xy


def _read_voltage(path):
    times, volts, domain = read_trace_xy(Path(path))
    if domain != "time" or len(times) < 2:
        raise ValueError(f"Expected at least two time-domain voltage samples in {path}")
    if not all(isfinite(value) for column in (times, volts) for value in column):
        raise ValueError(f"Nonfinite waveform sample in {path}")
    if any(right <= left for left, right in zip(times, times[1:])):
        raise ValueError(f"Waveform times must increase strictly in {path}")
    return times, volts


def _read_capture(capture):
    if isinstance(capture, (str, Path)):
        return (*_read_voltage(capture), [str(capture)])
    positive, negative = capture
    times, vp = _read_voltage(positive)
    negative_times, vn = _read_voltage(negative)
    if times != negative_times:
        raise ValueError("Differential legs must share a simultaneous, deskewed time grid")
    return times, [p - n for p, n in zip(vp, vn, strict=True)], [str(positive), str(negative)]


def _eye_phase(time_s, origin_s, period_s):
    offset = time_s - origin_s
    phase = offset % period_s
    # Decimal CSV times and periods can round an exact boundary just below zero.
    return 0.0 if period_s - phase <= max(ulp(offset), ulp(period_s)) else phase


def verify_eye_traces(
    *, captures, mask_path, max_sample_spacing_s, period_s=None, origin_s=0.0,
):
    """Apply one time/voltage mask to each saved capture and require every capture to pass.

    An item in captures is a differential CSV path or a (positive, negative)
    pair of CSV paths from one acquisition. Specify the fold period and common
    trigger-relative origin for a repeating pattern. Leave period_s unset for
    traces already expressed in the mask's time coordinates.
    """
    if not isfinite(max_sample_spacing_s) or max_sample_spacing_s <= 0:
        raise ValueError("Maximum sample spacing must be finite and positive")
    if not isfinite(origin_s) or (period_s is not None and (not isfinite(period_s) or period_s <= 0)):
        raise ValueError("Supply a finite origin and a finite positive period when folding")
    if isinstance(captures, (str, Path)):
        raise ValueError("Supply a sequence of captures")
    mask = load_mask(mask_path)
    if (mask["domain"], mask["x_unit"], mask["y_unit"]) != ("time", "s", "V"):
        raise ValueError("Use a time-domain Colosseum mask in seconds and volts")
    regions = mask["regions"]
    if not regions or any(
        not isfinite(region[axis]) for region in regions for axis in ("x0", "x1", "y0", "y1")
    ):
        raise ValueError("Supply a nonempty mask with finite bounds")
    if period_s is not None and any(not 0 <= region["x0"] <= region["x1"] < period_s for region in regions):
        raise ValueError("Folded mask time bounds must be within [0, period_s)")

    results = []
    for capture in captures:
        times, volts, files = _read_capture(capture)
        if any(right - left > max_sample_spacing_s for left, right in zip(times, times[1:])):
            raise ValueError(f"Waveform sample gap exceeds max_sample_spacing_s in {files}")
        if period_s is not None:
            if times[-1] - times[0] < period_s:
                raise ValueError(f"Capture must span at least one full fold period in {files}")
            times = [_eye_phase(time, origin_s, period_s) for time in times]
        result = evaluate_mask(times, volts, mask)
        results.append({
            "files": files,
            "samples": len(times),
            "passed": result.ok,
            "message": result.message,
            "reported_violations": [asdict(violation) for violation in result.violations],
        })
    if not results:
        raise ValueError("Supply at least one saved capture")
    return {
        "mask_path": str(mask_path),
        "period_s": period_s,
        "origin_s": origin_s if period_s is not None else None,
        "max_sample_spacing_s": max_sample_spacing_s,
        "captures": results,
        "passed": all(result["passed"] for result in results),
    }
