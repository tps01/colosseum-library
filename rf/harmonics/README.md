# Harmonics

Single CW tone; marker at n×f0.

## Building blocks

| Script | Block |
| --- | --- |
| `test_fundamental_power.py` | fundamental → expected dBm |
| `test_h2_dbc.py.design` (reserved) | H2 dBc → max |
| `test_h3_dbc.py.design` (reserved) | H3 dBc → max |

## Bench hookup and prerequisites

Plugins: Equipment + Shared. VSG RF OUT -> DUT input, DUT output -> analyzer through the calibrated output path. Establish CW frequency/power, DUT bias/mode and safe analyzer input range. Fundamental power is measured at a selected marker after a new sweep. H2/H3 remain designs: they require a measured fundamental reference, frequency-dependent path correction, enough dynamic range and a source/analyzer distortion check before a dBc value can be attributed to the DUT.

## RF output ownership

Each executable source-driven block owns its selected generator output(s),
starts with RF disabled and attempts output-off in `finally`, even if source
setup or analyzer acquisition fails. The two-source blocks attempt both outputs
independently. DUT DC power is externally owned and must already be stable;
these blocks do not power-cycle the DUT or change fixture routing.
