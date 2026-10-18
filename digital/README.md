# Digital

Atomic bring-up blocks for GPIO, buses, clocks, ethernet, and fan/PWM/tach.

**Start here:** [gpio/](gpio/) (see also `suites/digital_gpio_bench.toml.design`).

Each topic folder has a shared `config.toml.example`, `README.md` (block index),
and
one executable `test_<measure>.py` per implemented block, plus reserved designs.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-equipment` | DIO and supported instrument acquisition; other buses remain reserved |
| `colosseum-shared` | Numeric and Boolean evidence acceptance, waits |
| `colosseum-host` | `col.host.net` (ethernet link) |
| `colosseum-messaging` | SSH fan commands, ping/iperf parse |

See [docs/target_apis.md](../docs/target_apis.md) for TDD specifications.

## Catalog (32 building blocks)

| Topic | Blocks | Folder |
| --- | --- | --- |
| 1-Wire | 4 | [onewire/](onewire/) |
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

Rows labeled **reserved** refer to `.py.design` procedure proposals, not runnable
tests. See [catalog readiness](../docs/target_apis.md) before copying a block.
