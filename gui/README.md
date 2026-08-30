# GUI

Product UI automation via `colosseum-gui` (`col.gui.web` / `col.gui.desktop`).

Web and desktop are **separate kinds** (like `speca` vs `oscope`). Drivers
implement
each kind; generic commands are best-effort.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-gui` | `col.gui.web.*`, `col.gui.desktop.*` |
| `colosseum-core` | Runner / evidence |

`pip install colosseum-gui` includes Playwright, desktop drivers (pywinauto on
Windows; python-xlib + mss for generic/X11 on Linux), and test tooling.
Then run `playwright install chromium` for browser binaries.

## Catalog

| Folder | Kind | Typical driver |
| --- | --- | --- |
| [web/](web/) | Browser / Electron renderer | `playwright` (or `sim`) |
| [desktop/](desktop/) | Native window | `generic` (...)` |

## Platform notes

| Driver | Linux | Windows |
| --- | --- | --- |
| `sim` | yes | yes |
| `playwright` | yes | yes |
| `generic` / `x11` | yes (needs `$DISPLAY`) | yes (SendInput) |
| `pywinauto` | **no** (fails at connect) | yes |

X11-forwarded apps: use `col.gui.desktop` with `driver=generic` and
image/coords.
Accessibility trees are **not** forwarded over `ssh -X`.
