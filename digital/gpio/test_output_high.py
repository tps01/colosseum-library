"""DUT output high: command the DUT and independently sense it on bench DIO.
Required plugins: Equipment, Messaging, Shared. DUT GPIO output -> bench DIO input;
compatible return/voltage reference. The bench never drives this DUT output net.
"""
from pathlib import Path
import colosseum as col

USE_AUTOCONFIG = False
ssh_id = FILL_IN_HERE  # DUT control endpoint
sense_dio_id = FILL_IN_HERE  # independent bench input adapter
sense_line = FILL_IN_HERE  # zero-based sense input
settle_s = FILL_IN_HERE  # seconds after DUT command
command_timeout_s = FILL_IN_HERE  # positive command timeout seconds
dut_drive_command = FILL_IN_HERE  # vendor command driving the DUT pin high; exit 0
dut_release_command = FILL_IN_HERE  # vendor command restoring the fixture-safe DUT state; exit 0


def main() -> None:
    _load_bench()
    col.io.dio.configure_pin(dio_id=sense_dio_id, line=sense_line, output=False)
    try:
        col.messaging.ssh.exec(ssh_id=ssh_id, command=dut_drive_command, timeout=command_timeout_s, key="drive_high")
        col.messaging.ssh.verify_exit(key="drive_high", expected=0)
        col.shared.wait(duration=settle_s)
        col.io.dio.read_pin(dio_id=sense_dio_id, line=sense_line, key="pin_high")
        col.shared.verify.verify_field(key="pin_high", expected_val=True)
    finally:
        col.messaging.ssh.exec(ssh_id=ssh_id, command=dut_release_command, timeout=command_timeout_s, key="release_high")
        col.messaging.ssh.verify_exit(key="release_high", expected=0)


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
