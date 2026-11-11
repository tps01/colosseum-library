"""DC voltage of a DIO-driven low at the DUT interface, under its input load."""

from __future__ import annotations

from pathlib import Path

import colosseum as col

# SETUP:
#   DIO line -> DUT GPIO input net; DMM HI -> that net; DMM LO -> shared return.
#   Disable other drivers. DUT power, input load and voltage compatibility are prerequisites.

USE_AUTOCONFIG = False

# --- procedure (replace every FILL_IN_HERE) ---
dio_id = FILL_IN_HERE
line = FILL_IN_HERE
dmm_id = FILL_IN_HERE  # configured DC voltmeter
dmm_channel = FILL_IN_HERE  # physical DMM input/channel (usually 1)
settle_s = FILL_IN_HERE  # seconds after drive change before DC measurement
v_low_max = FILL_IN_HERE


def main() -> None:
    _load_bench()
    try:
        col.io.dio.configure_pin(dio_id=dio_id, line=line, output=True)
        col.io.dio.write_pin(dio_id=dio_id, line=line, value=False)
        col.shared.wait(duration=settle_s)
        col.equipment.dmm.measure_voltage(dmm_id=dmm_id, channel=dmm_channel, key="v_low")
        col.shared.verify.verify_field(key="v_low", maximum=v_low_max)
    finally:
        col.io.dio.configure_pin(dio_id=dio_id, line=line, output=False)


def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))


if __name__ == "__main__":
    main()
    col.endex()
