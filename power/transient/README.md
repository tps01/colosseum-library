# Controlled load-transient response

Requires Equipment **0.5.0+**, Shared **0.5.0+**, a qualified scope driver
(`tektronix-mdo4000` has explicit nonblocking arming), and an eload supporting CC
and controlled slew. Copy this whole folder including `transient_response.py`.
These blocks own the PSU/load/scope and turn the PSU off and load off on exit.

## Connections and prerequisites

PSU +/return -> DUT input supply/return. Eload +/- -> the DUT regulated output
and its return. Scope rail probe -> DUT output measurement plane; a current
probe or qualified current-monitor output -> a distinct scope trigger channel.
Both waveforms must share the acquisition time axis and be deskewed. Choose a
current-monitor threshold strictly between initial/final levels. Probe voltage,
common-mode range, 1 Mohm inputs and ground arrangement must fit this circuit.
Do not attach an earth-referenced ground clip to an incompatible node.
Enable the DUT's regulator/control mode beforehand; the PSU source is its input,
not a substitute for measuring its regulated output. Set source current budget,
load limits, current slew and probe settings for the actual DUT and fixture.

## Procedures and definitions

| Script | Event and acceptance |
| --- | --- |
| `test_overshoot_mv.py` | High-to-low current step; max(0, max post-event rail - target) in mV <= limit. |
| `test_undershoot_mv.py` | Low-to-high current step; max(0, target - min post-event rail) in mV <= limit. |
| `test_settle_time_ms.py` | Either direction; first sample after the last excursion outside target +/- settle_band_v, remaining inside through the observed tail for at least hold_s. |

Every block establishes initial current, enables the DUT supply, waits for
stabilization, presets/configures the scope, **arms without waiting**, changes
load current, waits for acquisition, and exports both channels. Initial rail
samples must meet `steady_tolerance_v`. Event time is the unique measured
current threshold crossing, linearly interpolated; CSV time zero need not be the
trigger origin. Sampling/record length must resolve both waveforms and cover
`pre_s` and `observation_s` around that event. `arm_delay_s` must allow the
qualified scope to become trigger-ready. A missed event, insufficient coverage,
ambiguous crossing or invalid samples produces ERROR; failure to remain settled
for the required hold within the observation window produces FAIL.

Raw rail/current CSVs and a structured response measurement are retained. Limits
are mV or ms as named, source/load/time settings use V/A/s. The helper computes
metrics from one capture, without Savitzky-Golay smoothing or hidden scope scalar
statistics. It supports numeric verify-only replay; full/procedure capture needs
persisted output and is incompatible with `--no-artifacts`.

Calibrate the current monitor's `current_v_per_a` and `current_zero_v`; its
pre-event and final-tail samples must confirm the requested initial/final load
within `current_tolerance_a`. Both intervals require at least two samples.
A current crossing without the intended step amplitude is not a valid test.
