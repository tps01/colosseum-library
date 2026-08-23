# Image click (desktop)

Best-effort click using an image template. Works with `driver=generic` or `sim`.

## FILL_IN_HERE

| Name | Meaning |
|------|---------|
| `desktop_id` | `[[gui.desktop]]` id |
| `image_path` | Path to template PNG |

## Platform

Linux needs `$DISPLAY` (X11/XWayland) for `generic`. Windows uses SendInput.
