# I2C

Level shifters if DUT is 1.8 V.

## Building blocks

| Script | Block |
| --- | --- |
| `test_master_write_read.py.design` (reserved) | write/read → match |
| `test_slave_ack.py.design` (reserved) | probe → ACK |

## Bench hookup and prerequisites

Reserved: no implemented I2C adapter namespace. Adapter SCL -> DUT SCL, SDA -> SDA, return -> return; provide pull-ups to the correct shared logic supply and level conversion if needed. Define adapter-controller/DUT-target roles, bus frequency, 7-bit versus shifted address, repeated-start/stop requirements and the register/data transaction. A successful probe only establishes ACK, not payload correctness.
