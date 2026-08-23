# Bench prerequisites

Check memory, disk, Python version, and optionally VISA on the bench PC.

## Plugins

- `colosseum-core`
- `colosseum-host`

## FILL_IN_HERE

| Name | Meaning |
|------|---------|
| `min_memory_mb` | Minimum available memory (MB) |
| `min_disk_gb` | Minimum free disk (GB) |
| `python_version_prefix` | Required Python prefix (e.g. `"3.11"`) |
| `require_visa` | If true, fail when VISA is unavailable |

## Run

```sh
# Copy bench.toml.example → bench.toml if you need [host.profile]; else a minimal file is fine
colosseum run test_bench_prerequisites.py --config bench.toml
```
