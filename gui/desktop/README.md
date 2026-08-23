# Desktop GUI catalog

Requires `colosseum-gui` with a `[[gui.desktop]]` row.

## Drivers

| Driver | Locators | Platforms |
|--------|----------|-----------|
| `sim` | automation_id / role+name / image | any (CI) |
| `generic` | image / x,y (best-effort) | Linux X11, Windows |
| `pywinauto` | AutomationId / Name / Invoke | **Windows only** |

## Blocks

| Test | Status | Notes |
|------|--------|-------|
| [image_click](image_click/) | Exemplar | Generic/sim image template click |
| [uia_click](uia_click/) | Exemplar | pywinauto/sim AutomationId click (Windows for real UIA) |
| [screenshot_match](screenshot_match/) | Exemplar | Capture + visual baseline |

## Screen objects

See [screens.py](screens.py).
