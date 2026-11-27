# P1dB

Input power sweep.

## Building blocks

| Script | Block |
| --- | --- |
| `test_p1db_compression_dbm.py` | P1dB → minimum |

## Bench hookup and prerequisites

Use a calibrated CW source and independent calibrated power sensors at the DUT input and output taps. Fix bias, load and temperature, and qualify the permitted power and current over the sweep.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [rf/rf_reference.py](../../rf/rf_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [p1db compression dbm](test_p1db_compression_dbm.py) | Use independently calibrated input and output taps/meters; qualify analyzer and source linearity and DUT power, current, recovery and thermal conditions across the sweep. |
