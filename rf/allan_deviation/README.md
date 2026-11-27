# RF Allan deviation

Overlapping Allan deviation from a simultaneous DUT and reference clock capture.

## Building blocks

| Script | Block |
| --- | --- |
| `test_allan_sigma.py` | Allan σ → max |

## Bench hookup and prerequisites

Use a simultaneous scope capture of the DUT and an independent reference at the same nominal frequency. A qualified divider can bring the RF signal into scope bandwidth.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [digital/waveform_reference.py](../../digital/waveform_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [allan sigma](test_allan_sigma.py) | Scope DUT and stable reference at the same nominal frequency, with a qualified RF divider if needed. Tau limits are [seconds, sigma_y_max] pairs. |
