# Agent guide

Read `RULES.md` before changing dependencies. Do not commit, push, merge, or tag unless
the user explicitly requests it.

## Scope

`colosseum-library` is **reusable testware**, not a Colosseum plugin:

- copy-out Python test scripts grouped by domain (`digital/`, `rf/`, `power/`, `host/`, `gui/`)
- optional per-test `bench.toml.example` files
- suite TOML templates under `suites/`
- `_template/` as the pattern for new tests

It must **not**:

- register a `colosseum.plugins` entry point or a `col.library.*` namespace
- invent instrument APIs that belong in plugins
- commit lab-specific numbers (keep `FILL_IN_HERE` in the catalog)

## Change discipline

- Keep changes focused and reviewable.
- New tests: copy `_template/` into `domain/<snake_name>/`.
- Prefer existing `col.*` plugin APIs (`equipment`, `io`, `host`, `shared`, `messaging`).
- Update the domain README when adding or reserving a test slot.
- Do not add an installable `pyproject.toml` unless tooling-only config is explicitly requested.

## Public behavior

- Users copy a test folder (or suite) into their project, replace every `FILL_IN_HERE`,
  wire instruments via autoconfig or `bench.toml`, and run with `colosseum run` /
  `colosseum run-suite`.
- Scripts use `def main():` and `col.endex()` under `__main__`.
- One `col.*` call per line with keyword arguments.
