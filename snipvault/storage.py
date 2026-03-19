import json
import os
from pathlib import Path

DEFAULT_VAULT_PATH = Path.home() / ".snipvault" / "vault.json"


def load(path: Path = DEFAULT_VAULT_PATH) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save(data: dict, path: Path = DEFAULT_VAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
