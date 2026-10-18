# IP2 / IP3

Dual-tone; tones 1 MHz apart.

## Building blocks

| Script | Block |
| --- | --- |
| `test_tone_f1_power.py` | f1 power → expected |
| `test_tone_f2_power.py` | f2 power → expected |
| `test_im3_product_power.py` | IM3 power → limit |
| `test_oip3_dbm.py.design` (reserved) | OIP3 → minimum |

## Bench hookup and prerequisites

Plugins: Equipment + Shared. The executable tone/IM3 blocks use TWO independent CW sources: each RF OUT -> its isolator/combiner input; combiner OUT -> DUT IN; DUT OUT -> analyzer through the qualified correction/attenuation path. Use distinct source IDs and explicit f1/f2 and per-source generator-port levels. Characterize combiner isolation, delivered per-tone power, source spur levels and analyzer linearity first. Span must isolate the selected component. IM3 checks both output carriers before applying its upper limit; OIP3 remains a reserved derived-method design.

## RF output ownership

Each executable source-driven block owns its selected generator output(s),
starts with RF disabled and attempts output-off in `finally`, even if source
setup or analyzer acquisition fails. The two-source blocks attempt both outputs
independently. DUT DC power is externally owned and must already be stable;
these blocks do not power-cycle the DUT or change fixture routing.
