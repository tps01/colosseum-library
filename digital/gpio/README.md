# GPIO

Pin header map; loopback jumper on J_GPIO_LB for loopback script.

## Building blocks

| Script | Block |
| --- | --- |
| `test_output_high.py` | DUT command high -> independent bench input reads true |
| `test_output_low.py` | DUT command low -> independent bench input reads false |
| `test_output_voltage_high.py` | Vhigh → minimum |
| `test_output_voltage_low.py` | Vlow → maximum |
| `test_rise_time.py` | rise time → max ns |
| `test_fall_time.py` | fall time → max ns |
| `test_common_mode_voltage.py.design` (reserved) | Vcm → limit |
| `test_differential_voltage.py.design` (reserved) | Vdiff → limit |
| `test_loopback_pattern.py` | fixture continuity, two low/high cycles -> matching independent readback |

## Static driven-interface voltage

`test_output_voltage_high.py` and `test_output_voltage_low.py` characterize a
**bench DIO output at the DUT input net**, under the connected DUT input load.
They do not command or characterize a DUT output. Connect DIO line to that net,
DMM HI to the same DUT-side point, and DMM LO to the shared signal return.
Disable competing drivers and establish compatible voltage levels and loading.
A DUT-output VOH/VOL test instead needs DUT-specific drive commands and a defined
output load; adapt the procedure explicitly for that purpose.

Install Equipment and Shared; configure `io.dio` and `equipment.dmm`. Provide
the physical DMM input/channel,
`settle_s` in seconds, and the minimum high or maximum low voltage in volts.
The script configures the individual DIO line as output, waits for settling,
then performs a fresh DC voltage reading. No scope Vpp or prior capture is used.

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

Plugins: Equipment and Shared, plus Messaging for DUT-commanded output blocks. Map the DUT header signals, bench DIO line numbers and shared return explicitly. Match voltage domains and input thresholds and disable competing drivers. State whether the DUT or fixture drives each net; do not connect two outputs together. Static DMM probes go at the DUT-side measurement point. Repetitive-edge capture additionally needs an already running DUT stimulus and a suitable scope/probe.

## DUT outputs versus fixture checks

High/low tests send DUT-specific SSH commands and read a separate **input-only**
bench DIO line connected to that DUT output. Fill the real drive and safe-release
commands and control endpoint; both command exit codes must succeed. Configure
DUT firmware/pin mux, supplies, input thresholds, voltage translation, return and
load before running. The bench does not write that net. A command ACK alone is
not evidence of a pin level. Each block restores the DUT using the supplied
release command, including on failure.

The loopback-pattern block is explicitly a **fixture self-test**. An external
jumper/passive fixture path connects two distinct lines; the procedure configures
one output and one input, drives two complete low/high cycles and records every
independent readback plus the aggregate pattern. Stuck-low/high and missing
connections cannot satisfy the entire pattern. It finishes output-low and then
releases that line to input. The DIO simulator does not emulate a jumper by
itself; passing simulated self-latch reads is not fixture or DUT qualification.
The static DMM high/low blocks are also bench-driven interface checks, as
specified above; adapt to DUT control before calling them DUT VOH/VOL tests.

## Static drive cleanup

The DIO-driven DC voltage blocks own only their selected fixture pin and release
it to input in `finally`, including after a DMM error. The DUT supply remains
externally owned. Release means high impedance, not a guaranteed low voltage;
provide the pull-up/down required for the safe idle state.
