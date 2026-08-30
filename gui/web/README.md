# Web GUI catalog

Requires `colosseum-gui` with a `[[gui.web]]` row (`driver = sim` or
`playwright`).

## Blocks

| Test | Status | Notes |
| --- | --- | --- |
| [button_visible](button_visible/) | Exemplar | Click + v... |
| [screensh... | Exemplar | Capture + visual baseline compare |
| [contrast... | Exemplar | Sample two rects, WCAG contrast |
| [navigation_ms](navigation_ms/) | Exemplar | Measure navigate timing |

## Screen objects

See [screens.py](screens.py) for locator dict helpers (not Page Object classes).
