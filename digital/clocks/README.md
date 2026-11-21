# Digital clocks

Probe/SMA on clock output; REF for alignment scripts.

## Building blocks

| Script | Block |
| --- | --- |
| `test_frequency.py` | frequency → tolerance |
| `test_jitter_rms.py` | jitter → max ps |
| `test_alignment_skew.py` | REF-DUT skew → max ns |
| `test_allan_deviation.py` | Allan σ(τ) → max |

## Bench hookup and prerequisites

Plugins: Equipment; Shared for promoted generic-bound procedures. Counter IN -> DUT CLK_OUT, return -> compatible signal return; configure impedance/coupling/trigger for the actual clock. Power and enable the DUT clock beforehand and establish any required frequency reference. The executable counter block reads a running clock; REF/DUT skew, jitter and Allan procedures remain designs and need their stated reference/statistical capabilities.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [digital/waveform_reference.py](../../digital/waveform_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [alignment skew](test_alignment_skew.py) | Same scope acquisition on A and B, with calibrated deskew and matching edges. Limits apply to B minus A. |
| [jitter rms](test_jitter_rms.py) | Prepare a repetitive DUT clock and qualify scope timebase, bandwidth and noise. Metric is period jitter in seconds RMS. |
| [allan deviation](test_allan_deviation.py) | Scope DUT and stable reference at the same nominal frequency, with a qualified RF divider if needed. Tau limits are [seconds, sigma_y_max] pairs. |
