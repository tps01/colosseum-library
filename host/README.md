# Host

Bench-PC prerequisites and local telemetry (`col.host.*`).

## Plugins

| Plugin | Used for |
|--------|----------|
| `colosseum-host` | System, bench, net, sample APIs |

## Catalog

| Test | Status | Notes |
|------|--------|-------|
| [bench_prerequisites](bench_prerequisites/) | Exemplar | Memory, disk, Python, optional VISA availability |

Host tests usually set `USE_AUTOCONFIG = False`. A minimal or empty bench TOML
is enough when no `[host.profile]` thresholds are required; limits live in
`FILL_IN_HERE`.
