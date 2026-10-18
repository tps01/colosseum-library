# RF power meter

Sensor at test frequency.

## Building blocks

| Script | Block |
| --- | --- |
| `test_avg_power_dbm.py` | avg power → window |
| `test_peak_power_dbm.py` | peak power → limit |
| `test_band_power_dbm.py.design` (reserved) | band power → limit |

## Peak versus average and fresh acquisition

Peak/average blocks require Equipment **0.5.0+**. Connect DUT RF OUT through the
qualified attenuator/DC block (where required) to the sensor; define DUT output
as the reference plane. The peak block's `path_loss_db` is positive path loss,
added by sensor correction. Zero/calibrate beforehand without RF as specified
by the sensor, then configure pulse/gate/trigger settings for the actual signal.
Apply a repetitive signal before running. The block starts and waits for a new
acquisition, then fetches envelope peak dBm; it never substitutes averaging=1.
Use a qualified peak-capable sensor and driver: generic SCPI availability is not
hardware qualification. The average block also starts a new acquisition.

U2000-series sensors are average-power sensors, not envelope-peak sensors;
their driver now explicitly refuses peak reads. See the
[Keysight measurement distinction](https://www.keysight.com/us/en/assets/7018-03996/application-notes/5991-2642.pdf).
The reserved band-power design is a separate integrated-power requirement.
