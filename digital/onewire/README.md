# 1-Wire

1-Wire on PCB header; parasitic vs external Vdd per script.

## Building blocks

| Script | Block |
|--------|-------|
| `test_rom_read.py` | ROM read → match |
| `test_scratchpad_crc.py` | scratchpad CRC → match |
| `test_parasitic_power.py` | parasitic read → valid byte |
| `test_brownout_presence.py` | presence at min V |
