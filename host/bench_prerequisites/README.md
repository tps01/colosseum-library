# Bench prerequisites

**Start here** for host: check memory, disk, Python version, and optionally VISA
on the bench PC.

## Plugins

- `colosseum-core`
- `colosseum-host`

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `min_memory_mb` | Minimum available memory (MB) |
| `min_disk_gb` | Minimum free disk (GB) |
| `python_version_prefix` | Required Python prefix (e.g. `"3.11"`) |
| `require_visa` | If true, fail when VISA is unavailable |

## Run

```sh
# Copy config.toml.example → config.toml if you need [host.profile];
# else a minimal file is fine
colosseum run test_bench_prerequisites.py --config config.toml
```

## Bench hookup and prerequisites

Plugins: Host (and core), no DUT or equipment connection. These are facts about the computer running Colosseum: free memory, free space on the API-selected volume, Python version and VISA backend availability. Confirm that volume is where run artifacts will be written; change the disk path when another volume is the actual requirement. A VISA backend check does not verify a connected, calibrated instrument, and `require_visa=True` rejects a simulated backend as well as a missing one. When false, VISA is optional and a simulated backend is permitted. Neither outcome validates selected equipment drivers or physical readiness.

Use Host **0.4.3+** for reliable PyVISA-sim identification: its native display
string can omit `@sim`, so earlier Host versions can misclassify that backend.
