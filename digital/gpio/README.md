# GPIO

Pin header map; loopback jumper on J_GPIO_LB for loopback script.

## Building blocks

| Script | Block |
| --- | --- |
| `test_output_high.py` | drive high → read true |
| `test_output_low.py` | drive low → read false |
| `test_output_voltage_high.py` | Vhigh → minimum |
| `test_output_voltage_low.py` | Vlow → maximum |
| `test_rise_time.py` | rise time → max ns |
| `test_fall_time.py` | fall time → max ns |
| `test_common_mode_voltage.py` | Vcm → limit |
| `test_differential_voltage.py` | Vdiff → limit |
| `test_loopback_pattern.py` | loopback → pattern |
