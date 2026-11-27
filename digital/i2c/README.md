# I2C

Level shifters if DUT is 1.8 V.

## Building blocks

| Script | Block |
| --- | --- |
| `test_master_write_read.py` | write/read → match |
| `test_slave_ack.py` | probe → ACK |

## Bench hookup and prerequisites

Adapter SCL -> DUT SCL, SDA -> SDA, return -> return; provide pull-ups to the correct shared logic supply and level conversion if needed. Define adapter-controller/DUT-target roles, bus frequency, 7-bit versus shifted address, repeated-start/stop requirements and the register/data transaction. A successful probe only establishes ACK, not payload correctness.

## Reference setup

Follow the [copy-out instructions](../../docs/reference_tests.md). This topic uses [reference_common.py](../../reference_common.py), [digital/i2c/i2c_reference.py](../../digital/i2c/i2c_reference.py). Fill `SETTINGS` for the selected fixture.

| Procedure | Fixture |
| --- | --- |
| [slave ack](test_slave_ack.py) | Aardvark master and passive Beagle. Isolate one 7-bit target, qualify pull-ups and verify address-only STOP with no payload. |
| [master write read](test_master_write_read.py) | Same isolated Aardvark/Beagle fixture. Use a documented read-only register address and known bytes. Capture repeated START. |
