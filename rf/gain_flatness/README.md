# Gain flatness

## Building blocks

| Script | Block |
| --- | --- |
| `test_gain_flatness_db.py` | Gmax-Gmin → max dB |

## Bench hookup and prerequisites

Use a calibrated VNA S21 log-magnitude sweep at the DUT reference planes. Establish linear DUT operation, and keep the declared passband inside the calibrated sweep.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [rf/rf_reference.py](../../rf/rf_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [gain flatness db](test_gain_flatness_db.py) | Use a calibrated, linear VNA S21 fixture. Bench owns VNA stimulus. Preconfigure sweep, IFBW, point count, source level and calibration. |
