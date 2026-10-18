"""undershoot_mv: measured rail response to one controlled load step.
Requires Equipment 0.5.0+, Shared 0.5.0+, and the companion transient_response.py.
Wire PSU -> DUT input, eload -> DUT output, scope rail probe -> DUT output and
current monitor -> actual load current. See README for the event/metric contract.
"""
from pathlib import Path
import colosseum as col
from transient_response import measure_response, verify_response

USE_AUTOCONFIG = False
settings = {
    "current_v_per_a": FILL_IN_HERE,  # calibrated monitor V/A, positive
    "current_zero_v": FILL_IN_HERE,  # calibrated monitor zero-current offset V
    "current_tolerance_a": FILL_IN_HERE,  # allowed initial/final actual-current error A
    "psu_id": FILL_IN_HERE,  # supply feeding DUT input
    "eload_id": FILL_IN_HERE,  # load across DUT regulated output
    "oscope_id": FILL_IN_HERE,  # scope with nonblocking arm_single
    "rail_channel": FILL_IN_HERE,  # rail voltage channel
    "current_channel": FILL_IN_HERE,  # current-monitor voltage channel (same capture)
    "supply_v": FILL_IN_HERE,  # DUT input supply V
    "current_limit_a": FILL_IN_HERE,  # DUT input supply current limit A
    "target_v": FILL_IN_HERE,  # required DUT regulated rail V
    "initial_a": FILL_IN_HERE,  # initial output load A; high for overshoot, low for undershoot
    "final_a": FILL_IN_HERE,  # final output load A; low for overshoot, high for undershoot
    "slew_a_per_s": FILL_IN_HERE,  # load current slew A/s
    "settle_s": FILL_IN_HERE,  # initial DUT settling delay s
    "arm_delay_s": FILL_IN_HERE,  # qualified arming readiness allowance s
    "acquire_timeout_s": FILL_IN_HERE,  # capture timeout s
    "rail_probe_ratio": FILL_IN_HERE,  # rail probe attenuation factor
    "current_probe_ratio": FILL_IN_HERE,  # current probe attenuation factor
    "rail_scale_v": FILL_IN_HERE,  # rail V/div
    "rail_offset_v": FILL_IN_HERE,  # rail vertical offset V
    "current_scale_v": FILL_IN_HERE,  # current monitor V/div
    "trigger_v": FILL_IN_HERE,  # load current monitor threshold V between the two load levels
    "record_points": FILL_IN_HERE,  # samples sufficient to resolve the transition
    "timebase_s_per_div": FILL_IN_HERE,  # s/div; include all pre/post windows
    "pre_s": FILL_IN_HERE,  # required stable pre-event window s
    "observation_s": FILL_IN_HERE,  # post-event observation window s
    "steady_tolerance_v": FILL_IN_HERE,  # pre-event rail acceptance half-band V
    "settle_band_v": FILL_IN_HERE,  # settling half-band V around target
    "hold_s": FILL_IN_HERE,  # required in-band hold through the observed tail s
}
max_undershoot_mv = FILL_IN_HERE  # mV


def main() -> None:
    _load_bench()
    measure_response(key="undershoot_mv", metric="undershoot_mv", settings=settings)
    verify_response(key="undershoot_mv", maximum=max_undershoot_mv)


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
