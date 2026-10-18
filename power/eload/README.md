# Electronic load

Eload ramp and steady load.

The executable loaded-rail block requires `load_current_tolerance_a` for its
measured-current prerequisite and `slew_a_per_s` for controlled load engagement.
It presets the owned load to remove inherited transient/list/short state,
selects CC mode, and verifies actual current before accepting the DMM rail result.

## Building blocks

| Script | Block |
| --- | --- |
| `test_rail_voltage_under_load.py` | Vrail under load → min |
| `test_current_monotonic_ramp.py.design` (reserved) | ramp → monotonic |

## Bench hookup and prerequisites

Plugins: Equipment + Shared. Connect PSU to the DUT input and eload across the output under test, sharing the intended power return/sense reference. Define source current budget, CC mode, compliance/power ratings, target current and settling. The loaded-rail block measures an independent DMM at DUT OUT (HI) and output return (LO), not PSU readback. Fill separate supply_v (input) and min_voltage_v (output), source current limit, source timeout/tolerance, DUT startup allowance and load settling. It starts with supply off/load disengaged, selects CC mode, waits for source voltage, then measures after loading. Finally it disengages the load and disables the source, including after setup/acquisition failure. The monotonic-ramp procedure remains a design and must compare measured current samples rather than only commanded values.
