"""Fixed protocol transactions on a qualified, isolated bus."""

import json

import colosseum as col
from colosseum.context import get_context

from reference_common import output_path


# Matches the externally installed Beagle Software API; no vendor files are bundled.
def i2c_packets(relative):
    import beagle_py

    with output_path(relative).open(encoding="utf-8") as handle:
        packets = [json.loads(line) for line in handle]
    no_stop = beagle_py.BG_READ_I2C_NO_STOP
    records = []
    for packet in packets:
        if packet.get("type") != "packet":
            continue
        words = packet["words"]
        status = packet["status"]
        if (
            packet["protocol"] != "i2c"
            or packet["loss"]
            or status not in (0, no_stop)
            or packet["count"] != len(words)
            or not words
            or any(type(word) is not int or not 0 <= word <= 511 for word in words)
        ):
            raise col.ProceduralFault("Invalid or incomplete I2C packet")
        records.append(
            (
                bytes(word & 255 for word in words),
                [not bool(word & 256) for word in words],
                status == no_stop,
            )
        )
    return records


def i2c(s, probe):
    address = s["address"]
    if not 8 <= address < 120:
        raise col.ProceduralFault("Use one explicit nonreserved 7-bit target address")
    controller, analyzer = s["i2c_id"], s["analyzer_id"]
    col.io.i2c.configure(i2c_id=controller, address=address, address_bits=7, clock_hz=s["clock_hz"])
    col.io.analyzer.configure(
        analyzer_id=analyzer, protocol="i2c", sample_rate_hz=s["sample_rate_hz"]
    )
    relative = "captures/transaction.jsonl"
    expected = b"" if probe else bytes.fromhex(s["expected_hex"])
    register = b"" if probe else bytes.fromhex(s["register_hex"])
    if not probe and (not register or not expected):
        raise col.ProceduralFault("Fill nonempty register and expected response bytes")
    col.io.analyzer.start(analyzer_id=analyzer, path=relative)
    observed = None
    try:
        col.shared.wait(duration=s["capture_settle_s"])
        if probe:
            col.io.i2c.write(i2c_id=controller, data=b"", key="address_only", optional=True)
        else:
            observed = col.io.i2c.write_read(
                i2c_id=controller,
                write_data=register,
                read_nbytes=len(expected),
                key="controller_rx",
                optional=True,
            )
    finally:
        try:
            col.io.analyzer.stop(analyzer_id=analyzer, timeout_s=s["timeout_s"])
        finally:
            summary = col.io.analyzer.export(analyzer_id=analyzer, path=relative, key="i2c_wire")
    if summary["loss_detected"] or summary["stop_reason"] != "stopped":
        raise col.ProceduralFault(f"Unusable I2C capture: {summary['stop_reason']}")
    records = i2c_packets(relative)
    address_byte = bytes([address << 1])
    if not records or records[0][0][:1] != address_byte:
        raise col.ProceduralFault("Did not capture the requested target transaction")
    tx, write_acks, continued = records[0]
    facts = {"packets": [{"hex": b.hex(), "acks": a, "continued": c} for b, a, c in records]}
    if probe:
        if len(records) != 1 or tx != address_byte or continued:
            raise col.ProceduralFault("Address probe had payload, extra packets, or no final STOP")
        commands = get_context().db.fetch_all_commands()
        if write_acks[0] and not any(
            row.key == "address_only" and row.status == "PASS" for row in commands
        ):
            raise col.ProceduralFault("Controller failed despite a captured address ACK")
        return facts | {"passed": write_acks[0]}
    if len(records) == 1 and not continued and not all(write_acks):
        if not (address_byte + register).startswith(tx):
            raise col.ProceduralFault("NACK occurred on an unexpected write frame")
        return facts | {"passed": False}
    if len(records) != 2 or not continued or records[1][2] or tx != address_byte + register:
        raise col.ProceduralFault("Expected one combined register write and read")
    rx, read_acks, _ = records[1]
    if rx[:1] != bytes([(address << 1) | 1]):
        raise col.ProceduralFault("Unexpected read address")
    if not all(write_acks) or not read_acks[0]:
        return facts | {"passed": False}
    if read_acks[1:] != [True] * (len(expected) - 1) + [False] or rx[1:] != observed:
        raise col.ProceduralFault(
            "Invalid read framing or disagreement between analyzer and controller"
        )
    return facts | {"passed": rx[1:] == expected}


def i2c_probe(s):
    return i2c(s, probe=True)


def i2c_register(s):
    return i2c(s, probe=False)
