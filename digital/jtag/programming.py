"""Select one operation on the copied file and fill its board-specific settings."""
from pathlib import Path

import colosseum as col

JTAG_ID = FILL_IN_HERE
OPERATION = FILL_IN_HERE  # "device", "flash", "verify", "boot", or "tcl"
SETTINGS = FILL_IN_HERE  # image/flash_part/fsbl/initialization_pdi, or reset/check_boot callbacks


def main():
    if OPERATION == "device":
        col.equipment.jtag.program_device(jtag_id=JTAG_ID, key="image", **SETTINGS)
    elif OPERATION == "flash":
        col.equipment.jtag.program_cfgmem(jtag_id=JTAG_ID, key="flash", **SETTINGS)
    elif OPERATION == "verify":
        col.equipment.jtag.verify_cfgmem(jtag_id=JTAG_ID, key="verify", **SETTINGS)
    elif OPERATION == "boot":
        col.equipment.jtag.boot_from_cfgmem(jtag_id=JTAG_ID, key="boot", **SETTINGS)
    elif OPERATION == "tcl":
        source = SETTINGS or {"script": Path(__file__).with_name("inspect_target.tcl")}
        col.equipment.jtag.run_tcl(jtag_id=JTAG_ID, key="tcl", **source)
    else:
        raise ValueError("Supply a recognized OPERATION")


if __name__ == "__main__":
    main()
    col.endex()
