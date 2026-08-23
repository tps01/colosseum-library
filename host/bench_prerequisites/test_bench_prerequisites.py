"""Bench-PC prerequisites: memory, disk, Python, optional VISA.

Required plugins:
  - colosseum-core
  - colosseum-host

Instruments:
  - None (host APIs only). Optional VISA backend check via ``col.host.bench``.

Run (after copy-out and filling FILL_IN_HERE)::

    colosseum run test_bench_prerequisites.py --config bench.toml
"""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# --- bench wiring ---
USE_AUTOCONFIG = False  # Host checks do not use VISA autoconfig

# --- procedure (replace every FILL_IN_HERE) ---
min_memory_mb = FILL_IN_HERE  # MB; e.g. 256.0
min_disk_gb = FILL_IN_HERE  # GB; e.g. 1.0
python_version_prefix = FILL_IN_HERE  # str; e.g. "3.11"
require_visa = FILL_IN_HERE  # bool; True fails the run if VISA is missing


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("bench.toml")))


def main() -> None:
    _load_bench()

    col.host.system.measure_memory_available_mb(key="mem_mb")
    col.host.system.verify_memory_available_mb(key="mem_mb", minimum=min_memory_mb)
    col.host.system.measure_disk_free_gb(key="disk_gb")
    col.host.system.verify_disk_free_gb(key="disk_gb", minimum=min_disk_gb)
    col.host.system.measure_python_version(key="py")
    col.host.system.verify_python_version(key="py", version_prefix=python_version_prefix)
    col.host.bench.measure_visa_backend(key="visa")
    col.host.bench.verify_visa_available(key="visa", allow_sim=True, optional=not require_visa)


if __name__ == "__main__":
    main()
    col.endex()
