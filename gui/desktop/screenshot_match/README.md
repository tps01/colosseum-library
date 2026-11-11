# Screenshot match (desktop)

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `desktop_id` | `[gui.desktop]` id |
| `screenshot_path` | Run-relative capture |
| `baseline_path` | Golden PNG |
| `max_diff_ratio` | Max differing-pixel fraction |

Baselines are environment-locked (DPI, theme, GPU).

## Application prerequisites

Start/attach the intended application in an unlocked interactive desktop session, with known test data and window state. Use FlaUI on Windows for UIA locators; generic supports image/coordinate controls, not an accessibility tree. Sim does not drive a live application.

For visual/image checks, supply reviewed baseline/template PNGs at known paths and
lock viewport/window size, DPI, theme and fonts. Sample rectangles use screenshot
pixels; do not mix logical UI coordinates with physical pixel rectangles.
See [GUI driver setup](../../README.md) for install/platform requirements.

`settle_timeout_s` bounds a best-effort rendering stability wait before capture.
It does not establish business completion; when used after another block, that
block must verify the application-specific completion condition first.
