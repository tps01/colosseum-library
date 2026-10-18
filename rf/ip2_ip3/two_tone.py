"""Two independent CW sources and one analyzer, copied with the IP3 topic."""
from math import isfinite
import colosseum as col


def prepare_two_tone(*, vsg1_id, vsg2_id, f1_hz, f2_hz, power1_dbm, power2_dbm):
    if vsg1_id == vsg2_id or not all(isfinite(x) for x in (f1_hz, f2_hz, power1_dbm, power2_dbm)) or not 0 < f1_hz < f2_hz:
        raise ValueError("Use distinct sources, finite levels and 0 < f1 < f2")
    # Isolators/combiner connect both generator outputs to the one DUT input.
    for source, frequency, power in ((vsg1_id, f1_hz, power1_dbm), (vsg2_id, f2_hz, power2_dbm)):
        col.equipment.vsg.preset(vsg_id=source)
        col.equipment.vsg.set_modulation(vsg_id=source, enabled=False)
        col.equipment.vsg.set_frequency(vsg_id=source, frequency=frequency)
        col.equipment.vsg.set_power(vsg_id=source, power_dbm=power)
    for source in (vsg1_id, vsg2_id):
        col.equipment.vsg.set_output(vsg_id=source, enabled=True)


def capture_component(*, speca_id, frequency_hz, span_hz, rbw_hz, vbw_hz, attenuation_db, reference_dbm, settle_s):
    if not all(isfinite(x) for x in (frequency_hz, span_hz, rbw_hz, vbw_hz, attenuation_db, reference_dbm, settle_s)) or min(frequency_hz, span_hz, rbw_hz, vbw_hz) <= 0 or settle_s < 0:
        raise ValueError("Invalid analyzer settings")
    col.equipment.speca.preset(speca_id=speca_id)
    col.equipment.speca.set_continuous_sweep(speca_id=speca_id, enabled=False)
    col.equipment.speca.set_trigger_source(speca_id=speca_id, source="IMM")
    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=frequency_hz)
    col.equipment.speca.set_span(speca_id=speca_id, span=span_hz)
    col.equipment.speca.set_rbw(speca_id=speca_id, rbw=rbw_hz)
    col.equipment.speca.set_vbw(speca_id=speca_id, vbw=vbw_hz)
    col.equipment.speca.set_auto_attenuation(speca_id=speca_id, enabled=False)
    col.equipment.speca.set_attenuation_db(speca_id=speca_id, attenuation_db=attenuation_db)
    col.equipment.speca.toggle_preamp(speca_id=speca_id, enabled=False)
    col.equipment.speca.set_reference_level(speca_id=speca_id, level_dbm=reference_dbm)
    col.equipment.speca.set_detector(speca_id=speca_id, detector="POS")
    col.equipment.speca.set_trace_mode(speca_id=speca_id, trace=1, mode="WRIT")
    col.shared.wait(duration=settle_s)
    col.equipment.speca.single_sweep(speca_id=speca_id)
    col.equipment.speca.toggle_marker(speca_id=speca_id, marker=1, enabled=True)
    col.equipment.speca.set_marker_frequency(speca_id=speca_id, marker=1, frequency_hz=frequency_hz)
