# Masking

## Building blocks

| Script | Block |
| --- | --- |
| `test_mask_margin_db.py` | mask margin → min dB |

## Bench hookup and prerequisites

Use a frequency-domain JSON mask with absolute Hz and dBm upper limits. The procedure checks full region coverage and reports the smallest margin and its frequency from the corrected unsmoothed trace.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [rf/rf_reference.py](../../rf/rf_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [mask margin db](test_mask_margin_db.py) | Prepare a stable DUT and fixed qualified analyzer sweep. Use a frequency JSON mask with absolute Hz and dBm keep_below regions. |
