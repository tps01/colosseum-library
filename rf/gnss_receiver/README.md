# GNSS receiver

Live serial/USB GNSS acceptance blocks. Requires usable sky view or an indoor
repeater. Instrument APIs live in `colosseum-equipment` (`col.equipment.gnss`).

## Building blocks

| Script | Primary quantity |
| --- | --- |
| `test_max_cn0_dbhz.py` | max C/N0 (dB-Hz) lower bound |
| `test_satellites_visible.py` | satellites visible lower bound |
| `test_ttff_s.py` | TTFF after `mark_acquisition_start` upper bound |
| `test_hdop.py` | HDOP upper bound (with position / plot evidence) |

Suite template: [`suites/gnss_receiver.toml.example`](../../suites/gnss_receiver.toml.example)
(CN0 → sats → TTFF → HDOP).

## Bench wiring

1. Copy this folder (or run from the library tree after fill-in).
2. Copy `config.toml.example` → `config.toml`.
3. Set `port` (e.g. `COM5` for a u-blox M9 USB serial adapter). Leave **`model`
   omitted** so open-time `MON-VER` probing can select `ublox-m9`.
4. Keep `USE_AUTOCONFIG = False` unless you intentionally use COM autoconfig.
5. Replace every `FILL_IN_HERE` in the scripts you will run.

Suggested first-fill values (tune to the antenna / environment):

| Field | Starter |
| --- | --- |
| `gnss_id` | `1` |
| `soak_s` | `20` |
| `min_cn0_dbhz` | `20` |
| `min_sats_visible` | `4` |
| `fix_timeout_s` / `max_ttff_s` | `120` |
| `max_hdop` | `5` |

Default baud in the example config is **9600**. If the receiver was moved to
another baud, edit `config.toml` to match or probing and stream will fail.

`test_ttff_s.py` does **not** cold-start the receiver; it marks acquisition T0
then waits for fix (warm/hot). `test_hdop.py` exports a config subset via
`save_config` before logging.

## Run

Single blocks:

```sh
colosseum run test_max_cn0_dbhz.py --config config.toml
colosseum run test_satellites_visible.py --config config.toml
colosseum run test_ttff_s.py --config config.toml
colosseum run test_hdop.py --config config.toml
```

Full prove-out (after copying the suite template beside the topic paths it
references, or adjusting paths):

```sh
colosseum run-suite gnss_receiver.toml --config rf/gnss_receiver/config.toml
```

## What to paste back after a prove-out

- Suite or block run summary (PASS/FAIL) and any traceback
- Log lines showing model probe / resolution (`ublox-m9` vs `generic` fallback)
- Run output artifacts under `gnss/`: `*_wire.ubx`, decoded `.nmea`,
  `*_track.csv`, plots, `baseline.txt`
- Which block failed and whether it was COM open, soak/stream, `wait_for_fix`,
  or a verify limit
