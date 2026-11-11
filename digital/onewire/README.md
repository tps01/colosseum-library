# 1-Wire

1-Wire on PCB header; parasitic vs external Vdd per script.

## Building blocks

| Script | Block |
| --- | --- |
| `test_rom_read.py.design` (reserved) | ROM read → match |
| `test_scratchpad_crc.py.design` (reserved) | scratchpad CRC → match |
| `test_parasitic_power.py.design` (reserved) | parasitic read → valid byte |
| `test_brownout_presence.py.design` (reserved) | presence at min V |

## Bench hookup and prerequisites

Reserved: no implemented 1-Wire adapter namespace. Adapter DQ -> DUT DQ, return -> return; use the correct pull-up supply and optional external VDD. Define ROM selection, bus reset/presence, command/byte sequence and timing. Parasitic operation needs a qualified strong pull-up during powered operations; a byte read alone is not proof of it. Brownout fixtures need a controlled VDD ramp/hold and restored nominal power. CRC must be recomputed over defined received bytes.
