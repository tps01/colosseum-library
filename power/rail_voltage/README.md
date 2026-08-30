# Rail voltage

Set a PSU rail, measure with a DMM, and verify the expected voltage.

## Plugins

- `colosseum-core`
- `colosseum-equipment`

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `psu_id` | `[[equipment.psu]]` id |
| `dmm_id` | `[[equipment.dmm]]` id |
| `dmm_channel` | DMM channel for the probe |
| `set_voltage_v` | PSU setpoint (V) |
| `current_limit_a` | PSU current limit (A) |
| `expected_voltage_v` | Verification target (V) |
| `voltage_tolerance_v` | Absolute tolerance (V) |

## Run

```sh
# After copy-out: fill FILL_IN_HERE; optionally export autoconfig IDs
colosseum run test_rail_voltage.py
colosseum run test_rail_voltage.py --config config.toml
```
