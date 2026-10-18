# RF

Atomic RF path and amplifier building blocks. Instrument APIs live in
`colosseum-equipment`. Implemented derived metrics use local copy-out helpers;
other methods remain [reserved contracts](../docs/measurement_contracts.md).

Each topic folder shares `config.toml.example` + `README.md`; each executable script has one primary quantity with supporting evidence as needed.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-equipment` | `vsg`, `speca`, `vna`, `pwrmeter`, `fs740` (TDD) |
| `colosseum-shared` | Numeric acceptance, bounds and settling waits |

See [catalog readiness](../docs/target_apis.md) for unavailable capabilities and
reserved procedure designs.

## Catalog (22 building blocks)

| Topic | Blocks | Folder |
| --- | --- | --- |
| Allan deviation | 1 | [allan_deviation/](allan_deviation/) |
| Frequency / OBW | 3 | [frequency/](frequency/) |
| Gain flatness | 1 | [gain_flatness/](gain_flatness/) |
| Harmonics | 3 | [harmonics/](harmonics/) |
| Mask margin | 1 | [masking/](masking/) |
| IP2 / IP3 / OIP3 | 4 | [ip2_ip3/](ip2_ip3/) |
| P1dB | 1 | [p1db/](p1db/) |
| Insertion loss (S21) | 2 | [insertion_loss/](insertion_loss/) |
| Return loss (S11) | 2 | [return_loss/](return_loss/) |
| Spurs | 1 | [spurs/](spurs/) |
| Power meter | 3 | [power_meter/](power_meter/) |

### Suite examples

- [suites/rf_passband.toml.design](../suites/rf_passband.toml.design) - S21,
  S11, gain flatness
- [suites/rf_linearity.toml.design](../suites/rf_linearity.toml.design) -
  P1dB, IM3, OIP3
- [suites/rf_amplifier.toml.design](../suites/rf_amplifier.toml.design) -
  broader RF acceptance

Rows labeled **reserved** refer to `.py.design` procedure proposals, not runnable
tests. See [catalog readiness](../docs/target_apis.md) before copying a block.
