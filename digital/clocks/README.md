# Digital clocks

Probe/SMA on clock output; REF for alignment scripts.

## Building blocks

| Script | Block |
| --- | --- |
| `test_frequency.py` | frequency → tolerance |
| `test_jitter_rms.py.design` (reserved) | jitter → max ps |
| `test_alignment_skew.py.design` (reserved) | REF-DUT skew → max ns |
| `test_allan_deviation.py.design` (reserved) | Allan σ(τ) → max |

## Bench hookup and prerequisites

Plugins: Equipment; Shared for promoted generic-bound procedures. Counter IN -> DUT CLK_OUT, return -> compatible signal return; configure impedance/coupling/trigger for the actual clock. Power and enable the DUT clock beforehand and establish any required frequency reference. The executable counter block reads a running clock; REF/DUT skew, jitter and Allan procedures remain designs and need their stated reference/statistical capabilities.
