from __future__ import annotations
from pathlib import Path
from . import storage


def add(name: str, snippet: str, tags: list[str] | None = None, path: Path = storage.DEFAULT_VAULT_PATH) -> None:
    storage.upsert(name, snippet, tags or [], path)


def get(name: str, path: Path = storage.DEFAULT_VAULT_PATH) -> dict | None:
    return storage.get_one(name, path)


def delete(name: str, path: Path = storage.DEFAULT_VAULT_PATH) -> bool:
    return storage.remove(name, path)


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
