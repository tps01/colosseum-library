# Target APIs (TDD contracts)

Catalog scripts call `col.*` plugin APIs. Many calls are **not implemented yet**;
the library defines the contract equipment and shared code must grow into. Do not
implement these APIs in `colosseum-library` — they belong in first-party plugins.

Status legend: **exists** (callable today), **TDD** (referenced by catalog, not yet shipped).

## `col.shared.signal` (colosseum-shared) — TDD

Pure trace math and derived RF metrics. Works on CSV traces under the run directory
(`frequency_hz`, `amplitude_dbm` columns) and/or orchestrates instrument sweeps.

| API | Status | Used by |
|-----|--------|---------|
| `savitzky_golay(values, window_length, polyorder)` | TDD | Internal to trace analysis |
| `measure_center_frequency(trace_path, key, sg_window_length, sg_polyorder, start_hz, stop_hz)` | TDD | `rf/frequency/test_center_frequency.py` |
| `measure_occupied_bandwidth(trace_path, key, sg_window_length, sg_polyorder, start_hz, stop_hz, threshold_db)` | TDD | `rf/frequency/test_occupied_bandwidth.py` |
| `measure_peak_power_dbm(...)` | TDD | Reserved for wideband peak blocks |
| `save_smoothed_trace(trace_path, out_path, sg_window_length, sg_polyorder)` | TDD | Optional artifact |
| `measure_mask_margin_db(trace_path, mask_path, sg_window_length, sg_polyorder, key)` | TDD | `rf/masking/test_mask_margin_db.py` |
| `measure_spur_max_dbc(trace_path, fundamental_hz, sg_window_length, sg_polyorder, key)` | TDD | `rf/spurs/test_spur_max_dbc.py` |
| `measure_gain_flatness(vsg_id, speca_id, freq_start_hz, freq_stop_hz, freq_step_hz, sg_window_length, sg_polyorder, key)` | TDD | `rf/gain_flatness/test_gain_flatness_db.py` |
| `measure_harmonic_dbc(speca_id, fundamental_hz, harmonic, key)` | TDD | `rf/harmonics/test_h2_dbc.py`, `test_h3_dbc.py` |
| `measure_oip3(vsg_id, speca_id, f1_hz, f2_hz, im3_hz, key)` | TDD | `rf/ip2_ip3/test_oip3_dbm.py` |
| `measure_p1db(vsg_id, speca_id, pin_start_dbm, pin_stop_dbm, pin_step_db, key)` | TDD | `rf/p1db/test_p1db_compression_dbm.py` |
| `measure_s21_max(vna_id, trace, key)` | TDD | `rf/insertion_loss/test_s21_max_db.py` |
| `measure_s11_max(vna_id, trace, key)` | TDD | `rf/return_loss/test_s11_max_db.py` |
| `measure_band_power_dbm(speca_id, start_hz, stop_hz, key)` | TDD | `rf/power_meter/test_band_power_dbm.py` |
| `ramp_eload_current(eload_id, i_start_a, i_stop_a, rate_a_per_s, key)` | TDD | `power/eload/test_current_monotonic_ramp.py` |

### Savitzky–Golay alignment note

`col.equipment.speca.measure_bw` documents Savitzky–Golay smoothing, but
`measure_bandwidth_hz` in equipment currently uses a simple moving average.
Phase 3 equipment work: refactor to call `col.shared.signal.savitzky_golay`,
rename `smoothing_order` → `sg_window_length` + `sg_polyorder`.

Implement SG in **stdlib-only** shared code unless a compliant numpy/scipy path
already exists in equipment (see `colosseum-core/RULES.md` license allowlist).

## `col.io.*` (colosseum-equipment) — mostly TDD

| API | Status | Used by |
|-----|--------|---------|
| `col.io.dio.configure`, `write_pin`, `read_pin` | **exists** | `digital/gpio/*` |
| `col.io.onewire.read_rom`, `read_scratchpad`, `read_byte`, `verify_presence` | TDD | `digital/onewire/*` |
| `col.io.i2c.write_read`, `probe` | TDD | `digital/i2c/*` |
| `col.io.spi.transfer` | TDD | `digital/spi/*` |
| `col.io.jtag.read_idcode`, `shift_dr` | TDD | `digital/jtag/*` |

## `col.equipment.oscope` — partial TDD

| API | Status | Used by |
|-----|--------|---------|
| `measure_jitter(oscope_id, channel, key)` | TDD | `digital/clocks/test_jitter_rms.py` |
| `measure_phase_delay(oscope_id, ref_channel, dut_channel, key)` | TDD | `digital/clocks/test_alignment_skew.py` |
| `measure_frequency(oscope_id, channel, key)` | TDD | `digital/tachometer_pwm/test_pwm_frequency.py` |
| `measure_duty_cycle(oscope_id, channel, key)` | TDD | `digital/tachometer_pwm/test_pwm_duty_cycle.py` |
| `measure_rise_time`, `measure_fall_time` | TDD | `digital/gpio/test_rise_time.py`, `test_fall_time.py` |
| `measure_vpp` / DMM voltage | TDD | `digital/gpio/test_output_voltage_*.py` |
| `measure_common_mode`, `measure_differential` | TDD | `digital/gpio/test_common_mode_voltage.py`, `test_differential_voltage.py` |
| `measure_eye_height` | TDD | `digital/ethernet/test_eye_height_mv.py` |
| `measure_overshoot_mv`, `measure_undershoot_mv`, `measure_settle_time` | TDD | `power/transient/*` |

## `col.equipment.freqcounter` — **exists**

Used by `digital/clocks/test_frequency.py`.

## `col.equipment.fs740` — TDD

| API | Used by |
|-----|---------|
| `measure_allan(fs740_id, tau_s, duration_s, key)` | `rf/allan_deviation/test_allan_sigma.py`, `digital/clocks/test_allan_deviation.py` |

## `col.equipment.vsg`, `speca`, `vna`, `pwrmeter` — mostly **exists**

Existing marker, sweep, and power APIs cover CW peak frequency, harmonics
fundamental power, dual-tone blocks, VNA S11/S21 spot markers, and pwrmeter avg/peak.

TDD additions on speca side: mask overlay artifact (`save_trace_with_mask`).

## `col.equipment.psu`, `eload` — partial

PSU set/measure/verify: **exists** (`power/rail_voltage`, `power/eload`).

Eload engage/disengage/set_current: TDD (referenced by transient and eload blocks).

## `col.host.net`, `col.messaging.ssh`, `col.shared.regex` — partial TDD

| API | Used by |
|-----|---------|
| `col.host.net.measure_operstate`, `verify_operstate_up` | `digital/ethernet/test_link_up.py` |
| SSH stdout + `col.shared.regex.verify_match` | `digital/ethernet/test_ping_reachability.py`, throughput, BER |
| `col.messaging.ssh.measure_stdout` | `digital/tachometer_pwm/test_fan_command_ack.py` |

## `col.shared.verify` — **exists**

Generic `verify_field`, `verify_measurement_exists` used across the catalog when
no dedicated instrument verifier exists.

## Runnable today (Phase 2 priority)

Scripts that can run with current equipment after filling `FILL_IN_HERE`:

- `digital/gpio/test_output_high.py`, `test_output_low.py`, `test_loopback_pattern.py`
- `digital/ethernet/test_link_up.py` (with host TOML)
- `power/rail_voltage/test_rail_voltage.py`
- `rf/insertion_loss/*`, `rf/return_loss/*` (VNA)
- `rf/frequency/test_peak_frequency.py`, `rf/harmonics/test_fundamental_power.py`
- `rf/power_meter/test_avg_power_dbm.py`

All other blocks depend on TDD APIs listed above.
