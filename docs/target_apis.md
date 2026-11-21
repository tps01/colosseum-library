# Catalog readiness

Fill each executable procedure's placeholders and follow its topic's bench
prerequisites. The complete catalog uses Equipment 0.25 for SPI target mode.
See the [copy-out instructions](reference_tests.md) for fixture setup and
helper files.

## API notes

- Spectrum analyzer trace analysis supports the half-power midpoint and 99% equal-tail occupied bandwidth.
- Set the GNSS receiver message profile with `set_message_profile` before calling `start_logging`.
- Scope frequency/rise/fall measurements use `measure_frequency_hz`,
  `measure_rise_time_s`, and `measure_fall_time_s`, after a fresh acquisition.
- Equipment eload `set_current`, `engage`, and `disengage` exist.
- Generic numeric acceptance uses Shared `verify_field(minimum=..., maximum=...)`.
- Power-meter frequency takes `frequency_hz`; peak and average have distinct APIs.
- VNA trace setup requires an explicit format; peak S21 is not worst insertion loss.

## Reference procedures

- [SPI](../digital/spi/README.md) covers controller transfers and a two-adapter
  target response. Target mode requires Equipment 0.25 or later.
- [JTAG](../digital/jtag/README.md) covers Vivado and Quartus inventory and
  scan workflows. Quartus requires Equipment 0.23 or later.
- The [offline Ethernet eye-mask check](../digital/ethernet/README.md#offline-eye-mask-reference)
  verifies saved scope captures against a supplied time-domain mask.
- The [measurement contracts](measurement_contracts.md) describe the evidence
  expected from the digital, timing, power, and RF reference blocks.

## Suite readiness

`.toml.example` files reference executable templates. `.toml.design` files are
reserved composition sketches and are not runnable suites. In particular, the
RF and GPIO edge designs still need stimulus, routing, capture
and cleanup contracts. A suite needs one coherent fixture; filenames alone do
not establish it.
