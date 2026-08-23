# Digital

Atomic bring-up blocks for GPIO, buses, clocks, ethernet, and fan/PWM/tach.

Each topic folder has a shared `bench.toml.example`, `README.md` (block index), and
one `test_<measure>.py` per building block (one measurement + one verify).

## Plugins

| Plugin | Used for |
|--------|----------|
| `colosseum-equipment` | `col.io.dio`, `col.io.i2c/spi/jtag/onewire` (TDD), `col.equipment.oscope`, `freqcounter` |
| `colosseum-shared` | `col.shared.verify`, `col.shared.signal`, `col.shared.regex` |
| `colosseum-host` | `col.host.net` (ethernet link) |
| `colosseum-messaging` | SSH fan commands, ping/iperf parse |

See [docs/target_apis.md](../docs/target_apis.md) for TDD contracts.

## Catalog (32 building blocks)

| Topic | Blocks | Folder |
|-------|--------|--------|
| 1-Wire | 4 | [onewire/](onewire/) |
| Clocks | 4 | [clocks/](clocks/) |
| Ethernet | 5 | [ethernet/](ethernet/) |
| Fan / PWM / tach | 4 | [tachometer_pwm/](tachometer_pwm/) |
| GPIO | 9 | [gpio/](gpio/) |
| I2C | 2 | [i2c/](i2c/) |
| SPI | 2 | [spi/](spi/) |
| JTAG | 2 | [jtag/](jtag/) |

### Suite examples

- [suites/digital_gpio_bench.toml.example](../suites/digital_gpio_bench.toml.example) — GPIO output and timing
- [suites/digital_bringup.toml.example](../suites/digital_bringup.toml.example) — broader digital smoke
