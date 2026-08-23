"""Desktop screen locator helpers (copy-out testware)."""


def start_button_uia() -> dict[str, str]:
    """Windows UIA / sim tree locator."""
    return {"automation_id": "StartBtn"}


def start_button_image() -> dict[str, str]:
    """Generic/sim image locator (path filled by the test)."""
    return {"image": "goldens/start_button.png"}
