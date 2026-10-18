# SPI

CS/MOSI/MISO/SCK pin map.

## Building blocks

| Script | Block |
| --- | --- |
| `test_master_transfer.py.design` (reserved) | transfer → pattern |
| `test_slave_response.py.design` (reserved) | slave read → expected |

## Bench hookup and prerequisites

Reserved: no implemented SPI adapter namespace. Controller SCK/CS/MOSI -> DUT SCK/CS/SDI; DUT SDO -> controller MISO; share signal return and compatible voltage references. Define controller/target roles, CPOL/CPHA, bit order, word length, clock rate, CS polarity/timing and exact command/dummy/data bytes. Clocking an empty transmit string is not a defined read transaction by itself.
