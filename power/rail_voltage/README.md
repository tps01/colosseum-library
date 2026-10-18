# Rail voltage

**Start here** for power: set a PSU rail, measure with a DMM, and verify voltage.

## Plugins

- `colosseum-core`
- `colosseum-equipment`
- `colosseum-shared`

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `psu_id` | `[equipment.psu]` id |
| `dmm_id` | `[equipment.dmm]` id |
| `dmm_channel` | DMM channel for the probe |
| `set_voltage_v` | PSU setpoint (V) |
| `current_limit_a` | PSU current limit (A) |
| `source_timeout_s` | Deadline for source voltage readiness (s) |
| `source_tolerance_v` | Source voltage readiness half-band (V) |
| `dut_settle_s` | Qualified startup allowance after source readiness (s) |

## Parameters file

Copy `parameters.toml.example` → `parameters.toml` (or pass `--parameters`) to supply
`[rail_v]` `expected_val` / `tolerance`. Instrument IDs stay as `FILL_IN_HERE` in
the script.

The script omits inline limits so the parameters file controls acceptance. For
an inline-only variant, pass `expected_val=` and `tolerance=` to
`verify_voltage`; those explicit values override the file when both are present.

## Run

```sh
# After copy-out: fill FILL_IN_HERE; optionally export autoconfig IDs
colosseum run test_rail_voltage.py
colosseum run test_rail_voltage.py --config config.toml
colosseum run test_rail_voltage.py --config config.toml --parameters parameters.toml
colosseum run test_rail_voltage.py --config config.toml --report junit
```

## Bench hookup and prerequisites

Plugins: Equipment (PSU + DC DMM). PSU +/return -> DUT input supply/return. DMM HI -> the named DUT rail test point, LO -> its return; use the actual DMM input/channel, not an invented scan channel. Establish DUT enable/control mode, source current budget and expected rail limits. Copy/fill `parameters.toml` with `[rail_v] expected_val/tolerance` or pass `--parameters`; this script requires those limits. The PSU setpoint need not equal the DUT rail target. Stabilization and source lifecycle must follow the owning bench/suite contract.

## Owned supply lifecycle

Requires Shared for the qualified `dut_settle_s` startup allowance. This block
starts with its PSU output off, sets voltage/current limit, enables output, waits
for measured source voltage within `source_tolerance_v` for at most
`source_timeout_s`, then waits for DUT startup and reads the DMM. Source voltage
readiness alone is not DUT readiness. It always attempts output-off in `finally`.
The block owns this output; do not use it on a supply shared with unrelated loads.
Limits still come from the filled `parameters.toml` file.
