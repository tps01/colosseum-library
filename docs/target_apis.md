# Target APIs (TDD specifications)

Catalog scripts call `col.*` plugin APIs. Many calls are **not implemented
yet**;
the library defines the API specification that equipment and shared code must
grow into. Do
not
implement these APIs in `colosseum-library` — they belong in first-party
plugins.

Status legend: **exists** (callable today), **TDD** (referenced by catalog, not
yet shipped).

## `col.shared.signal` (colosseum-shared) — TDD

Pure trace math and derived RF metrics. Works on CSV traces under the run
directory
(`frequency_hz`, `amplitude_dbm` columns) and/or orchestrates instrument sweeps.

| API | Status | Used by |
| --- | --- | --- |
| `savitzky_golay(...)` | TDD | Internal to trace analysis |
| `measure_center_frequency(...)` | TDD | `rf/frequ... |
| `measure_occupied_bandwidth(...)` | TDD | `rf/frequ... |
| `measure_peak_power_dbm(...)` | TDD | Reserved for wideband peak blocks |
| `save_smoothed_trace(...)` | TDD | Optional artifact |
| `measure_mask_margin_db(...)` | TDD | `rf/masking/test_mask_margin_db.py` |
| `measure_spur_max_dbc(...)` | TDD | `rf/spurs/test_spur_max_dbc.py` |
| `measure_gain_flatness(...)` | TDD | `rf/gain_... |
| `measure_harmonic_dbc(...)` | TDD | `rf/harmo... |
| `measure_oip3(...)` | TDD | `rf/ip2_ip3/test_oip3_dbm.py` |
| `measure_p1db(...)` | TDD | `rf/p1db/test_p1db_compression_dbm.py` |
| `measure_s21_max(vna_id, trace, key)` | TDD | `rf/inser... |
| `measure_s11_max(...)` | TDD | `rf/return_loss/test_s11_max_db.py` |
| `measure_band_power_dbm(...)` | TDD | `rf/power... |
| `ramp_eload_current(...)` | TDD | `power/el... |

### Savitzky–Golay alignment note

`col.equipment.speca.measure_bw` documents Savitzky–Golay smoothing, but
`measure_bandwidth_hz` in equipment currently uses a simple moving average.
Phase 3 equipment work: refactor to call `col.shared.signal.savitzky_golay`,
rename `smoothing_order` → `sg_window_length` + `sg_polyorder`.

Implement SG in **stdlib-only** shared code unless a compliant numpy/scipy path
already exists in equipment (see `colosseum-core/RULES.md` license allowlist).

## `col.io.*` (colosseum-equipment) — mostly TDD

| API | Status | Used by |
| --- | --- | --- |
| `col.io.d... | **exists** | `digital/gpio/*` |
| `col.io.o... | TDD | `digital/onewire/*` |
| `col.io.i2c.write_read`, `probe` | TDD | `digital/i2c/*` |
| `col.io.spi.transfer` | TDD | `digital/spi/*` |
| `col.io.jtag.read_idcode`, `shift_dr` | TDD | `digital/jtag/*` |

## `col.equipment.oscope` — partial TDD

| API | Status | Used by |
| --- | --- | --- |
| `measure_jitter(...)` | TDD | `digital/clocks/test_jitter_rms.py` |
| `measure_phase_delay(...)` | TDD | `digital/clocks/test_alignment_skew.py` |
| `measure_frequency(oscope_id, channel, key)` | TDD | `digital/... |
| `measure_duty_cycle(oscope_id, channel, key)` | TDD | `digital/... |
| `measure_rise_time`, `measure_fall_time` | TDD | `digital/... |
| `measure_vpp` / DMM voltage | TDD | `digital/gpio/test_output_voltage_*.py` |
| `measure_common_mode`, `measure_differential` | TDD | `digital/... |
| `measure_eye_height` | TDD | `digital/ethernet/test_eye_height_mv.py` |
| `measure_... | TDD | `power/transient/*` |

## `col.equipment.freqcounter` — **exists**

Used by `digital/clocks/test_frequency.py`.

## `col.equipment.fs740` — TDD

| API | Used by |
| --- | --- |
| `measure_allan(fs740_id, tau_s, duration_s, key)` | `rf/allan... |

## `col.equipment.vsg`, `speca`, `vna`, `pwrmeter` — mostly **exists**

Existing marker, sweep, and power APIs cover CW peak frequency, harmonics
fundamental power, dual-tone blocks, VNA S11/S21 spot markers, and pwrmeter
avg/peak.

TDD additions on speca side: mask overlay artifact (`save_trace_with_mask`).

## `col.equipment.psu`, `eload` — partial

PSU set/measure/verify: **exists** (`power/rail_voltage`, `power/eload`).

Eload engage/disengage/set_current: TDD (referenced by transient and eload
blocks).

## `col.host.net`, `col.messaging.ssh`, `col.shared.regex` — partial TDD

| API | Used by |
| --- | --- |
| `col.host... | `digital/ethernet/test_link_up.py` |
| SSH stdout + `col.shared.regex.verify_match` | `digital/... |
| `col.messaging.ssh.measure_stdout` | `digital/... |

## `col.shared.verify` — **exists**

Generic `verify_field`, `verify_measurement_exists` used across the catalog when
no dedicated instrument verifier exists.

## `col.gui.web` / `col.gui.desktop` (colosseum-gui) — **exists** (sim + adapters)

Web and desktop are separate kinds. Drivers: web `sim`|`playwright`; desktop
`sim`|`generic`|`pywinauto` (Windows-only for pywinauto). Generic commands are
best-effort; tree locators raise `GuiCapabilityError` on the wrong driver.

| API | Status | Used by |
| --- | --- | --- |
| `col.gui.... | **exists** | `gui/web/button_visible` |
| `col.gui.... | **exists** | `gui/web/screenshot_match` |
| `col.gui.... | **exists** | `gui/web/contrast_ratio` |
| `col.gui.... | **exists** | `gui/web/navigation_ms` |
| `col.gui.desktop.click(image=)` | **exists** | `gui/desktop/image_click` |
| `col.gui.desktop.click(...)` | **exists** | `gui/desktop/uia_click` |
| `col.gui.... | **exists** | `gui/desktop/screenshot_match` |

## Runnable today (Phase 2 priority)

Scripts that can run with current equipment after filling `FILL_IN_HERE`:

- `digital/gpio/test_output_high.py`, `test_output_low.py`,
  `test_loopback_pattern.py`
- `digital/ethernet/test_link_up.py` (with host TOML)
- `power/rail_voltage/test_rail_voltage.py`
- `rf/insertion_loss/*`, `rf/return_loss/*` (VNA)
- `rf/frequency/test_peak_frequency.py`,
  `rf/harmonics/test_fundamental_power.py`
- `rf/power_meter/test_avg_power_dbm.py`

All other blocks depend on TDD APIs listed above.
