# Ethernet

RJ45 to DUT; dut_ip and dut_iface in FILL_IN_HERE.

## Building blocks

| Script | Block |
| --- | --- |
| `test_link_up.py` | operstate → UP |
| `test_ping_reachability.py` | ping loss → max |
| `test_throughput_mbps.py` | iperf Mbps → minimum |
| `test_eye_height_mv.py` | eye height → minimum |
| `test_ber.py` | BER → maximum |
