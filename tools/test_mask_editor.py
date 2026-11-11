"""Run with pytest against an installed equipment package and a Tk display."""

import contextlib
import tkinter as tk

import pytest

from mask_editor import MaskEditorApp, MaskEditorCancelled
from colosseum_equipment.tools.mask_schema import load_mask


@pytest.mark.parametrize("domain,template", [
    ("frequency", "freq_spur_floor"), ("time", "time_pulse_envelope"),
])
def test_editor_save_and_reopen(tmp_path, domain, template):
    path = tmp_path / f"{domain}.json"
    try:
        app = MaskEditorApp(domain=domain, template=template, path=str(path))
    except tk.TclError as exc:
        pytest.skip(f"no Tk display: {exc}")
    try:
        app._root.update_idletasks()
        assert app._mask["regions"]
        app._on_save()
        assert app._result_path == path
        assert load_mask(path)["domain"] == domain
    finally:
        app._root.destroy()
    reopened = MaskEditorApp(domain=domain, import_path=str(path))
    try:
        assert reopened._mask == load_mask(path)
        reopened._on_cancel()
        assert reopened._result_path is None
        # Avoid mainloop here: cancellation has already happened.
        reopened._root.after(0, reopened._on_cancel)
        with pytest.raises(MaskEditorCancelled):
            reopened.run()
    finally:
        with contextlib.suppress(tk.TclError):
            reopened._root.destroy()
