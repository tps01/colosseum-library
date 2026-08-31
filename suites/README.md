# Suite templates

Copy a `*.toml.example` to your project (drop the `.example` suffix) **together
with** the test folders it lists. Suite paths are relative to the suite file.

## Run

```sh
# Config already loaded by suite CLI, or by each test's _load_bench / autoconfig:
colosseum run-suite power_acceptance.toml --config config.toml
colosseum run-suite rf_passband.toml --config config.toml
```

When every test uses `USE_AUTOCONFIG = True` and VISA gear only, `--config` may
be omitted if the first script calls autoconfig. Prefer an explicit config TOML
for mixed suites (DIO + host + instruments).

## Templates

| File | Blocks composed |
| --- | --- |
| `host_smoke.toml.example` | `host/bench_prerequisites` |
| `power_acceptance.toml.example` | `power/rail_voltage` |
| `power_dynamic.toml.example` | eload + transient (4 blocks) |
| `digital_gpio_bench.toml.example` | GPIO output + rise time |
| `digital_bringup.toml.example` | GPIO + loopback + ethernet link |
| `rf_passband.toml.example` | S21 max, S11 max, gain flatness |
| `rf_linearity.toml.example` | P1dB, IM3, OIP3 |
| `rf_amplifier.toml.example` | broader RF acceptance (6 blocks) |

Optional `fail_fast = true` stops remaining tests after a required failure;
teardown still runs.
