# Development tools

These scripts run from a checkout or can be copied into your project. They do
not register Colosseum plugins.

## Mask editor

Install colosseum-equipment in the same Python environment (its dependencies
include Matplotlib). Python also needs working Tk support. From this repository:

```sh
python tools/mask_editor.py --domain frequency --template freq_spur_floor --path masks/spurs.json
python tools/mask_editor.py --domain time --template time_pulse_envelope
python tools/mask_editor.py --import-path masks/spurs.json
```

The editor supports frequency and time masks, region editing, built-in templates,
background trace CSVs and JSON save/import. Omit `--path` to choose a destination
in the Save dialog. Save prints the absolute destination and exits with code 0;
Cancel closes without saving and exits with code 1. Run it as an offline tool;
relative paths are relative to your current directory.

Mask validation and built-in templates are supplied by the installed equipment
package. Keep that package compatible when copying this script. Equipment still
provides `col.equipment.tools.load_mask`, `save_mask` and `list_mask_templates`.
Procedures apply and verify masks through `col.equipment.speca` and
`col.equipment.oscope`. The old `col.equipment.tools.create_mask` entry point has
been replaced by this script.

Developer check (requires pytest and a display):

```sh
python -m pytest tools/test_mask_editor.py
```

## Release helpers

Use `windows/download_releases.ps1` and `windows/install_releases.ps1` on
Windows, or `linux/download_releases.sh` and `linux/install_releases.sh` on
Linux. The download helpers save assets in `tools/`; the install helpers create
an OS-specific virtual environment in their respective platform directory.
