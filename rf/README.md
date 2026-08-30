# RF

Atomic RF path and amplifier building blocks. Instrument APIs live in
`colosseum-equipment`; trace analysis and derived metrics in `col.shared.signal`
(TDD).

Each topic folder shares `config.toml.example` + `README.md`; every script is one
measurement and one verify.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-equipment` | `vsg`, `speca`, `vna`, `pwrmeter`, `fs740` (TDD) |
| `colosseum-shared` | Savitzky–... |

See [docs/target_apis.md](../docs/target_apis.md) for TDD specifications and the
`speca.measure_bw` / Savitzky–Golay alignment note.

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

- [suites/rf_passband.toml.example](../suites/rf_passband.toml.example) — S21,
  S11, gain flatness
- [suites/rf_linearity.toml.example](../suites/rf_linearity.toml.example) —
  P1dB, IM3, OIP3
- [suites/rf_amplifier.toml.example](../suites/rf_amplifier.toml.example) —
  broader RF acceptance
