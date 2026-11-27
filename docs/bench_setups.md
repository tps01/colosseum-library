# Recommended test setups

Use the linked suite template and topic instructions to fill instrument IDs,
limits and fixture settings. Solid arrows show physical or application paths.
Dotted arrows show runner control, configuration, or evidence. These diagrams
show live setups. See [simulation and live bench setup](bench_modes.md) before
selecting drivers.

## Power acceptance

```mermaid
flowchart LR
    Limits["Rail limits (parameters.toml)"] -.-> Runner["Colosseum runner"]
    Runner -. "VISA control" .-> PSU["PSU"]
    Runner -. "VISA read" .-> DMM["DC DMM"]
    PSU -->|"Input supply and return"| DUT["DUT"]
    DUT -->|"Rail test point and its return"| DMM
    DMM -. "Rail voltage" .-> Runner
```

The block owns the PSU output and switches it off in cleanup. Prepare the DUT
enable state and provide its allowed startup time.

[Suite template](../suites/power_acceptance.toml.example) · [Rail voltage procedure](../power/rail_voltage/)

## Dynamic power

```mermaid
flowchart LR
    Runner["Colosseum runner"] -. "Instrument control" .-> PSU["PSU"]
    Runner -.-> Load["Electronic load"]
    Runner -.-> DMM["DC DMM"]
    Runner -.-> Scope["Two-channel oscilloscope"]
    PSU -->|"Input supply and return"| DUT["DUT regulator"]
    DUT -->|"Output rail and return"| Load
    DUT -->|"Output voltage"| DMM
    DUT -->|"Rail probe"| Scope
    Load -->|"Calibrated current monitor and trigger"| Scope
    Scope -. "Paired waveform CSVs" .-> Runner
```

Each block cycles and releases its own PSU and load. The current monitor must
measure the physical load current. Deskew the rail and current channels and
configure the current monitor as the scope trigger.

[Suite template](../suites/power_dynamic.toml.example) · [Loaded-rail procedure](../power/eload/) · [Transient procedures](../power/transient/)

## Digital bring-up

```mermaid
flowchart LR
    Runner["Colosseum runner and Ethernet interface"] <-->|"Ethernet link and SSH"| DUT["Powered DUT"]
    Supply["Fixture supply"] -->|"Power and return"| DUT
    DUT -->|"DUT output and signal return"| Sense["DIO sense input"]
    Runner -. "Read input" .-> Sense
    Runner -. "Drive loopback pattern" .-> Out["Separate DIO output"]
    Out -->|"Passive loopback jumper"| In["Separate DIO input"]
    Runner -. "Read loopback" .-> In
```

The fixture owns DUT power and firmware setup. The DIO line wired to the DUT
output stays input-only. The loopback uses two other pins. The DUT-command tests
run the configured SSH release command during cleanup.

[Suite template](../suites/digital_bringup.toml.example) · [GPIO procedures](../digital/gpio/) · [Ethernet link procedure](../digital/ethernet/)

## GNSS receiver

```mermaid
flowchart LR
    RF["Antenna with sky view or authorized repeater"] -->|"GNSS RF"| DUT["Powered GNSS receiver"]
    DUT <-->|"USB or serial stream and control"| Runner["Colosseum runner"]
    Runner -.-> Evidence["Decoded and binary logs, track CSV, plots"]
```

The fixture provides usable sky signal and receiver power. Each block sets the
receiver message profile and stops its own recording. The suite measures
time-to-fix from a marked acquisition start on an already operating receiver.

[Suite template](../suites/gnss_receiver.toml.example) · [GNSS procedures](../rf/gnss_receiver/)

## Host smoke

```mermaid
flowchart LR
    subgraph PC["Runner PC"]
        Runner["Colosseum runner"] -. "Read local facts" .-> System["Memory, disk and Python"]
        Runner -. "Probe" .-> VISA["VISA backend (optional by policy)"]
    end
    Runner -.-> Evidence["Verification results"]
```

The suite reads host facts and can require a real VISA backend. Instrument
connectivity and calibration are separate fixture checks.

[Suite template](../suites/host_smoke.toml.example) · [Bench prerequisites](../host/bench_prerequisites/)

## Desktop smoke

```mermaid
flowchart LR
    subgraph Desktop["Interactive Windows desktop"]
        Runner["Colosseum runner"] -.-> FlaUI["FlaUI / UI Automation"]
        FlaUI -->|"Click and read status control"| App["Application under test"]
        App -->|"Rendered post-click view"| Capture["Screenshot capture"]
    end
    Operator["Operator or fixture"] -->|"Launch and reset before each run"| App
    Capture -.-> Compare["Visual comparison"]
    Baseline["Approved post-click baseline"] -.-> Compare
```

Both blocks use the same desktop configuration. Keep that session interactive
and preserve the post-click application state until the comparison completes.

[Suite template](../suites/gui_desktop_smoke.toml.example) · [UIA click](../gui/desktop/uia_click/) · [Screenshot comparison](../gui/desktop/screenshot_match/)
