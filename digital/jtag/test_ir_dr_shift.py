"""Verify chain-wide captured TDO for a board-defined IR/DR sequence."""
import colosseum as col

JTAG_ID = FILL_IN_HERE
STEPS = FILL_IN_HERE  # [{"state": "RESET"}, {"register": "IR", "bits": ..., "tdi": "..."}, ...]
EXPECTED_SCANS = FILL_IN_HERE  # [{"register": "IR", "bits": ..., "tdo": "..."}]; uppercase padded hex


@col.measurement
def measure_scan_match(*, key):
    scan = col.equipment.jtag.scan(jtag_id=JTAG_ID, steps=STEPS, key="chain_scan")
    return scan["scans"] == EXPECTED_SCANS


def main():
    measure_scan_match(key="scan_matches")
    col.shared.verify.verify_field(key="scan_matches", expected_val=True)


if __name__ == "__main__":
    main()
    col.endex()
