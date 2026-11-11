# RF Allan deviation

FS740; 10 MHz ref; DUT LO input.

## Building blocks

| Script | Block |
| --- | --- |
| `test_allan_sigma.py.design` (reserved) | Allan σ → max |

## Bench hookup and prerequisites

Reserved: FS740/Allan API absent. Route DUT clock/LO and the independent reference to the specified measurement/reference inputs with compatible levels/termination. Define reference quality, sample interval, duration, tau values and overlapping/non-overlapping statistic, dead time and missing-sample policy. No config file can supply the missing acquisition/statistical implementation.
