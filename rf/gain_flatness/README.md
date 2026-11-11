# Gain flatness

Sweep with optional SG on power series.

## Building blocks

| Script | Block |
| --- | --- |
| `test_gain_flatness_db.py.design` (reserved) | Gmax-Gmin → max dB |

## Bench hookup and prerequisites

Reserved derived method. VSG RF OUT -> DUT IN, DUT OUT -> analyzer, using reference-plane cable/attenuator correction over the entire band. Hold delivered input power constant (or measure/correct it), establish frequency sweep/settling and verify source/receiver linearity. Gain is corrected output minus corrected input in dB; flatness is max minus min of that gain series. Define missing-sample and optional smoothing behavior before promotion.
