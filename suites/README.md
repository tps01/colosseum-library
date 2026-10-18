# Suite templates

Copy a `*.toml.example` to your project (drop the `.example` suffix) **together
with** the test folders it lists. Suite paths are relative to the suite file.

## Run

```sh
# Config already loaded by suite CLI, or by each test's _load_bench / autoconfig:
colosseum run-suite power_acceptance.toml --config config.toml
colosseum run-suite host_smoke.toml --config config.toml
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
| `digital_gpio_bench.toml.design` | GPIO output + rise time |
| `digital_bringup.toml.example` | GPIO + loopback + ethernet link |
| `rf_passband.toml.design` | S21 max, S11 max, gain flatness |
| `rf_linearity.toml.design` | P1dB, IM3, OIP3 |
| `rf_amplifier.toml.design` | broader RF acceptance (6 blocks) |
| `gui_desktop_smoke.toml.example` | desktop UIA click + screenshot match |

For a fuller Windows teaching suite (multi-desktop, `args=`, hotkey, file wait),
use `colosseum-gui/examples/desktop_suite/` (requires gui 0.2.3+ and shared 0.3.5+).

Optional `fail_fast = true` stops remaining tests after a required failure;
teardown still runs.

A test entry may set `parameters = "relative/path.toml"` (resolved from the suite
file). CLI `--parameters` still wins for the whole process. See
`power_acceptance.toml.example` for a rail check that points at a limits file.
After copy-out, rename `parameters.toml.example` → `parameters.toml` (or point
`parameters=` at your filled file).

## Reserved suites

Only `.toml.example` files are runnable suite templates. `.toml.design` files
retain the proposed compositions for review and must not be passed to run-suite.
Their `.py.design` dependencies are not executable. Fill-in values cannot supply
missing instrument capabilities. See [readiness](../docs/target_apis.md).

## Fixture and state contracts

`power_dynamic.toml.example` uses one fixed input-supply/output-load fixture with
a DMM at the DUT output and simultaneous rail/current scope channels. Copy both
the eload and transient topic folders including `transient_response.py`, merge
the bench rows (the eload example contains PSU/load/DMM/scope), and fill identical
instrument IDs and compatible supply/load settings across blocks. Each block
starts a new power cycle and cleans up its owned source/load; no earlier test
provides initial state for a later one. The DUT must support those cycles.

`digital_bringup` requires a separate fixture loopback pair that cannot contend
with DUT outputs, DIO sense wiring for the DUT-command tests, and an Ethernet
link to the specified runner interface. DUT power/firmware/SSH readiness are
external prerequisites. GPIO blocks release their drives between tests.

`gui_desktop_smoke` uses one FlaUI-capable desktop for both blocks, starts from
an externally reset application, then verifies the same post-click status/view.
Fill the separate status locator and approved post-action screenshot. Re-run
only after restoring the initial application state. Sim cannot qualify this flow.

Empty setup/teardown arrays are intentional only where the blocks own their
cleanup or the stated state is externally prepared. They do not launch apps,
switch RF routes, or establish stimulus. Reserved RF/GPIO compositions state
their missing workflow in the sketch header and remain non-executable. Ordinary
`finally` cleanup is attempted on Python errors; a killed process, lost connection
or instrument fault still requires the fixture's independent protection.
