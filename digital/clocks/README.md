# Digital clocks

Probe/SMA on clock output; REF for alignment scripts.

## Building blocks

| Script | Block |
| --- | --- |
| `test_frequency.py` | frequency → tolerance |
| `test_jitter_rms.py` | jitter → max ps |
| `test_alignment_skew.py` | REF-DUT skew → max ns |
| `test_allan_deviation.py` | Allan σ(τ) → max |
