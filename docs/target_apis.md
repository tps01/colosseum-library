# Catalog readiness and reserved procedures

This is copy-out testware. A `.py` file is an executable procedure template: fill
its placeholders and establish its stated bench prerequisites. A `.py.design`
file is a **non-executable design**, retained because it needs a supported acquisition/transport and measurement contract. Renaming a design or filling its values does not implement it.

The executable templates have been checked against the current local core
0.17.1, equipment 0.5.0, Shared 0.5.0, host 0.4.3, messaging 0.4.3 and GUI 0.3.3
sources. This is an API check, not a claim of live-bench qualification.

## Implemented equivalents worth using

- Scope frequency/rise/fall measurements use `measure_frequency_hz`,
  `measure_rise_time_s`, and `measure_fall_time_s`, after a fresh acquisition.
- Equipment eload `set_current`, `engage`, and `disengage` exist.
- Generic numeric acceptance uses Shared `verify_field(minimum=..., maximum=...)`.
- Power-meter frequency takes `frequency_hz`; peak and average have distinct APIs.
- VNA trace setup requires an explicit format; peak S21 is not worst insertion loss.

## Reserved procedure designs

Implement or revise the measurement contract before promoting a design to `.py`.
Protocol adapters, Allan/jitter/eye metrics and derived RF analysis need
method/capability decisions; this table does not authorize a new Shared signal
namespace or prescribe a new plugin API. Define calibration, units, bounds, events, references, CRC and smoothing
before implementing or promoting these proposals. See the concrete
[measurement contracts](measurement_contracts.md). Speculative code has been removed
from the reserved slots; these names do not imply implemented APIs.

| Design | Missing measurement/transport capability |
| --- | --- |
| [digital/clocks/test_alignment_skew.py.design](../digital/clocks/test_alignment_skew.py.design) | Simultaneous calibrated signed edge skew |
| [digital/clocks/test_allan_deviation.py.design](../digital/clocks/test_allan_deviation.py.design) | Sampled fractional-frequency Allan deviation |
| [digital/clocks/test_jitter_rms.py.design](../digital/clocks/test_jitter_rms.py.design) | Defined timestamp-based RMS jitter |
| [digital/ethernet/test_eye_height_mv.py.design](../digital/ethernet/test_eye_height_mv.py.design) | PHY-qualified eye acquisition and height statistic |
| [digital/gpio/test_common_mode_voltage.py.design](../digital/gpio/test_common_mode_voltage.py.design) | Simultaneous calibrated common-mode voltage |
| [digital/gpio/test_differential_voltage.py.design](../digital/gpio/test_differential_voltage.py.design) | Simultaneous calibrated differential voltage |
| [digital/i2c/test_master_write_read.py.design](../digital/i2c/test_master_write_read.py.design) | I2C transaction transport and byte/ACK evidence |
| [digital/i2c/test_slave_ack.py.design](../digital/i2c/test_slave_ack.py.design) | Non-destructive I2C probe and actual ACK evidence |
| [digital/jtag/test_idcode.py.design](../digital/jtag/test_idcode.py.design) | Chain-aware JTAG IDCODE transport and comparison |
| [digital/jtag/test_ir_dr_shift.py.design](../digital/jtag/test_ir_dr_shift.py.design) | Chain-aware JTAG IR/DR transport and bit comparison |
| [digital/onewire/test_brownout_presence.py.design](../digital/onewire/test_brownout_presence.py.design) | Measured supply sequence and acquired presence-pulse evidence |
| [digital/onewire/test_parasitic_power.py.design](../digital/onewire/test_parasitic_power.py.design) | Qualified strong-pull-up operation without external VDD |
| [digital/onewire/test_rom_read.py.design](../digital/onewire/test_rom_read.py.design) | 1-Wire ROM transport, addressing and CRC evidence |
| [digital/onewire/test_scratchpad_crc.py.design](../digital/onewire/test_scratchpad_crc.py.design) | 1-Wire scratchpad transport and CRC over received bytes |
| [digital/spi/test_master_transfer.py.design](../digital/spi/test_master_transfer.py.design) | SPI master transfer and byte evidence |
| [digital/spi/test_slave_response.py.design](../digital/spi/test_slave_response.py.design) | Slave-capable SPI fixture and response evidence |
| [digital/tachometer_pwm/test_pwm_duty_cycle.py.design](../digital/tachometer_pwm/test_pwm_duty_cycle.py.design) | Repetitive waveform capture and duty-cycle statistic |
| [power/eload/test_current_monotonic_ramp.py.design](../power/eload/test_current_monotonic_ramp.py.design) | Independent timestamped current and compliance evidence |
| [rf/allan_deviation/test_allan_sigma.py.design](../rf/allan_deviation/test_allan_sigma.py.design) | Sampled fractional-frequency Allan deviation |
| [rf/frequency/test_center_frequency.py.design](../rf/frequency/test_center_frequency.py.design) | Explicit center-frequency definition and trace acquisition |
| [rf/frequency/test_occupied_bandwidth.py.design](../rf/frequency/test_occupied_bandwidth.py.design) | Integrated-power OBW with declared percentage and band edges |
| [rf/gain_flatness/test_gain_flatness_db.py.design](../rf/gain_flatness/test_gain_flatness_db.py.design) | Corrected unsmoothed gain versus frequency |
| [rf/harmonics/test_h2_dbc.py.design](../rf/harmonics/test_h2_dbc.py.design) | Corrected H2 and fundamental measurement |
| [rf/harmonics/test_h3_dbc.py.design](../rf/harmonics/test_h3_dbc.py.design) | Corrected H3 and fundamental measurement |
| [rf/ip2_ip3/test_oip3_dbm.py.design](../rf/ip2_ip3/test_oip3_dbm.py.design) | Qualified balanced-tone carriers and both IM3 products |
| [rf/masking/test_mask_margin_db.py.design](../rf/masking/test_mask_margin_db.py.design) | Full unsmoothed trace-to-mask comparison |
| [rf/p1db/test_p1db_compression_dbm.py.design](../rf/p1db/test_p1db_compression_dbm.py.design) | Calibrated power sweep and compression crossing |
| [rf/power_meter/test_band_power_dbm.py.design](../rf/power_meter/test_band_power_dbm.py.design) | Calibrated selected-band linear-power integration |
| [rf/spurs/test_spur_max_dbc.py.design](../rf/spurs/test_spur_max_dbc.py.design) | Unsmoothed spur search with explicit reference and exclusions |

## Suite readiness

`.toml.example` files reference executable templates. `.toml.design` files are
reserved composition sketches and are not runnable suites. In particular, the
RF and GPIO edge designs still need stimulus, routing, capture
and cleanup contracts. A suite needs one coherent fixture; filenames alone do
not establish it.
