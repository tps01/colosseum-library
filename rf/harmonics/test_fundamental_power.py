"""One block: fundamental power."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   CW tone at fundamental_hz.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
fundamental_hz = FILL_IN_HERE
expected_power_dbm = FILL_IN_HERE
power_tolerance_db = FILL_IN_HERE

source_power_dbm = FILL_IN_HERE  # generator-port dBm; account for input-path loss
span_hz = FILL_IN_HERE  # Hz; isolate the desired component
rbw_hz = FILL_IN_HERE  # Hz; resolve nearby tones
vbw_hz = FILL_IN_HERE  # Hz
analyzer_attenuation_db = FILL_IN_HERE  # dB; avoid analyzer-generated distortion
reference_level_dbm = FILL_IN_HERE  # dBm; no clipping/overload
settle_s = FILL_IN_HERE  # seconds after source/receiver changes


def main() -> None:
    _load_bench()
    try:
        col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=False)
        col.equipment.vsg.preset(vsg_id=vsg_id)
        col.equipment.vsg.set_modulation(vsg_id=vsg_id, enabled=False)
        col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=fundamental_hz)
        col.equipment.vsg.set_power(vsg_id=vsg_id, power_dbm=source_power_dbm)
        col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)
        col.equipment.speca.preset(speca_id=speca_id)
        col.equipment.speca.set_continuous_sweep(speca_id=speca_id, enabled=False)
        col.equipment.speca.set_trigger_source(speca_id=speca_id, source="IMM")
        col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=fundamental_hz)
        col.equipment.speca.set_span(speca_id=speca_id, span=span_hz)
        col.equipment.speca.set_rbw(speca_id=speca_id, rbw=rbw_hz)
        col.equipment.speca.set_vbw(speca_id=speca_id, vbw=vbw_hz)
        col.equipment.speca.set_auto_attenuation(speca_id=speca_id, enabled=False)
        col.equipment.speca.set_attenuation_db(speca_id=speca_id, attenuation_db=analyzer_attenuation_db)
        col.equipment.speca.toggle_preamp(speca_id=speca_id, enabled=False)
        col.equipment.speca.set_reference_level(speca_id=speca_id, level_dbm=reference_level_dbm)
        col.equipment.speca.set_detector(speca_id=speca_id, detector="POS")
        col.equipment.speca.set_trace_mode(speca_id=speca_id, trace=1, mode="WRIT")
        col.shared.wait(duration=settle_s)
        col.equipment.speca.single_sweep(speca_id=speca_id)
        col.equipment.speca.toggle_marker(speca_id=speca_id, marker=1, enabled=True)
        col.equipment.speca.set_marker_frequency(speca_id=speca_id, marker=1, frequency_hz=fundamental_hz)
        col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="fund_dbm")
        col.equipment.speca.verify_marker_power(key="fund_dbm", expected_val=expected_power_dbm, tolerance=power_tolerance_db)
    finally:
        col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=False)


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
