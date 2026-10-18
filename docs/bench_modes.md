# Simulation and live bench setup

Most example rows select `driver = sim`. Those rows exercise procedure plumbing
with generated responses. They do not contact the DUT, browser or instrument,
and a passing simulated run is not evidence of physical performance. Changing
only `resource`, `url` or an application title does **not** change a sim driver.

## Copy-out transition

1. Copy only the topic folders and companion helpers you need. Fill every
   `FILL_IN_HERE`, copy the relevant config example to `config.toml`, and supply
   the required parameter/baseline files. Keep only instrument rows used by the
   procedure; examples can contain categories for reserved neighboring designs.
2. For each equipment row, change both `driver = visa` and `resource` to the
   actual VISA address, select a supported `model`, and match its ID/channel in
   the script. `model = generic` means generic SCPI, not guaranteed compatibility.
   For example, after discovering your DMM address:

   ```toml
   [equipment.dmm]
   dmm_id = 1
   driver = visa
   resource = "FILL_IN_HERE"
   model = generic
   ```

   This minimal row is an illustration, not a complete config for a PSU+DMM
   procedure. Copy the actual model/address for **every** instrument it uses.
3. Replace DIO/SSH simulation with a supported adapter/transport and its required
   fields. Bus designs are still reserved. For web use `driver = "playwright"`
   and install its browser binaries; for Windows UIA use `driver = "flaui"`;
   generic desktop image/coordinate automation needs a live supported desktop.
   Replace sim-specific seed/response fields, not just the endpoint string.
4. Follow the topic's hookup and readiness requirements. Qualify command support,
   channel mappings, trigger/completion behavior, source/load ratings and output
   ownership. Calibration, compensation/path loss and uncertainty belong to the
   selected fixture; a schema-valid config cannot supply them.
5. Run with an explicit filled config, e.g.
   `colosseum run test_rail_voltage.py --config config.toml --parameters parameters.toml`.
   Inspect the resolved config/logs and device response to confirm that all rows
   intended to be live use live drivers. Deliberately mixed runs must identify
   which evidence is simulated.

`USE_AUTOCONFIG=True` discovers VISA equipment when no config is already loaded;
it does not replace an explicitly loaded sim config. Export/discover first and
copy the resulting IDs into the procedure. DIO, SSH, application state, DUT
enabling, routing and physical calibration still require explicit preparation.

`host/bench_prerequisites` is a computer check. `require_visa=True` makes VISA
required and disallows the simulated VISA backend; false makes it optional and
allows simulation. A working real VISA backend still does not prove that any
configured row is live or that a connected instrument supports a given method.

## Which instruments are needed?

Use the active script and its topic README as the authority. Static DC needs the
specified DMM; loaded-rail needs PSU, eload and DMM; transient needs PSU, eload,
scope and a calibrated current monitor; two-tone IM3 needs two isolated sources
and an analyzer; VNA blocks need the calibrated VNA fixture. Unused FS740/ASG or
other rows in neighboring reserved examples are not prerequisites for a simpler
active block. Remove those rows rather than connecting unrelated equipment.

Use Host **0.4.3+** for reliable PyVISA-sim identification: its native display
string can omit `@sim`, so earlier Host versions can misclassify that backend.
