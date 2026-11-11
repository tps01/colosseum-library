"""im3_product_power: two CW generators -> isolated combiner -> DUT -> analyzer.

Requires Equipment + Shared and a powered, enabled DUT. Copy this topic including
two_tone.py. Set generator-port levels with measured path loss; verify source and
analyzer linearity independently before calling the result DUT IM3.
"""
from __future__ import annotations
from pathlib import Path
from math import isfinite
import colosseum as col
from two_tone import prepare_two_tone, capture_component

USE_AUTOCONFIG = False
vsg1_id = FILL_IN_HERE
vsg2_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
f1_hz = FILL_IN_HERE
f2_hz = FILL_IN_HERE
power1_dbm = FILL_IN_HERE  # generator 1 port dBm
power2_dbm = FILL_IN_HERE  # generator 2 port dBm
span_hz = FILL_IN_HERE  # Hz; isolate the desired component
rbw_hz = FILL_IN_HERE  # Hz; resolve nearby tones
vbw_hz = FILL_IN_HERE  # Hz
analyzer_attenuation_db = FILL_IN_HERE  # dB; avoid analyzer-generated distortion
reference_level_dbm = FILL_IN_HERE  # dBm; no clipping/overload
settle_s = FILL_IN_HERE  # seconds after source/receiver changes
max_im3_dbm = FILL_IN_HERE
expected_f1_dbm = FILL_IN_HERE
expected_f2_dbm = FILL_IN_HERE
tolerance_db = FILL_IN_HERE


def main() -> None:
    if not isfinite(span_hz) or not 0 < span_hz < f2_hz - f1_hz:
        raise ValueError("Span must isolate a component: 0 < span < f2 - f1")
    _load_bench()
    try:
        col.equipment.vsg.set_output(vsg_id=vsg1_id, enabled=False)
        col.equipment.vsg.set_output(vsg_id=vsg2_id, enabled=False)
        prepare_two_tone(vsg1_id=vsg1_id, vsg2_id=vsg2_id, f1_hz=f1_hz, f2_hz=f2_hz, power1_dbm=power1_dbm, power2_dbm=power2_dbm)
        capture_component(speca_id=speca_id, frequency_hz=f1_hz, span_hz=span_hz, rbw_hz=rbw_hz, vbw_hz=vbw_hz, attenuation_db=analyzer_attenuation_db, reference_dbm=reference_level_dbm, settle_s=settle_s)
        col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="im3_ref_f1")
        col.shared.verify.verify_field(key="im3_ref_f1", expected_val=expected_f1_dbm, tolerance=tolerance_db)
        capture_component(speca_id=speca_id, frequency_hz=f2_hz, span_hz=span_hz, rbw_hz=rbw_hz, vbw_hz=vbw_hz, attenuation_db=analyzer_attenuation_db, reference_dbm=reference_level_dbm, settle_s=settle_s)
        col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="im3_ref_f2")
        col.shared.verify.verify_field(key="im3_ref_f2", expected_val=expected_f2_dbm, tolerance=tolerance_db)
        capture_component(speca_id=speca_id, frequency_hz=2 * f2_hz - f1_hz, span_hz=span_hz, rbw_hz=rbw_hz, vbw_hz=vbw_hz, attenuation_db=analyzer_attenuation_db, reference_dbm=reference_level_dbm, settle_s=settle_s)
        col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="im3_dbm")
        col.shared.verify.verify_field(key="im3_dbm", maximum=max_im3_dbm)
    finally:
        try:
            col.equipment.vsg.set_output(vsg_id=vsg1_id, enabled=False)
        finally:
            col.equipment.vsg.set_output(vsg_id=vsg2_id, enabled=False)


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
