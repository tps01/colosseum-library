# Spurs

## Building blocks

| Script | Block |
| --- | --- |
| `test_spur_max_dbc.py` | spur dBc → max |

## Bench hookup and prerequisites

Use a calibrated analyzer with a fixed grid, detector and RBW. The procedure retains repeated unsmoothed sweeps and reports the highest included spur relative to a stable carrier.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [rf/rf_reference.py](../../rf/rf_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [spur max dbc](test_spur_max_dbc.py) | Preconfigure the analyzer for repeatable single sweeps with a fixed grid, RBW and detector. Qualify the output path, detector and worst-case detection level. Explicitly exclude the carrier, harmonic and modulation windows. |
