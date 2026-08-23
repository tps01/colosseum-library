# Web GUI catalog

Requires `colosseum-gui` with a `[[gui.web]]` row (`driver = sim` or `playwright`).

## Blocks

| Test | Status | Notes |
|------|--------|-------|
| [button_visible](button_visible/) | Exemplar | Click + verify visible (sim/playwright) |
| [screenshot_match](screenshot_match/) | Exemplar | Capture + visual baseline compare |
| [contrast_ratio](contrast_ratio/) | Exemplar | Sample two rects, WCAG contrast |
| [navigation_ms](navigation_ms/) | Exemplar | Measure navigate timing |

## Screen objects

See [screens.py](screens.py) for locator dict helpers (not Page Object classes).
