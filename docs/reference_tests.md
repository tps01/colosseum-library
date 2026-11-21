# Reference procedures

Copy the selected procedure, its bench config example, and the helper files
listed in the topic's **Reference setup** section. Preserve their paths relative
to the project root, including the shared helper at the root. Put the project
root on PYTHONPATH first. From a checkout, use the catalog root directly.

For example, from the project root on Windows PowerShell:

```powershell
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"
colosseum run rf/spurs/test_spur_max_dbc.py --config config.toml
```

For bench-driven procedures, use the topic's config template and setup instructions to select
instruments, fixture wiring and measurement settings. Replace every
FILL_IN_HERE in the copied script. Run with an explicit config and keep
persisted artifacts enabled. The offline Ethernet mask check uses saved files
and runs without a bench config.

Scope acquisition examples use a preconfigured single-shot acquisition. Set the trigger,
record length, timebase, channel activity, probe scale and deskew before
running. Simultaneous measurements use channels with identical time grids.
Set the analysis window and maximum sample spacing for the measurement.

Spectrum analysis uses the fixture's calibrated reference plane and a
qualified, repeatable acquisition. Keep calibration files, analyzer settings
and the fixture description with the run. Configured limits apply to the
reference setup in each topic.

Offline runs used stubbed instruments and synthetic evidence.
