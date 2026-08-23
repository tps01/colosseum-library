# New library test template

Copy this folder to `../<domain>/<snake_name>/`, rename `test.py` to
`test_<snake_name>.py`, and replace the placeholder procedure.

Keep every `FILL_IN_HERE` in the **catalog** copy. Lab values belong only in the
user's project copy.

## Checklist

1. Module docstring: purpose, required plugins, instruments, how to run.
2. Top-of-file procedure block with `FILL_IN_HERE` and unit comments.
3. `_load_bench()` that respects `col.config.is_loaded()`, `USE_AUTOCONFIG`, and
   a sibling `bench.toml`.
4. `def main():` with one `col.*` call per line (keyword args).
5. `if __name__ == "__main__": main(); col.endex()`.
6. Optional `bench.toml.example` using real plugin section names only
   (`[[equipment.*]]`, `[[io.dio]]`, … — never `[library.*]`).
7. Short `README.md` in the test folder listing FILL_IN_HERE keys and plugins.
