# Rail voltage

**Start here** for power: set a PSU rail, measure with a DMM, and verify voltage.

## Plugins

- `colosseum-core`
- `colosseum-equipment`

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `psu_id` | `[equipment.psu]` id |
| `dmm_id` | `[equipment.dmm]` id |
| `dmm_channel` | DMM channel for the probe |
| `set_voltage_v` | PSU setpoint (V) |
| `current_limit_a` | PSU current limit (A) |
| `expected_voltage_v` | Verification target (V); optional if using `parameters.toml` |
| `voltage_tolerance_v` | Absolute tolerance (V); optional if using `parameters.toml` |

## Optional parameters file

Copy `parameters.toml.example` → `parameters.toml` (or pass `--parameters`) to supply
`[rail_v]` `expected_val` / `tolerance`. Instrument IDs stay as `FILL_IN_HERE` in
the script.

## Run

```sh
# After copy-out: fill FILL_IN_HERE; optionally export autoconfig IDs
colosseum run test_rail_voltage.py
colosseum run test_rail_voltage.py --config config.toml
colosseum run test_rail_voltage.py --config config.toml --parameters parameters.toml
colosseum run test_rail_voltage.py --config config.toml --report junit
```
