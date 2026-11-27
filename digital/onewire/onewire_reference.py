"""Standard-speed 1-Wire reference transactions."""

import colosseum as col


def crc8(data):
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0x8C if crc & 1 else 0)
    return crc


def onewire_rom(s):
    expected = bytes.fromhex(s["expected_rom_hex"])
    if len(expected) != 8 or expected[0] != 0x28 or crc8(expected[:-1]) != expected[-1]:
        raise col.ProceduralFault("Expected a valid DS18B20 ROM")
    device = s["onewire_id"]
    col.io.onewire.configure(onewire_id=device, speed="standard")
    col.io.onewire.reset(onewire_id=device, required=True)
    raw = col.io.onewire.write_read(
        onewire_id=device, write_data=b"\x33", read_nbytes=8, key="rom_raw"
    )
    if not isinstance(raw, bytes) or len(raw) != 8 or len(set(raw)) == 1:
        raise col.ProceduralFault("Invalid 1-Wire ROM frame")
    crc = crc8(raw[:-1])
    return {
        "hex": raw.hex(),
        "received_crc": raw[-1],
        "calculated_crc": crc,
        "passed": raw == expected and raw[-1] == crc,
    }


def onewire_scratchpad(s):
    rom = bytes.fromhex(s["expected_rom_hex"])
    if len(rom) != 8 or rom[0] != 0x28 or crc8(rom[:-1]) != rom[-1]:
        raise col.ProceduralFault("Expected a valid DS18B20 ROM")
    device = s["onewire_id"]
    col.io.onewire.configure(onewire_id=device, speed="standard")
    col.io.onewire.select(onewire_id=device, rom=rom.hex())
    col.io.onewire.write(onewire_id=device, data=b"\x44")
    col.shared.wait(duration=0.75)
    col.io.onewire.select(onewire_id=device, rom=rom.hex())
    raw = col.io.onewire.write_read(
        onewire_id=device, write_data=b"\xbe", read_nbytes=9, key="scratchpad_raw"
    )
    if not isinstance(raw, bytes) or len(raw) != 9 or len(set(raw)) == 1:
        raise col.ProceduralFault("Invalid 1-Wire scratchpad frame")
    crc = crc8(raw[:-1])
    layout_valid = (raw[4] & 0x9F) == 0x1F and raw[5] == 0xFF and raw[7] == 0x10
    return {
        "hex": raw.hex(),
        "received_crc": raw[-1],
        "calculated_crc": crc,
        "passed": layout_valid and raw[-1] == crc,
    }
