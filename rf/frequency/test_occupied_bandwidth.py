"""Verify the width containing 99% of integrated power. Requires Equipment 0.20 and Shared 0.9."""

from pathlib import Path

import colosseum as col

from wideband_trace import capture_trace, qualify_trace

# SETUP: Supply a stable modulated signal through a qualified RF path.
speca_id = FILL_IN_HERE
sweep_center_hz = FILL_IN_HERE
sweep_span_hz = FILL_IN_HERE
sweep_points = FILL_IN_HERE
rbw_hz = FILL_IN_HERE
vbw_hz = FILL_IN_HERE
detector = FILL_IN_HERE  # model-specific power detector
attenuation_db = FILL_IN_HERE
reference_dbm = FILL_IN_HERE
start_hz = FILL_IN_HERE  # analysis window inside the sweep
stop_hz = FILL_IN_HERE
guard_hz = FILL_IN_HERE  # width at each end of the analysis window
min_peak_dbm = FILL_IN_HERE
max_guard_dbm = FILL_IN_HERE
max_bandwidth_hz = FILL_IN_HERE


def main() -> None:
    if not col.config.is_loaded():
        col.config.load_config(path=Path(__file__).with_name("config.toml"))
    trace_path = capture_trace(
        speca_id=speca_id, sweep_center_hz=sweep_center_hz, sweep_span_hz=sweep_span_hz,
        sweep_points=sweep_points, rbw_hz=rbw_hz, vbw_hz=vbw_hz, detector=detector,
        attenuation_db=attenuation_db, reference_dbm=reference_dbm, key="occupied_bandwidth_trace",
    )
    qualify_trace(
        path=trace_path, start_hz=start_hz, stop_hz=stop_hz,
        guard_hz=guard_hz, min_peak_dbm=min_peak_dbm, max_guard_dbm=max_guard_dbm,
    )
    col.equipment.speca.measure_bw(
        speca_id=speca_id, start_hz=start_hz, stop_hz=stop_hz, trace_path=trace_path,
        method="occupied_power", occupied_power_pct=99, smoothing_order=0, save_plot=True, key="occupied_bandwidth",
    )
    col.shared.verify.verify_field(key="occupied_bandwidth", maximum=max_bandwidth_hz)


if __name__ == "__main__":
    main()
    col.endex()
