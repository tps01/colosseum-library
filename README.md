# Colosseum Library

Reusable **copy-out test procedures and reserved designs** for Colosseum benches. This is
testware, not a `col.*` plugin: there is no installable package and no
`colosseum.plugins` entry point. Tests call first-party plugins
(`col.equipment`, `col.io`, `col.host`, `col.shared`, …) after you copy a folder
into your project and fill placeholders.

Framework docs (install, runners, parameters, reports):
https://tps01.github.io/colosseum-core/ — see **Testware library**.

## Recommended first copies

| Stub | Why start here |
| --- | --- |
| [`power/rail_voltage/`](power/rail_voltage/) | Classic measure → verify; parameter-file rail limits |
| [`digital/gpio/`](digital/gpio/) | DIO bring-up blocks |
| [`host/bench_prerequisites/`](host/bench_prerequisites/) | Plugin-light PC checks (good early smoke) |
| [`suites/power_acceptance.toml.example`](suites/power_acceptance.toml.example) | Suite composing the rail procedure with parameter-file limits |

## Why

Many benches differ in IP addresses, instrument models, and DUT wiring, but the
core checks stay the same (rail voltage, GPIO toggle, gain flatness, …). This
catalog provides rigid procedures with `FILL_IN_HERE` placeholders and optional
config TOML examples.

## How to use a test

1. Copy a test directory (for example `power/rail_voltage/`) into your project.
2. Replace every `FILL_IN_HERE` in the Python script (units are in trailing
   comments).
3. Read the topic's **Bench hookup and prerequisites** (or equivalent connection
   section), connect DUT signal/power/return paths, and establish DUT mode,
   calibration and external services. Configure instrument communication:
   - **Autoconfig** (VISA gear): leave `USE_AUTOCONFIG = True`, or call
     `col.equipment.autoconfig(export_path="config.toml")` once and copy IDs into
     the script.
   - **TOML**: copy `config.toml.example` → `config.toml`, set resources, set
     `USE_AUTOCONFIG = False`.
4. Install the plugins listed in the test docstring (same env as
   `colosseum-core`, from GitHub Release wheels).
5. Copy/fill `parameters.toml.example` → `parameters.toml` (or pass
   `--parameters`) where the procedure requires file-based limits; the rail
   example requires them. Matching fields in a parameters file override the same
   limit arguments on the call.
6. Run:

```sh
colosseum run path/to/test_rail_voltage.py
# or with an explicit config when USE_AUTOCONFIG is False:
colosseum run path/to/test_rail_voltage.py --config path/to/config.toml
# optional reports (off by default):
colosseum run path/to/test_rail_voltage.py --config path/to/config.toml --report junit
```

Unfilled `FILL_IN_HERE` raises `NameError` immediately so a half-configured copy
cannot silently measure the wrong thing.

## Layout

| Path | Purpose |
| --- | --- |
| `_template/` | Copy this when adding a new catalog test |
| `docs/target_apis.md` | Executable/reserved procedure readiness |
| `digital/` | 32 atomic blocks (GPIO, buses, clocks, ethernet, fan/PWM) |
| `rf/` | 22 atomic RF blocks (VNA, SA, pwrmeter, trace analysis) |
| `power/` | 6 atomic blocks (rail, transient, eload) |
| `host/` | Bench-PC prerequisites and telemetry |
| `gui/` | Product UI automation (`col.gui.web` / `col.gui.desktop`) |
| `suites/` | Suite TOML templates that compose building blocks |
| `tools/` | Helper scripts for Colosseum test development (e.g. release downloads) |

Executable templates use `.py`; procedures needing unavailable APIs use
`.py.design` and are not runnable. See [catalog readiness](docs/target_apis.md)
for the complete missing-capability list. There are 39 executable templates and
29 reserved procedure designs at this checkpoint. API compatibility does not
establish bench readiness.

Each **topic folder** is self-contained: shared `config.toml.example`,
`README.md` (block index), and one `test_<measure>.py` per building block (one
measurement + one verify). Copy a topic folder or chain blocks via suite TOML.

## Autoconfig vs TOML

| Layer | What changes | How to fill |
| --- | --- | --- |
| Instruments | VISA resources, models, IDs | `col.equipment.autoconfig(...)` |
| Procedure | Frequencies, pins, limits | `FILL_IN_HERE` in the Python file |
| Limit kwargs (optional) | `expected_val`, tolerances by `key=` | sibling / suite / CLI parameters TOML |

Autoconfig today discovers VISA instruments only. DIO, serial, SSH, host
profile, and DUT endpoints still need TOML or script parameters. After
autoconfig, assign instrument IDs from the log or an exported TOML
(`export_path=...`).

Scripts skip loading when config is already loaded so the same file works in a
suite that shared `setup` / `--config`.

## Suites

Copy a `suites/*.toml.example` together with the test folders it references.
Paths in suite TOML are relative to the suite file. See
[suites/README.md](suites/README.md).

## Adding a test

1. Copy `_template/` to `domain/<snake_name>/`.
2. Rename `test.py` → `test_<snake_name>.py`.
3. Fill the procedure; keep `FILL_IN_HERE` in the committed catalog.
4. Document plugins and instruments in the module docstring and domain README.

## Building-block rule

Every catalog script:

1. May include stimulus/setup commands.
2. Defines one primary acceptance quantity; supporting prerequisite measurements
   and raw trace artifacts are retained when needed for a valid verdict.
3. Verifies that quantity and any required prerequisites with explicit evidence keys.
4. Keeps `FILL_IN_HERE` in the committed catalog; wiring goes in `# SETUP:`
   comments.

Suites compose blocks. A block may retain supporting evidence; a filename is
not a reason to discard the carrier-presence checks needed to validate IM3.

## Plugin dependencies by domain

See each domain `README.md` and [docs/target_apis.md](docs/target_apis.md). Reserved `.py.design` files refer to proposed capabilities that are not
implemented. They are excluded from executable suite templates; promote them
only after the method and prerequisites are defined and implemented.

- **digital** - `colosseum-equipment`, `colosseum-shared`, `colosseum-host`,
  `colosseum-messaging`
- **rf** - `colosseum-equipment`, `colosseum-shared` (trace analysis TDD)
- **power** - `colosseum-equipment`, `colosseum-shared`
- **host** - `colosseum-host`
- **gui** - `colosseum-gui` (includes web + desktop drivers)

## Library ground rules

- The library does not need CI/CD
- The library does not need unit tests (catalog scripts are the examples)
- The library does not need versioning or gitflow, though a simple develop →
  main mechanism is fine
- Tests should be portable: autoconfig + correct physical setup should cover
  most complexity
- Scripts may use libraries outside Colosseum when necessary

## Numeric acceptance limits

Catalog blocks using `verify_field(minimum=..., maximum=...)` require
`colosseum-shared` **0.5.0 or newer** in the runner's environment. Bounds are
inclusive and reject non-finite measurements. Use `expected_val` / `tolerance`
for a target window, or `minimum` / `maximum` for limits; do not combine them.
Signed dBc upper limits remain negative values; a more negative reading passes.
Skew is bounded on both sides of zero. Limits are in the measurement's units.

Transient and fresh power-sensor capture procedures require Equipment **0.5.0+**.
Copy topic folders with their companion helpers (`transient_response.py` or
`two_tone.py`) where present; the helpers are local testware, not plugins.

## Bench modes and lifecycle

Read [simulation to live setup](docs/bench_modes.md) before interpreting results.
Most configs deliberately default to simulation; changing an address does not
select a live driver. Each block states whether it owns stimulus or requires
externally prepared DUT/fixture state. Owned outputs are released in `finally`;
VNA RF output remains explicitly fixture-owned because no public disable API is
available. See topic prerequisites and [suite state contracts](suites/README.md).

The 29 reserved slots have [precise measurement contracts](docs/measurement_contracts.md),
with the old speculative implementations removed. They still require supported
acquisition/transport implementations and qualification before promotion.

The historical `scripts/scaffold_catalog.py` was retired because importing or
running it overwrote corrected procedures with obsolete generated code. Add or
edit blocks directly from `_template/`; there is no catalog regeneration step.
