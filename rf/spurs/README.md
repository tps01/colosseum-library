# Spurs

Max-hold trace; SG smoothing.

## Building blocks

| Script | Block |
| --- | --- |
| `test_spur_max_dbc.py.design` (reserved) | spur dBc → max |

## Bench hookup and prerequisites

Reserved derived method. DUT RF output -> analyzer through the qualified reference-plane correction path; if driven, establish its source frequency/power and DUT mode. Define the band, RBW/detector, observation/max-hold duration, fundamental reference, carrier/harmonic exclusion regions and noise-floor validity. Retain the trace and define whether smoothing may hide a narrow spur before implementing a worst-spur dBc metric.
