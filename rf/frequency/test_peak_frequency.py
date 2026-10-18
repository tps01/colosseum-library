"""One block: CW peak marker frequency."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   VSG CW into DUT; SA on output.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
vsg_id = FILL_IN_HERE
speca_id = FILL_IN_HERE
center_freq_hz = FILL_IN_HERE
freq_tolerance_hz = FILL_IN_HERE

source_power_dbm = FILL_IN_HERE  # generator-port dBm; account for input-path loss
span_hz = FILL_IN_HERE  # Hz; isolate the desired component
rbw_hz = FILL_IN_HERE  # Hz; resolve nearby tones
vbw_hz = FILL_IN_HERE  # Hz
analyzer_attenuation_db = FILL_IN_HERE  # dB; avoid analyzer-generated distortion
reference_level_dbm = FILL_IN_HERE  # dBm; no clipping/overload
settle_s = FILL_IN_HERE  # seconds after source/receiver changes
min_peak_power_dbm = FILL_IN_HERE  # reject noise-only or absent-carrier captures


def main() -> None:
    _load_bench()
    try:
        col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=False)
        col.equipment.vsg.preset(vsg_id=vsg_id)
        col.equipment.vsg.set_modulation(vsg_id=vsg_id, enabled=False)
        col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=center_freq_hz)
        col.equipment.vsg.set_power(vsg_id=vsg_id, power_dbm=source_power_dbm)
        col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)
        col.equipment.speca.preset(speca_id=speca_id)
        col.equipment.speca.set_continuous_sweep(speca_id=speca_id, enabled=False)
        col.equipment.speca.set_trigger_source(speca_id=speca_id, source="IMM")
        col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=center_freq_hz)
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
        col.equipment.speca.peak_search(speca_id=speca_id, marker=1)
        col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="peak_power")
        col.shared.verify.verify_field(key="peak_power", minimum=min_peak_power_dbm)
        col.equipment.speca.measure_marker_frequency(speca_id=speca_id, marker=1, key="peak_f")
        col.equipment.speca.verify_marker_frequency(key="peak_f", expected_val=center_freq_hz, tolerance=freq_tolerance_hz)
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
