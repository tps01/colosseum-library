"""Shared capture evidence and one-verdict runner for copy-outs."""

import csv
from math import isfinite
from pathlib import Path

import colosseum as col
from colosseum.context import get_context


def output_path(relative):
    directory = get_context().output_dir
    if directory is None:
        raise col.ProceduralFault("This procedure requires persisted artifacts")
    return Path(directory) / relative


def trace(relative, x_field, y_field):
    with output_path(relative).open(encoding="utf-8", newline="") as handle:
        rows = [(float(r[x_field]), float(r[y_field])) for r in csv.DictReader(handle)]
    if len(rows) < 2 or not all(isfinite(x) and isfinite(y) for x, y in rows):
        raise col.ProceduralFault("Expected at least two finite trace samples")
    if any(a[0] >= b[0] for a, b in zip(rows, rows[1:])):
        raise col.ProceduralFault("The trace axis must increase strictly")
    return rows


def window(rows, start, stop, max_spacing):
    if (
        not all(isfinite(x) for x in (start, stop, max_spacing))
        or not start < stop
        or max_spacing <= 0
    ):
        raise col.ProceduralFault("Invalid analysis window or maximum sample spacing")
    if rows[0][0] > start or rows[-1][0] < stop:
        raise col.ProceduralFault("Trace does not cover the analysis window")
    if any(
        b[0] - a[0] > max_spacing for a, b in zip(rows, rows[1:]) if a[0] < stop and b[0] > start
    ):
        raise col.ProceduralFault("Trace sampling gap exceeds the qualified spacing")
    selected = [(x, y) for x, y in rows if start <= x <= stop]
    if len(selected) < 2:
        raise col.ProceduralFault("Analysis window contains too few samples")
    return selected


@col.measurement
def capture_result(*, key, collect, settings):
    """Record structured supporting evidence with the primary acceptance result."""
    output_path("capture")
    result = collect(settings)
    if type(result["passed"]) is not bool:
        raise col.ProceduralFault("Procedure did not produce a valid verdict")
    return result


def required(*, key, collect, settings, config):
    if not col.config.is_loaded():
        col.config.load_config(path=config)
    capture_result(key=key, collect=collect, settings=settings)
    col.shared.verify.verify_field(key=key, field="passed", expected_val=True)


def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise col.ProceduralFault(f"Missing or nonfinite {name}")
    return value


def bounds(value, limits):
    low, high = limits
    if number(low, "minimum") > number(high, "maximum"):
        raise col.ProceduralFault("Inverted acceptance bounds")
    return low <= number(value, "measurement") <= high
