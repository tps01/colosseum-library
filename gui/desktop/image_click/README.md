# Image click (desktop)

Best-effort click using an image template. Works with `driver=generic` or `sim`.

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `desktop_id` | `[gui.desktop]` id |
| `image_path` | Path to template PNG |

## Platform

Linux needs `$DISPLAY` (X11/XWayland) for `generic`. Windows uses SendInput.

## Application prerequisites

Start/attach the intended application in an unlocked interactive desktop session, with known test data and window state. Use FlaUI on Windows for UIA locators; generic supports image/coordinate controls, not an accessibility tree. Sim does not drive a live application.

For visual/image checks, supply reviewed baseline/template PNGs at known paths and
lock viewport/window size, DPI, theme and fonts. Sample rectangles use screenshot
pixels; do not mix logical UI coordinates with physical pixel rectangles.
See [GUI driver setup](../../README.md) for install/platform requirements.

## Postcondition and deadline

The click is followed by bounded screenshot polling against an independently
reviewed **post-action** `baseline_path`. Fill `timeout_s`, `poll_s` and
`max_diff_ratio`; artifacts must be enabled. Only the final comparison records
PASS/FAIL, so normal rendering delay does not create failed intermediate rows.
The last screenshot remains available on timeout. Set an absolute baseline path
or one relative to the runner working directory. Do not use the click-target PNG
as the postcondition. Choose a tolerance/window whose changed status region is
large enough that the unchanged pre-action screen fails; lock window geometry
and remove unrelated animations. This proves the approved visible outcome, not
an unobserved backend operation.
