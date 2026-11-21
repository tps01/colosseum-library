"""Check device-scoped IR/DR captures against fixture expectations."""
import colosseum as col

JTAG_ID = FILL_IN_HERE
STEPS = FILL_IN_HERE  # IDLE, IR and DR steps for the selected device
EXPECTED_SCANS = FILL_IN_HERE  # list of register, bits and uppercase padded tdo rows


@col.measurement
def measure_scan_match(*, key):
    scan = col.equipment.jtag.scan(jtag_id=JTAG_ID, scope="device", steps=STEPS, key="device_scan")
    return scan["scans"] == EXPECTED_SCANS


def main():
    measure_scan_match(key="device_scan_matches")
    col.shared.verify.verify_field(key="device_scan_matches", expected_val=True)


if __name__ == "__main__":
    main()
    col.endex()
