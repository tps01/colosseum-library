"""Aardvark master, DUT slave, 8-bit MSB-first, active-low CS0. Wire a common return and use one read-only frame."""

from pathlib import Path

import colosseum as col

from reference_common import required

SETTINGS = {
    "spi_id": FILL_IN_HERE,
    "tx_hex": FILL_IN_HERE,
    "expected_hex": FILL_IN_HERE,
    "response_offset": FILL_IN_HERE,
    "mode": FILL_IN_HERE,
    "clock_hz": FILL_IN_HERE,
}


def spi_master(s):
    tx = bytes.fromhex(s["tx_hex"])
    expected = bytes.fromhex(s["expected_hex"])
    offset = s["response_offset"]
    if not expected or offset < 0 or offset + len(expected) > len(tx):
        raise col.ProceduralFault("Expected SPI response must fit within the full-duplex frame")
    col.io.spi.configure(
        spi_id=s["spi_id"], mode=s["mode"], clock_hz=s["clock_hz"], chip_select=0, bits_per_word=8
    )
    rx = col.io.spi.transfer(spi_id=s["spi_id"], data=tx, key="full_duplex_rx")
    if not isinstance(rx, bytes) or len(rx) != len(tx):
        raise col.ProceduralFault("Invalid SPI receive length")
    return {
        "tx": tx.hex(),
        "rx": rx.hex(),
        "mode": s["mode"],
        "clock_hz": s["clock_hz"],
        "chip_select": 0,
        "passed": rx[offset : offset + len(expected)] == expected,
    }


def main() -> None:
    required(
        key="master_transfer",
        collect=spi_master,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
