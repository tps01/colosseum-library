# Button visible (web)

## Plugins

- `colosseum-gui` (`col.gui.web`)

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `web_id` | `[gui.web]` id |
| `button_role` / `button_name` | Accessible locator for the control to click |
| `status_role` / `status_name` | Accessible locator that must become visible |

## Drivers

`sim` or `playwright`. Not desktop.

## Application prerequisites

Prepare the configured application page: start the service, authenticate if needed, seed known test data and ensure the target page/state is ready before the action. Use Playwright with installed browser binaries for live web tests; sim does not connect to the configured URL.

For visual/image checks, supply reviewed baseline/template PNGs at known paths and
lock viewport/window size, DPI, theme and fonts. Sample rectangles use screenshot
pixels; do not mix logical UI coordinates with physical pixel rectangles.
See [GUI driver setup](../../README.md) for install/platform requirements.

## Asynchronous result

Fill `timeout_s` for bounded enabled/status waits. The script waits for the
button to be enabled and the post-click status to become visible before its
verification. Select a status that uniquely represents the requested outcome;
prepare initial data/state where it is absent, rather than verifying a status
that was already visible before the click.
