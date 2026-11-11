# JTAG

10-pin Cortex or custom header.

## Building blocks

| Script | Block |
| --- | --- |
| `test_idcode.py.design` (reserved) | IDCODE → hex |
| `test_ir_dr_shift.py.design` (reserved) | DR shift → expected |

## Bench hookup and prerequisites

Reserved: no implemented JTAG adapter namespace. Map TCK/TMS/TDI/TDO, target voltage reference and return by signal, not just connector shape; map reset lines if the fixture uses them. Power the target, establish chain order and TAP reset, IR widths/instructions, clock rate and DR length/bit order. Do not assume an IDCODE transaction and an arbitrary DR shift have the same prerequisites.
