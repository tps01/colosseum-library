"""Verify one full-duplex SPI frame using separate controller and target adapters."""

from pathlib import Path

import colosseum as col

from reference_common import required

SETTINGS = {
    "controller_id": FILL_IN_HERE,
    "target_id": FILL_IN_HERE,
    "mosi_hex": FILL_IN_HERE,
    "miso_hex": FILL_IN_HERE,
    "mode": FILL_IN_HERE,
    "clock_hz": FILL_IN_HERE,
    "timeout_ms": FILL_IN_HERE,
}


def spi_slave_response(settings):
    controller = settings["controller_id"]
    target = settings["target_id"]
    mosi = bytes.fromhex(settings["mosi_hex"])
    miso = bytes.fromhex(settings["miso_hex"])
    mode = settings["mode"]
    clock_hz = settings["clock_hz"]
    timeout_ms = settings["timeout_ms"]
    if controller == target:
        raise col.ProceduralFault("Select separate controller and target SPI IDs")
    if len(mosi) != len(miso) or not 1 <= len(miso) <= 64:
        raise col.ProceduralFault("Use equal-length MOSI and MISO patterns of 1–64 bytes")
    if type(mode) is not int or mode not in range(4):
        raise col.ProceduralFault("Set SPI mode to an integer in 0–3")
    if type(clock_hz) is not int or not 125_000 <= clock_hz <= 4_000_000:
        raise col.ProceduralFault("Use a clock within the two Aardvark adapters' supported range")
    if type(timeout_ms) is not int or not 1 <= timeout_ms <= 2_147_483_647:
        raise col.ProceduralFault("Supply a positive integer target timeout in milliseconds")

    applied = col.io.spi.configure(
        spi_id=controller, mode=mode, clock_hz=clock_hz, chip_select=0, bits_per_word=8
    )
    col.io.spi.target_start(spi_id=target, response=miso, key="arm_spi_target")
    try:
        controller_rx = col.io.spi.transfer(spi_id=controller, data=mosi, key="controller_miso")
        event = col.io.spi.target_receive(spi_id=target, timeout_ms=timeout_ms, key="target_mosi")
    finally:
        col.io.spi.target_stop(spi_id=target, key="stop_spi_target")

    if not isinstance(controller_rx, bytes) or len(controller_rx) != len(miso):
        raise col.ProceduralFault("Controller returned invalid MISO frame evidence")
    if not isinstance(event, dict) or event.get("event") != "received" or not isinstance(event.get("data_hex"), str):
        raise col.ProceduralFault("Target did not return a received SPI frame")
    try:
        target_rx = bytes.fromhex(event["data_hex"])
    except ValueError as exc:
        raise col.ProceduralFault("Target returned malformed MOSI bytes") from exc
    if type(event.get("nbytes")) is not int or event["nbytes"] != len(target_rx):
        raise col.ProceduralFault("Target byte count does not match the captured MOSI frame")
    return {
        "expected_mosi": mosi.hex(),
        "received_mosi": target_rx.hex(),
        "expected_miso": miso.hex(),
        "received_miso": controller_rx.hex(),
        "mode": mode,
        "requested_clock_hz": clock_hz,
        "actual_clock_hz": applied.get("actual_clock_hz"),
        "passed": target_rx == mosi and controller_rx == miso,
    }


def main() -> None:
    required(
        key="slave_response",
        collect=spi_slave_response,
        settings=SETTINGS,
        config=Path(__file__).with_name("config.toml"),
    )


if __name__ == "__main__":
    main()
    col.endex()
