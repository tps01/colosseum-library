"""Web screen locator helpers (copy-out testware)."""


def start_button() -> dict[str, str]:
    return {"role": "button", "name": "Start"}


def status_ready() -> dict[str, str]:
    return {"role": "status", "name": "Ready"}


def status_running() -> dict[str, str]:
    return {"role": "status", "name": "Running"}
