# Tachometer / PWM

Fan connector pinout; PWM/tach on scope channel.

## Building blocks

| Script | Block |
| --- | --- |
| `test_fan_command_ack.py` | fan command → ack |
| `test_pwm_frequency.py` | PWM freq → expected |
| `test_pwm_duty_cycle.py.design` (reserved) | duty cycle → tolerance |
| `test_tachometer_rpm.py` | tach RPM → limit |

The fan acknowledgement command must exit 0 and print exactly `OK` (surrounding
whitespace is ignored). `NOT OK`, unrelated log text and nonzero exits fail.
The command confirms acknowledgement only; RPM/PWM requires a separate test.

## Fresh edge/frequency captures

The executable edge/frequency/tach blocks preset and own the scope. Use a
qualified driver (for example `tektronix-mdo4000`) and supply all probe, input,
vertical, timebase, record-length and trigger settings. The powered DUT must
already generate repetitive edges: these blocks do not create a one-time GPIO
transition. A missing trigger is an error. Match bandwidth/sample rate to the
edge being measured; verify the instrument's timing thresholds and valid-range
behavior for the chosen model. Scope timing evidence is in **seconds**; ns limits
are converted by `1e-9`. Frequency is Hz. Tach verification converts the recorded
frequency to RPM using `Hz * 60 / pulses_per_rev`; its maximum-only requirement
does not prove that a fan is spinning. Document any required tach pull-up.

## Bench hookup and prerequisites

Plugins: Equipment + Shared for scope/tach; Messaging for fan acknowledgement. Scope tip -> PWM or tach signal, reference -> compatible DUT return. Map fan supply, return, PWM input and tach output separately; provide a correctly referenced tach pull-up where required. Establish DUT/fan power, command setpoint and steady operating state, and obtain pulses/revolution from the actual fan. ACK alone does not prove speed. Duty-cycle measurement remains reserved.
