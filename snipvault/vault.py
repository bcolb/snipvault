from __future__ import annotations
from pathlib import Path
from . import storage


def add(name: str, snippet: str, tags: list[str] | None = None, path: Path = storage.DEFAULT_VAULT_PATH) -> None:
    """Save a snippet to the vault, overwriting any existing entry with the same name."""
    storage.upsert(name, snippet, tags or [], path)


def get(name: str, path: Path = storage.DEFAULT_VAULT_PATH) -> dict | None:
    """Retrieve a snippet by name. Returns None if not found."""
    return storage.get_one(name, path)


def delete(name: str, path: Path = storage.DEFAULT_VAULT_PATH) -> bool:
    """Delete a snippet by name. Returns True if deleted, False if it didn't exist."""
    return storage.remove(name, path)


def list_all(path: Path = storage.DEFAULT_VAULT_PATH) -> dict:
    """Return all snippets in the vault as a dict keyed by name."""
    return storage.load(path)


def search(query: str, path: Path = storage.DEFAULT_VAULT_PATH) -> dict:
    """Search snippets by name, content, or tag. Case-insensitive substring match."""
    data = storage.load(path)
    q = query.lower()
    return {
        name: entry
        for name, entry in data.items()
        if q in name.lower()
        or q in entry["snippet"].lower()
        or any(q in tag.lower() for tag in entry["tags"])
    }
