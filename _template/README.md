# New library test template

Copy this folder to `../<domain>/<snake_name>/`, rename `test.py` to
`test_<snake_name>.py`, and replace the placeholder procedure.

Keep every `FILL_IN_HERE` in the **catalog** copy. Lab values belong only in the
user's project copy.

## Checklist

1. Module docstring: purpose, required plugins, instruments, how to run.
2. Top-of-file procedure block with `FILL_IN_HERE` and unit comments.
3. `_load_bench()` that respects `col.config.is_loaded()`, `USE_AUTOCONFIG`, and
   a sibling `config.toml`.
4. `def main():` with one `col.*` call per line (keyword args).
5. `if __name__ == "__main__": main(); col.endex()`.
6. Optional `config.toml.example` using real plugin section names only
   (`[[equipment.*]]`, `[io.dio]`, … - never `[library.*]`).
7. Optional `parameters.toml.example` for limit kwargs by evidence `key=`
   (sibling `parameters.toml`, suite entry `parameters=`, or CLI `--parameters`).
8. Short `README.md` in the test folder listing FILL_IN_HERE keys and plugins.
9. Document optional `--report wats` / `--report junit` in the run section when
   useful; do not invent library-owned report switches.

## Procedure contract before copy-out

Include a terminal/signal connection map (stimulus -> DUT -> receiver, plus
returns/references), required plugins and supported model capabilities, DUT
power/firmware/control mode and external services. Define calibration/reference
planes, units/statistic/acceptance, acquisition ordering and output ownership.
Separate fixture self-tests from DUT behavior and identify evidence that rejects
missing stimulus. Name any required companion files and parameter-file limits.
