# SPI

CS/MOSI/MISO/SCK pin map.

## Building blocks

| Script | Block |
| --- | --- |
| `test_master_transfer.py` | transfer → pattern |
| `test_slave_response.py` | Full-duplex MOSI and MISO pattern checks |

## Bench hookup and prerequisites

Controller SCK/CS/MOSI -> DUT SCK/CS/SDI; DUT SDO -> controller MISO; share signal return and compatible voltage references. Define controller/target roles, CPOL/CPHA, bit order, word length, clock rate, CS polarity/timing and exact command/dummy/data bytes. Clocking an empty transmit string is not a defined read transaction by itself.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [master transfer](test_master_transfer.py) | Aardvark master, DUT slave, 8-bit MSB-first, active-low CS0. Wire a common return and use one read-only frame. |
| [slave response](test_slave_response.py) | Two Aardvarks with Equipment 0.25+. The controller sends one frame and the target returns a preloaded response. Compare both directions. |

For the slave-response setup, copy [config.slave_response.toml.example](config.slave_response.toml.example)
to `config.toml`. Enter a different serial number and SPI ID for each adapter,
then match the target row's mode to the procedure's `SETTINGS["mode"]`.
Connect SCK, CS0, MOSI, MISO, and ground between the adapters. Both use
8-bit MSB-first frames, active-low CS, and compatible 3.3 V signaling. Keep
adapter target power off. Use different MOSI and MISO patterns of equal length
and choose a clock suitable for the fixture.
