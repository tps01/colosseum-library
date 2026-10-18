# Masking

Mask CSV alongside trace; SG smoothing required.

## Building blocks

| Script | Block |
| --- | --- |
| `test_mask_margin_db.py.design` (reserved) | mask margin → min dB |

## Bench hookup and prerequisites

Reserved margin-analysis design. DUT output -> analyzer at the specified corrected measurement plane; establish DUT stimulus/mode and instrument acquisition settings. Define mask axes, units, interpolation, limits and the sign of margin, and retain the exact trace/mask. Existing Equipment JSON mask pass/fail is a different supported workflow; the proposed CSV/SG minimum-margin method must not be presented as implemented.
