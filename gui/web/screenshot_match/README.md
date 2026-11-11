# Screenshot match (web)

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `web_id` | `[gui.web]` id |
| `screenshot_path` | Run-relative capture path |
| `baseline_path` | Golden PNG (usually project-relative) |
| `max_diff_ratio` | Max fraction of differing pixels |

## Drivers

`sim` or `playwright`.

## Application prerequisites

Prepare the configured application page: start the service, authenticate if needed, seed known test data and ensure the target page/state is ready before the action. Use Playwright with installed browser binaries for live web tests; sim does not connect to the configured URL.

For visual/image checks, supply reviewed baseline/template PNGs at known paths and
lock viewport/window size, DPI, theme and fonts. Sample rectangles use screenshot
pixels; do not mix logical UI coordinates with physical pixel rectangles.
See [GUI driver setup](../../README.md) for install/platform requirements.

`settle_timeout_s` bounds a best-effort rendering stability wait before capture.
Prepare the intended business/application state first; screenshot stability alone
is not completion evidence.
