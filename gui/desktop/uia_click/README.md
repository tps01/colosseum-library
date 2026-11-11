# UIA click (desktop)

Uses `automation_id=` (or role+name). Requires `driver=flaui` on Windows,
or `driver=sim` in CI.

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `desktop_id` | `[gui.desktop]` id |
| `automation_id` | UIA AutomationId |
| `expected_text` | Control text after the click |

## Application prerequisites

Start/attach the intended application in an unlocked interactive desktop session, with known test data and window state. Use FlaUI on Windows for UIA locators; generic supports image/coordinate controls, not an accessibility tree. Sim does not drive a live application.

For visual/image checks, supply reviewed baseline/template PNGs at known paths and
lock viewport/window size, DPI, theme and fonts. Sample rectangles use screenshot
pixels; do not mix logical UI coordinates with physical pixel rectangles.
See [GUI driver setup](../../README.md) for install/platform requirements.

## Asynchronous result

Fill `status_automation_id` for the result control separately from the clicked
control, and `timeout_s` for a bounded wait. The script waits for the action to
be enabled, clicks, waits for the expected status text, then records a text
verification. Start from a state where that result is not already present.
