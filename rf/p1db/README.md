# P1dB

Input power sweep.

## Building blocks

| Script | Block |
| --- | --- |
| `test_p1db_compression_dbm.py.design` (reserved) | P1dB → minimum |

## Bench hookup and prerequisites

Reserved derived method. Calibrated CW source -> DUT input; calibrated output tap/attenuator -> linear receiver. Power/enable the DUT and fix frequency, bias, load and temperature conditions. Specify corrected input/output planes, a linear-region gain estimate, sweep direction/step/settling, permitted power/current stop and recovery. Define input versus output P1dB and interpolate the 1 dB gain-compression crossing; source or analyzer compression invalidates DUT attribution.
