# RF frequency

## Building blocks

| Script | Block |
| --- | --- |
| `test_peak_frequency.py` | CW peak freq → expected |
| `test_center_frequency.py` | Midpoint of the dominant signal's half-power crossings, in Hz |
| `test_occupied_bandwidth.py` | Width containing 99% of integrated power with 0.5% in each tail, in Hz |

## Bench hookup and prerequisites

For CW peak frequency, connect VSG RF OUT to DUT IN and DUT OUT to analyzer RF
IN through a qualified attenuator/DC block where required. Power and enable the
DUT before RF. Set generator-port power with known input-path loss, and set the
analyzer span, RBW, VBW, attenuation and reference level for the intended carrier.
The procedure checks carrier power before verifying peak frequency.

## Wideband setup

Copy the topic folder including `wideband_trace.py`. Use Equipment 0.20 and
Shared 0.9 or compatible later versions. Only the `equipment.speca` row is
needed for either wideband block. Set the live driver, model and address for
your analyzer, then prepare a stable modulated signal from the DUT or an
external source. Establish a flat response over the analysis band from the
DUT output reference plane to the analyzer input. Reference-lock instruments
when required by the uncertainty budget.

Choose a sweep and analysis window that cover the entire signal plus quiet
guard bands on both sides. Fill the sweep point count, RBW/VBW and detector for
the signal and analyzer model. Use a detector qualified for power measurements,
with constant effective RBW and no trace averaging. Set attenuation and
reference level to avoid overload, and choose the minimum peak and maximum
guard levels at the analyzer input using a qualified reference capture.
Integrated power uses the measured noise floor without subtraction. Qualify the
noise contribution, frequency accuracy and coverage before choosing limits.

Each block presets the analyzer, takes one completed sweep, and saves the
unsmoothed CSV and an annotated plot. The plot evidence includes both edge
frequencies. Keep artifacts enabled. Both blocks leave stimulus control and
shutdown to the fixture.

```sh
colosseum run test_center_frequency.py --config config.toml
colosseum run test_occupied_bandwidth.py --config config.toml
```

## RF output ownership

Each executable source-driven block owns its selected generator output(s),
starts with RF disabled and attempts output-off in `finally`, even if source
setup or analyzer acquisition fails. The two-source blocks attempt both outputs
independently. DUT DC power is externally owned and must already be stable;
these blocks do not power-cycle the DUT or change fixture routing.
