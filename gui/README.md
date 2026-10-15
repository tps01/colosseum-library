# GUI

Product UI automation via `colosseum-gui` (`col.gui.web` / `col.gui.desktop`).

Web and desktop are **separate kinds** (like `speca` vs `oscope`). Drivers
implement each kind; generic commands are best-effort.

## Plugins

| Plugin | Used for |
| --- | --- |
| `colosseum-gui` | `col.gui.web.*`, `col.gui.desktop.*` |
| `colosseum-core` | Runner / evidence |
| `colosseum-shared` | Optional file wait helpers (`verify_new_file`, …) |

`pip install colosseum-gui` includes Playwright, desktop drivers (**FlaUI** /
pythonnet on Windows; python-xlib + mss for generic/X11 on Linux), and test
tooling. Then run `playwright install chromium` for browser binaries.

Use **colosseum-gui 0.2.3+** when you need launch `args=` or chord `press_key`.

## Catalog

| Folder | Kind | Typical driver |
| --- | --- | --- |
| [web/](web/) | Browser / Electron renderer | `playwright` (or `sim`) |
| [desktop/](desktop/) | Native window | `flaui` (Windows), `generic`, or `sim` |

## Platform notes

| Driver | Linux | Windows |
| --- | --- | --- |
| `sim` | yes | yes |
| `playwright` | yes | yes |
| `generic` | yes (needs `$DISPLAY`) | yes |
| `flaui` | **no** | yes (UIA3) |

X11-forwarded apps: use `col.gui.desktop` with `driver=generic` and
image/coords. Accessibility trees are **not** forwarded over `ssh -X`.

For a full multi-desktop teaching suite (harness + hotkey + file wait), see
`colosseum-gui/examples/desktop_suite/` rather than copying these blocks alone.
