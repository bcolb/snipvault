from __future__ import annotations
from pathlib import Path
from . import storage


def add(name: str, snippet: str, tags: list[str] | None = None, path: Path = storage.DEFAULT_VAULT_PATH) -> None:
    data = storage.load(path)
    data[name] = {"snippet": snippet, "tags": tags or []}
    storage.save(data, path)


def get(name: str, path: Path = storage.DEFAULT_VAULT_PATH) -> dict | None:
    return storage.load(path).get(name)


def delete(name: str, path: Path = storage.DEFAULT_VAULT_PATH) -> bool:
    data = storage.load(path)
    if name not in data:
        return False
    del data[name]
    storage.save(data, path)
    return True


def list_all(path: Path = storage.DEFAULT_VAULT_PATH) -> dict:
    return storage.load(path)


def search(query: str, path: Path = storage.DEFAULT_VAULT_PATH) -> dict:
    data = storage.load(path)
    q = query.lower()
    return {
        name: entry
        for name, entry in data.items()
        if q in name.lower()
        or q in entry["snippet"].lower()
        or any(q in tag.lower() for tag in entry["tags"])
    }
