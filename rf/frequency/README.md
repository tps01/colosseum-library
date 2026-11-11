# RF frequency

Wideband scripts need trace save + SG smoothing.

## Building blocks

| Script | Block |
| --- | --- |
| `test_peak_frequency.py` | CW peak freq → expected |
| `test_center_frequency.py.design` (reserved) | wideband CF → expected |
| `test_occupied_bandwidth.py.design` (reserved) | OBW → max Hz |

## Bench hookup and prerequisites

Plugins: Equipment + Shared. VSG RF OUT -> DUT IN; DUT OUT -> analyzer RF IN through the qualified attenuator/DC block where required. Power/enable the DUT before RF. Set generator-port power with known input-path loss, and receiver span/RBW/VBW/attenuation/reference level for the intended carrier. Reference-lock instruments where required by the frequency uncertainty budget. The peak-frequency block requires carrier power above its presence threshold; it is not an oscillator-startup test. Wideband center/OBW designs need separate analysis definitions.

## RF output ownership

Each executable source-driven block owns its selected generator output(s),
starts with RF disabled and attempts output-off in `finally`, even if source
setup or analyzer acquisition fails. The two-source blocks attempt both outputs
independently. DUT DC power is externally owned and must already be stable;
these blocks do not power-cycle the DUT or change fixture routing.
