# Colosseum Library

Reusable **copy-out** test scripts for Colosseum benches. This is testware, not
a
`col.*` plugin: there is no installable package and no `colosseum.plugins` entry
point. Tests call first-party plugins (`col.equipment`, `col.io`, `col.host`,
`col.shared`, …) after you copy a folder into your project and fill parameters.

## Why

Many benches differ in IP addresses, instrument models, and DUT wiring, but the
core checks stay the same (rail voltage, GPIO toggle, gain flatness, …). This
catalog provides rigid procedures with `FILL_IN_HERE` placeholders and optional
config TOML examples.

## How to use a test

1. Copy a test directory (for example `power/rail_voltage/`) into your project.
2. Replace every `FILL_IN_HERE` in the Python script (units are in trailing
  comments).
3. Wire instruments:
   - **Autoconfig** (VISA gear): leave `USE_AUTOCONFIG = True`, or call
     `col.equipment.autoconfig(export_path="config.toml")` once and copy IDs into
     the script.
   - **TOML**: copy `config.toml.example` → `config.toml`, set resources, set
     `USE_AUTOCONFIG = False`.
4. Install the plugins listed in the test docstring (same env as
  `colosseum-core`).
5. Run:

```sh
colosseum run path/to/test_rail_voltage.py
# or with an explicit config when USE_AUTOCONFIG is False:
colosseum run path/to/test_rail_voltage.py --config path/to/config.toml
```

Unfilled `FILL_IN_HERE` raises `NameError` immediately so a half-configured copy
cannot silently measure the wrong thing.

## Layout

| Path | Purpose |
| --- | --- |
| `_template/` | Copy this when adding a new catalog test |
| `docs/target_apis.md` | TDD specifications referenced by catalog scripts |
| `digital/` | 32 atomic blocks (GPIO, buses, clocks, ethernet, fan/PWM) |
| `rf/` | 22 atomic RF blocks (VNA, SA, pwrmeter, trace analysis) |
| `power/` | 6 atomic blocks (rail, transient, eload) |
| `host/` | Bench-PC prerequisites and telemetry |
| `gui/` | Product UI automation (`col.gui.web` / `col.gui.desktop`) |
| `suites/` | Suite TOML templates that compose building blocks |

Each **topic folder** is self-contained: shared `config.toml.example`,
`README.md`
(block index), and one `test_<measure>.py` per building block (one measurement +
one verify). Copy a topic folder or chain blocks via suite TOML.

## Autoconfig vs TOML

| Layer | What changes | How to fill |
| --- | --- | --- |
| Instruments | VISA resources, models, IDs | `col.equipment.autoconfig(...)` |
| Procedure | Frequenci... | `FILL_IN_HERE` in the Python file |

Autoconfig today discovers VISA instruments only. DIO, serial, SSH, host
profile,
and DUT endpoints still need TOML or script parameters. After autoconfig, assign
instrument IDs from the log or an exported TOML (`export_path=...`).

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
2. Emits **exactly one** `@measurement` row (one `key`).
3. Ends with **exactly one** verify for that quantity.
4. Keeps `FILL_IN_HERE` in the committed catalog; wiring goes in `# SETUP:`
  comments.

Suites compose blocks — they do not combine multiple measurements in one script.

## Plugin dependencies by domain

See each domain `README.md` and [docs/target_apis.md](docs/target_apis.md). Many
scripts call TDD APIs not yet implemented in plugins; equipment rises to meet
them.

- **digital** — `colosseum-equipment`, `colosseum-shared`, `colosseum-host`,
  `colosseum-messaging`
- **rf** — `colosseum-equipment`, `colosseum-shared` (trace analysis TDD)
- **power** — `colosseum-equipment`, `colosseum-shared`
- **host** — `colosseum-host`
- **gui** — `colosseum-gui` (`pip install colosseum-gui`; includes web + desktop
  drivers)

## Library Ground Rules

- The library does not need CI/CD
- The library does not need test scripts/ unit tests (though tests from the
  library are valid as e2e tests themselves)
- The library does not need versioning or gitflow, though a simple develop ->
  main mechanism is fine.
- Tests in the library should be portable. An inexperienced user should have to
  do minimal coding to get a test working. (i.e. autoconfig + a correct physical
  hardware setup should handle most complexity)
- Library tests may use libraries outside colosseum to accomplish certain tasks,
  when necessary. Colosseum is built on python for this reason- one framework
  cannot possibly cover every use-case or test flow.
