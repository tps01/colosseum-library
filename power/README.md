# Power

Atomic PSU, DMM, eload, and transient-response building blocks.

**Start here:** [rail_voltage/](rail_voltage/) (required parameter-file limits).

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-equipment` | PSU, DMM, eload and scope acquisition |
| `colosseum-shared` | Numeric acceptance, bounds and settling waits |

See [docs/target_apis.md](../docs/target_apis.md) for TDD specifications.

## Catalog (6 building blocks)

| Topic | Blocks | Folder |
| --- | --- | --- |
| Rail voltage (DMM) | 1 | [rail_voltage/](rail_voltage/) |
| Transient response | 3 | [transient/](transient/) |
| Electronic load | 2 | [eload/](eload/) |

### Suite examples

- [suites/power_acceptance.toml.example](../suites/power_acceptance.toml.example)
  - steady rail check
- [suites/power_dynamic.toml.example](../suites/power_dynamic.toml.example) -
  load step + transient

Rows labeled **reserved** refer to `.py.design` procedure proposals, not runnable
tests. See [catalog readiness](../docs/target_apis.md) before copying a block.
