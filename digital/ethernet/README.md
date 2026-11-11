# Ethernet

RJ45 to DUT; dut_ip and local_iface in FILL_IN_HERE.

## Building blocks

| Script | Block |
| --- | --- |
| `test_link_up.py` | operstate → UP |
| `test_ping_reachability.py` | ping loss → max |
| `test_throughput_mbps.py` | iperf Mbps → minimum |
| `test_eye_height_mv.py.design` (reserved) | eye height → minimum |
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

Plugins: Host for the runner-side link check; Messaging and Shared/custom verification for SSH traffic results. Label runner NIC, SSH traffic peer, DUT NIC/address and the connecting cable separately. Prepare address/routing and Linux traffic tools; the traffic-result contracts above apply. Eye/BER fixtures and the DUT PHY test mode are separate from a successful software link check; the eye-height procedure is reserved.
