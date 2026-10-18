"""Envelope peak RF power from a new qualified-sensor acquisition."""

from __future__ import annotations

from pathlib import Path
from math import isfinite

import colosseum as col

# SETUP:
#   DUT RF output -> calibrated peak-capable sensor; pulse/gate/trigger mode prepared.
#   Apply a repeating DUT signal. Generic SCPI is not proof of peak capability.

USE_AUTOCONFIG = True

# --- procedure (replace every FILL_IN_HERE) ---
pwrmeter_id = FILL_IN_HERE
freq_hz = FILL_IN_HERE
sensor_channel = FILL_IN_HERE  # one-based physical sensor channel
path_loss_db = FILL_IN_HERE  # positive loss between DUT output plane and sensor
max_peak_dbm = FILL_IN_HERE


def main() -> None:
    if not isfinite(freq_hz) or freq_hz <= 0 or not isfinite(path_loss_db) or path_loss_db < 0:
        raise ValueError("Use positive frequency and finite nonnegative path loss")
    _load_bench()
    col.equipment.pwrmeter.set_frequency(pwrmeter_id=pwrmeter_id, frequency_hz=freq_hz, channel=sensor_channel)
    col.equipment.pwrmeter.set_offset_db(pwrmeter_id=pwrmeter_id, offset_db=path_loss_db, channel=sensor_channel)
    col.equipment.pwrmeter.acquire(pwrmeter_id=pwrmeter_id, channel=sensor_channel)
    col.equipment.pwrmeter.measure_power_peak_dbm(pwrmeter_id=pwrmeter_id, channel=sensor_channel, key="peak_dbm")
    col.shared.verify.verify_field(key="peak_dbm", maximum=max_peak_dbm)


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
