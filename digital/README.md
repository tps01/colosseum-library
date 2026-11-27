# Digital

Atomic bring-up blocks for GPIO, buses, clocks, ethernet, and fan/PWM/tach.

**Start here:** [gpio/](gpio/) (see also `suites/digital_gpio_bench.toml.design`).

Each topic has a block index and one `test_<measure>.py` per block.
Bench-driven blocks include an example configuration.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-equipment` | DIO, I?C and SPI controller operations, 1-Wire, and instrument acquisition |
| `colosseum-shared` | Numeric and Boolean evidence acceptance, waits |
| `colosseum-host` | `col.host.net` (ethernet link) |
| `colosseum-messaging` | SSH fan commands, ping/iperf parse |

See the [measurement contracts](../docs/measurement_contracts.md) for evidence requirements.

## Catalog (31 building blocks)

| Topic | Blocks | Folder |
| --- | --- | --- |
| 1-Wire | 3 | [onewire/](onewire/) |
| Clocks | 4 | [clocks/](clocks/) |
| Ethernet | 5 | [ethernet/](ethernet/) |
| Fan / PWM / tach | 4 | [tachometer_pwm/](tachometer_pwm/) |
| GPIO | 9 | [gpio/](gpio/) |
| I2C | 2 | [i2c/](i2c/) |
| SPI | 2 | [spi/](spi/) |
| JTAG | 2 | [jtag/](jtag/) |

### Suite examples

- [suites/digital_gpio_bench.toml.design](../suites/digital_gpio_bench.toml.design)
  - GPIO output and timing
- [suites/digital_bringup.toml.example](../suites/digital_bringup.toml.example)
  - broader digital smoke
