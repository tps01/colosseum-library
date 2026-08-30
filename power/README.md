# Power

Atomic PSU, DMM, eload, and transient-response building blocks.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-equipment` | `col.equipment.psu`, `dmm`, `eload` (...)` |
| `colosseum-shared` | `col.shared.signal.ramp_eload_current` (...)` |

See [docs/target_apis.md](../docs/target_apis.md) for TDD specifications.

## Catalog (6 building blocks)

| Topic | Blocks | Folder |
| --- | --- | --- |
| Rail voltage (DMM) | 1 | [rail_voltage/](rail_voltage/) |
| Transient response | 3 | [transient/](transient/) |
| Electronic load | 2 | [eload/](eload/) |

### Suite examples

- [suites/power_acceptance.toml.example](../suites/power_acceptance.toml.example)
  — steady rail check
- [suites/power_dynamic.toml.example](../suites/power_dynamic.toml.example) —
  load step + transient
