"""Fresh scope capture for tach; Equipment and Shared required.

DUT must already generate repetitive edges/PWM/tach. This block owns and presets
scope configuration. Probe tip -> DUT signal, probe reference -> compatible DUT
return; establish DUT power/mode and any required pull-up before running.
Run: colosseum run test_tachometer_rpm.py --config config.toml
"""
from __future__ import annotations

from pathlib import Path
from math import isfinite
from colosseum.context import get_context
from colosseum.decorators import VerificationResult

import colosseum as col

USE_AUTOCONFIG = False

oscope_id = FILL_IN_HERE  # int
scope_channel = FILL_IN_HERE  # one-based physical scope channel
probe_ratio = FILL_IN_HERE  # e.g. 10 for a 10x probe
input_ohms = FILL_IN_HERE  # supported termination, matched to the probe/DUT
scale_v_per_div = FILL_IN_HERE  # V/div; full waveform must remain on screen
offset_v = FILL_IN_HERE  # V
timebase_s_per_div = FILL_IN_HERE  # s/div; includes complete periods/edges
record_points = FILL_IN_HERE  # enough samples to resolve the required timing
trigger_level_v = FILL_IN_HERE  # V; inside the logic swing
acquire_timeout_s = FILL_IN_HERE  # positive seconds
pulses_per_rev = FILL_IN_HERE  # positive pulses/revolution
max_rpm = FILL_IN_HERE  # maximum RPM; this alone does not prove rotation


@col.verification
def verify_rpm(*, key: str, maximum: float, pulses_per_rev: float) -> VerificationResult:
    if not isfinite(pulses_per_rev) or pulses_per_rev <= 0 or not isfinite(maximum) or maximum < 0:
        raise ValueError("Expected positive pulses/revolution and a finite nonnegative RPM limit")
    row = get_context().db.get_measurement("equipment", "oscope.measure_frequency_hz", key, row_index=0)
    if row is None or row.value is None:
        raise ValueError("Missing tachometer frequency evidence")
    hz = float(row.value)
    if not isfinite(hz) or hz < 0:
        raise ValueError("Tachometer frequency must be finite and nonnegative")
    rpm = hz * 60.0 / pulses_per_rev
    return VerificationResult(status="PASS" if rpm <= maximum else "FAIL", actual=rpm, message=f"Tachometer {rpm} RPM <= {maximum} RPM")


def main() -> None:
    _load_bench()
    col.equipment.oscope.preset(oscope_id=oscope_id)
    col.equipment.oscope.set_channel_display(oscope_id=oscope_id, channel=scope_channel, enabled=True)
    col.equipment.oscope.set_channel_coupling(oscope_id=oscope_id, channel=scope_channel, coupling="DC")
    col.equipment.oscope.set_channel_probe_attenuation(oscope_id=oscope_id, channel=scope_channel, attenuation=probe_ratio)
    col.equipment.oscope.set_channel_impedance(oscope_id=oscope_id, channel=scope_channel, ohms=input_ohms)
    col.equipment.oscope.set_channel_scale_v(oscope_id=oscope_id, channel=scope_channel, volts_per_div=scale_v_per_div)
    col.equipment.oscope.set_channel_offset_v(oscope_id=oscope_id, channel=scope_channel, offset_v=offset_v)
    col.equipment.oscope.set_timebase_scale(oscope_id=oscope_id, seconds_per_div=timebase_s_per_div)
    col.equipment.oscope.set_record_length(oscope_id=oscope_id, points=record_points)
    col.equipment.oscope.set_acquire_mode(oscope_id=oscope_id, mode="sample")
    col.equipment.oscope.set_trigger_mode(oscope_id=oscope_id, mode="normal")
    col.equipment.oscope.set_trigger_source(oscope_id=oscope_id, source=f"CH{scope_channel}")
    col.equipment.oscope.set_trigger_level_v(oscope_id=oscope_id, level_v=trigger_level_v)
    col.equipment.oscope.set_trigger_slope(oscope_id=oscope_id, slope="rising")
    col.equipment.oscope.acquire(oscope_id=oscope_id, timeout_s=acquire_timeout_s)
    col.equipment.oscope.measure_frequency_hz(oscope_id=oscope_id, channel=scope_channel, key="tach_hz")
    verify_rpm(key="tach_hz", maximum=max_rpm, pulses_per_rev=pulses_per_rev)



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
