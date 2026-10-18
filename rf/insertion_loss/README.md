# Insertion Loss (S21)

Use a qualified VNA driver. Connect port 1 to DUT input and port 2 to DUT output;
for S11 use the specified output termination (normally the calibrated VNA port 2).
Perform/verify calibration at the DUT connector reference planes with the same
cables, adapters and termination. Verify a known through/load before DUT runs;
no preset here silently erases that calibration. Configure source power for a
linear DUT response and receiver range, plus IF bandwidth and a valid point count.
The scripts own trace 1 and restrict the VNA to one trace for unambiguous markers.

| Script | Quantity |
| --- | --- |
| `test_s21_at_freq.py` | **Signed** MLOG S21 dB at the named marker after a new sweep; target +/- tolerance. |
| `test_s21_max_db.py` | Worst **positive loss** over the entire requested band, with raw CSV evidence. |

Band insertion_loss_db is `-min(S21_db)`;
largest insertion loss must be <= max_insertion_loss_db.
No absolute-value transformation is used. For S21 [-1, -10] dB, worst insertion
loss is 10 dB. For S11 [-1, -20] dB, worst return loss is 1 dB. Spot values remain
signed, e.g. -10 dB, so their targets are not interchangeable with positive loss.
Band tests target passive paths; active gain/compression requires its own method.

Fill band/source/IF settings and copy this whole folder. Limits use Shared 0.5.0+.
`save_trace_data` obtains a fresh sweep; the band scripts verify finite data,
point count, monotonic frequency and requested endpoints before deriving loss.
Artifact-capable output is required for a new band capture; numeric verify-only
replay uses its recorded derived measurement without fetching a new trace.

## VNA source lifecycle prerequisite

The fixture/operator owns VNA RF enable and DUT DC power. Current public VNA APIs
set source level and trigger/sweep state but provide no RF-output disable; neither
an aborted sweep nor closing a session guarantees RF off. Establish a qualified
source level before connecting the DUT and disable RF at the instrument or in
your fixture controller before reconnecting/rerouting. These blocks preserve
calibration and do not promise output-off teardown. Automated switching suites
must implement a supported fixture-specific RF interlock first.
