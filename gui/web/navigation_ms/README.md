# Navigation timing (web)

## FILL_IN_HERE

| Name | Meaning |
| --- | --- |
| `web_id` | `[gui.web]` id |
| `url` | Absolute URL to open |
| `max_ms` | Maximum navigation duration in ms |

Requires `colosseum-shared` for `col.shared.verify.verify_field`, or replace
with a
dedicated GUI verifier when available.

## Application prerequisites

Prepare the configured application page: start the service, authenticate if needed, seed known test data and ensure the target page/state is ready before the action. Use Playwright with installed browser binaries for live web tests; sim does not connect to the configured URL.

For visual/image checks, supply reviewed baseline/template PNGs at known paths and
lock viewport/window size, DPI, theme and fonts. Sample rectangles use screenshot
pixels; do not mix logical UI coordinates with physical pixel rectangles.
See [GUI driver setup](../../README.md) for install/platform requirements.

The live Playwright metric ends at DOMContentLoaded. Acceptance is the inclusive
range 0..max_ms. This is not application/business-ready latency: asynchronous
data loading and rendering may continue afterward. To test business readiness,
time the action through a separately defined status condition instead of
relabeling this navigation metric. Sim supplies canned timings only.
