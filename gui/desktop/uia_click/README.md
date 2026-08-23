# UIA click (desktop)

Uses `automation_id=` (or role+name). Requires `driver=pywinauto` on Windows,
or `driver=sim` in CI. On Linux, `pywinauto` fails at connect with OSError.

## FILL_IN_HERE

| Name | Meaning |
|------|---------|
| `desktop_id` | `[[gui.desktop]]` id |
| `automation_id` | UIA AutomationId |
| `expected_text` | Control text after the click |
