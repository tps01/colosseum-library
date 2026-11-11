# Reserved measurement contracts

These are decisions for future implementations, not callable APIs. All 29
`.py.design` slots remain reserved. Their old speculative implementations have
been removed: an invented method name or a successful command is not evidence
that a DUT meets a requirement. Implementations must retain raw evidence, reject
missing/malformed/non-finite data, and distinguish acquisition errors from a
measured limit failure. Select actual supported hardware/transport APIs before
promoting a slot. No `shared.signal` namespace is implied.

## Protocol adapters

| Slots | Required method and evidence |
| --- | --- |
| I2C master write/read, slave ACK | Specify controller role, adapter, bus voltage/pull-ups, address width/reserved addresses, speed, timeout and repeated-start/STOP behavior. Record ACK/NACK and received bytes separately. Compare the defined register payload; an ACK alone does not prove its contents. A probe must not modify arbitrary devices. |
| SPI master transfer, slave response | Specify master/slave role, mode, bit order, clock, CS timing, full-duplex transaction bytes and expected response alignment. Record received bytes and transfer status. A master adapter cannot implement a slave-response fixture without slave-capable hardware. |
| JTAG IDCODE, IR/DR shift | Specify chain order/length, TAP reset, IR widths, instruction and DR length/bit order, TCK and reference voltage. Retain complete shifted bits and mask only documented variable fields. Compare IDCODE against manufacturer/part/version policy; never infer success from a completed shift. |
| 1-Wire ROM | Specify adapter, reset/presence timing, pull-up, power mode and single-device vs ROM search behavior. Retain all eight bytes, check family/serial expectations and ROM CRC. Reject bus contention, missing presence and all-zero/all-one responses. |
| 1-Wire scratchpad CRC | Select the device/ROM, initiate its operation and wait for documented completion, then read the full scratchpad. For a Dallas/Maxim CRC-8 device, compute CRC over received payload bytes (polynomial x^8+x^5+x^4+1, reflected 0x8C, initial zero), compare against the received CRC byte, and validate the device-specific payload layout. A fixed expected CRC is invalid for variable payloads. Use the device's specified algorithm if different. |
| 1-Wire parasitic power | Remove external VDD and verify it is absent at the DUT. Reset/select the device, start an operation that requires parasitic power, assert a qualified strong pull-up for its specified interval, release it, and read/validate the completed result and CRC. Record VDD, bus voltage/current or qualified supply evidence and operation timing. Reading one byte does not establish parasitic operation. Restore external supply/pull-up state in cleanup. |
| 1-Wire brownout presence | Sweep or step measured DUT supply through defined levels with specified dwell, reset/presence timing and recovery sequence. At each level acquire actual presence pulse evidence (present/absent plus timing), not a verification result or row-existence check. Define the threshold as the boundary between observed outcomes with voltage resolution, repeat count/hysteresis, and power-cycle recovery. Disable/restore the owned source on failure. |

## Timing and electrical measurements

| Slots | Required method and evidence |
| --- | --- |
| Digital/RF Allan deviation | Define oscillator reference, nominal frequency, phase vs frequency input, sample cadence/dead time, record duration, tau list, overlapping vs nonoverlapping estimator and fractional-frequency normalization. Retain timestamps/raw samples, counts per tau and uncertainty/confidence policy. Return dimensionless sigma_y(tau); reject unsupported tau or insufficient samples. The digital and RF slots share this definition, not an assumed FS740 method. |
| RMS jitter | Define period, cycle-to-cycle or time-interval-error jitter; edge polarity/threshold/hysteresis, sample count, bandwidth/filter and reference/detrending policy. Retain event timestamps and the stated statistic in seconds RMS. Do not substitute an unqualified scope scalar with unknown settings. |
| Alignment skew | Capture both signals simultaneously with calibrated channel/probe deskew. Define corresponding edges, threshold, polarity, modulo-period ambiguity, sample count, statistic and sign (B minus A). Report signed seconds and test both bounds; phase degrees need a stated frequency conversion. |
| Ethernet eye height | Specify PHY/speed/encoding, fixture/test mode, termination, compliance point, clock recovery, bandwidth/equalization and eye mask/sampling aperture. Retain waveform/eye histogram and uncertainty; report mV by the defined eye-height statistic. Ordinary DC amplitude is not eye height. |
| GPIO common mode, differential | Acquire calibrated simultaneous Vp and Vn with a qualified differential/isolated topology; define DC or waveform statistic and bandwidth. Compute Vcm=(Vp+Vn)/2 or Vdiff=Vp−Vn in volts on matching samples. State loading, reference, range, deskew and acceptance window. Never connect grounded scope returns across incompatible nodes. |
| PWM duty cycle | Acquire multiple complete cycles with defined polarity/threshold/hysteresis and bandwidth. Compute high duration/period per cycle, aggregate using a stated statistic and report percent (0..100). Require valid repetitive edges and a minimum count; constant levels are not zero/100% valid PWM evidence by default. |
| Eload current monotonic ramp | Define initial/final current, step or slew, settling/cadence, independent current-monitor scale/bandwidth, compliance voltage and noise allowance. Timestamp measured current and DUT voltage throughout the ramp. Reject missed samples, saturation or compliance dropout; compare successive measured samples with the declared noise allowance and confirm endpoints. Commanded setpoints or a returned Boolean cannot prove monotonic actual current. Always disengage the load and disable the owned source in cleanup. |

## RF analysis

For every trace-derived result, specify frequency range/grid, RBW/VBW, detector,
averaging, sweep completion, units and input/reference planes. Retain the raw
unsmoothed trace and correction data. Qualify analyzer/source linearity and noise
floor. Do not apply Savitzky–Golay or other smoothing to acceptance extrema:
it can erase narrow violations. Any display smoothing must remain separate from
the verdict. Interpolation must not bridge unmeasured gaps or extrapolate.

| Slots | Required method and evidence |
| --- | --- |
| Center frequency | Choose and name the definition: peak, midpoint of specified band-edge crossings, or power centroid. Define carrier/noise discrimination and search band. Report Hz with a method-specific uncertainty; do not silently switch definitions for asymmetric spectra. |
| Occupied bandwidth | Choose integrated-power OBW at a stated percentage (e.g. 99%) with defined equal-tail allocation, integration band, bin widths and noise subtraction policy. Integrate linear power, not dB values. An X-dB-down crossing bandwidth is a separate method and must be named separately. Report both edge frequencies and width in Hz; require the full signal inside the acquisition span. |
| Gain flatness | Measure corrected gain vs frequency using known DUT-input power or a calibrated S21 sweep. Define passband/grid and report max(gain)−min(gain) in dB from unsmoothed valid samples. Require adequate carrier SNR and no compression. Absolute output-power ripple is gain flatness only if input power is known constant at the DUT plane. |
| H2/H3 dBc | Measure the fundamental and exactly 2f/3f on fresh sweeps with appropriate separate receiver settings. Apply frequency-dependent path corrections. Report P_harmonic−P_fundamental in dBc; require a valid fundamental and qualify generator harmonics/analyzer distortion and harmonic noise-floor handling. Define fundamental drift and amplitude stability between sweeps. |
| Maximum spur dBc | Specify search band and explicit carrier/harmonic/modulation exclusion windows. Retain every included trace bin and frequency of the worst spur. Reference a measured, corrected carrier (or explicitly named total signal power); report max spur minus reference in dBc. A noise-floor-limited result is a bound with stated detection limit, not a fabricated exact spur measurement. |
| Mask margin | Define mask frequency reference (absolute Hz or carrier offset), amplitude reference (dBm, dBc, or density), interpolation and covered bandwidth. Compare all valid unsmoothed bins after correction. Margin = mask limit minus measured level, with the minimum margin and its frequency retained; nonnegative passes. Reject incomplete mask coverage and incompatible RBW/density units. |
| OIP3 | Use two independent low-distortion sources with characterized isolation and a linear DUT operating point. Measure both carriers and both IM3 products, distinguish noise floor from products, and document balanced-tone validity. For each side compute OIP3=P_carrier+(P_carrier−P_IM3)/2 at a stated output plane; report sides separately and select a declared acceptance statistic. Do not call a single IM3 level an intercept measurement. |
| P1dB | Sweep measured/calibrated input power from a verified small-signal region through compression within DUT ratings. Record corrected input/output pairs, establish a small-signal gain fit, bracket the first 1 dB deviation and interpolate with stated step size/uncertainty. Specify input P1dB vs output P1dB and recovery/repeatability. No crossing means an explicit bound or failed range requirement. Disable the owned RF source in cleanup. |
| Band power | Use a supported channel-power acquisition or a calibrated spectral integration with bin equivalent-noise-bandwidth and detector corrections. Specify band edges, density vs bin-power units, overlap/windowing and noise handling. Sum linear watts and convert to dBm once. A broadband sensor scalar cannot establish selected-band power in the presence of out-of-band energy. |

## Promotion decision

The contracts above are retained requirements, not promises to implement 29 new
features. Select the needed DUT, transport and instrument capability first; merge
overlapping Allan/trace analysis only when a real implementation needs it.
Promotion requires a supported acquisition path, numeric/evidence acceptance,
failure/timeout cleanup and a qualified worked example. Removed sketches should
not be reconstructed by renaming proposed calls.
