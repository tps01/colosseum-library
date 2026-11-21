# Ethernet

RJ45 to DUT; dut_ip and local_iface in FILL_IN_HERE.

## Building blocks

| Script | Block |
| --- | --- |
| `test_link_up.py` | operstate → UP |
| `test_ping_reachability.py` | ping loss → max |
| `test_throughput_mbps.py` | iperf Mbps → minimum |
| [`test_eye_mask.py`](test_eye_mask.py) | Saved differential captures checked against a supplied mask |
| `test_ber.py` | BER → maximum |

## Traffic prerequisites and result contracts

The SSH endpoint is the traffic-generating peer, and `dut_ip` is the DUT traffic
address. Connect that peer's NIC to the DUT and configure addressing/routing.
These commands require a Linux SSH peer with iputils `ping` and `iperf3` installed.
Start `iperf3 -s` on the DUT before throughput tests. Throughput is forward TCP,
peer to DUT, using the receiver aggregate in iperf3 JSON, in decimal Mbit/s.
`iperf_duration_s` and `ping_count` are positive integers; `max_loss` is percent.

The DUT-specific BER command must complete within 30 seconds, exit 0, and print
one JSON object such as `{"ber": 1e-9}`. BER and `ber_max` are fractions in 0..1.
The command owns PHY test setup, duration and bit counting; adapt it to the DUT.
Raw stdout/stderr and exit code are preserved as `ssh.exec` evidence. Failed
commands, missing fields and malformed results cannot pass these checks.

`test_link_up.py` checks `local_iface` on the Colosseum runner. It does not query
a remote DUT interface; use a DUT command when that is the requirement.

## Bench hookup and prerequisites

Use Host for the runner-side link check, Messaging for SSH traffic, and Shared
for acceptance. Prepare the PHY test mode and measurement fixture separately
from the traffic setup.

## Oscilloscope options for PHY waveform capture

These `col.equipment.oscope` models support analog acquisition and waveform
export for offline analysis. Select the scope bandwidth, differential probe,
and breakout fixture for the exact PHY and test point.

| Instrument | Equipment model |
| --- | --- |
| Rohde & Schwarz RTP164 | `rohde-rtp164` |
| Tektronix MSO54B, MSO64B | `tektronix-mso54b`, `tektronix-mso64b` (Equipment 0.24+) |
| Keysight MXR104B, MXR404B | `keysight-mxr104b`, `keysight-mxr404b` (Equipment 0.24+) |

These profiles export analog voltage samples. R&S RTO6 and Teledyne LeCroy
WavePro HD can supply CSVs when their exports are converted to the format below.

## Offline eye mask reference

Copy `test_eye_mask.py` with `eye_reference.py`, preserving their paths
relative to the project root. Fill the script's `SETTINGS`. With the project
root on `PYTHONPATH`, run `colosseum run digital/ethernet/test_eye_mask.py`.
The procedure uses saved files and needs no instrument rows.

Use [eye_reference.py](eye_reference.py) to apply a supplied Colosseum
time-domain mask to saved scope CSVs with `time_s` and `voltage_v` columns.
Each capture is a differential CSV path or a pair of simultaneous, deskewed
single-ended CSV paths in positive, negative order. The helper subtracts the
legs on their shared grid and evaluates each differential capture separately.

```python
from digital.ethernet.eye_reference import verify_eye_traces

result = verify_eye_traces(
    captures=["differential.csv", ("positive.csv", "negative.csv")],
    mask_path="eye_mask.json",
    period_s=FILL_IN_HERE,
    origin_s=FILL_IN_HERE,
    max_sample_spacing_s=FILL_IN_HERE,
)
```

Use a trigger-relative origin and a known fold period for a repeating pattern.
Express the mask's time bounds within the resulting `[0, period_s)` window.
Omit `period_s` for CSVs already aligned to the mask axis. The helper uses
Equipment's rectangular mask regions. The reference records per-capture
evidence and uses Shared to verify the combined verdict. Supply the
mask, fit parameters, and capture coverage for your fixture. The result
reports mask pass/fail for the sampled data.
