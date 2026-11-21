# 1-Wire

1-Wire on a PCB header with a controlled external VDD supply.

## Building blocks

| Script | Block |
| --- | --- |
| `test_rom_read.py` | ROM read → match |
| `test_scratchpad_crc.py` | scratchpad CRC → match |
| `test_brownout_presence.py` | Falling and rising presence thresholds ? voltage window |

## Bench hookup and prerequisites

Connect adapter DQ to DUT DQ and return to return. Use the specified pull-up supply and external VDD. Define ROM selection, bus reset/presence, the command and byte sequence, and timing. Brownout fixtures need a controlled VDD ramp or hold and restored nominal power. Recompute CRC over the specified received bytes.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [digital/onewire/onewire_reference.py](../../digital/onewire/onewire_reference.py), [digital/onewire/brownout_reference.py](../../digital/onewire/brownout_reference.py), [digital/waveform_reference.py](../../digital/waveform_reference.py). Fill `SETTINGS` for the selected fixture. ROM and scratchpad use the 1-Wire helper. Brownout uses the brownout and waveform helpers.

| Procedure | Fixture |
| --- | --- |
| [rom read](test_rom_read.py) | Externally powered single DS18B20, DS9481R and standard-speed pull-up. Use the full eight-byte ROM in wire order. |
| [scratchpad crc](test_scratchpad_crc.py) | Same externally powered single-drop fixture. Verify a full DS18B20 scratchpad after conversion. |
| [brownout presence](test_brownout_presence.py) | Put actual DUT VDD on the first channel and the bus on the second. Verify the bus cannot back-power the DUT. Trigger on reset, with a full post-reset window and supply recovery. |
