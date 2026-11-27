"""Verify the expected ordered IDCODEs using the configured JTAG tools."""
import colosseum as col

JTAG_ID = FILL_IN_HERE
EXPECTED_IDCODES = FILL_IN_HERE  # list of hex strings, in tool discovery order


@col.measurement
def measure_idcodes(*, key):
    inventory = col.equipment.jtag.list_devices(jtag_id=JTAG_ID, key="device_inventory")
    return [int(device["idcode"], 16) for device in inventory["devices"]]


def main():
    measure_idcodes(key="chain_idcodes")
    col.shared.verify.verify_field(key="chain_idcodes", expected_val=[int(x, 16) for x in EXPECTED_IDCODES])


if __name__ == "__main__":
    main()
    col.endex()
