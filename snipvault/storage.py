import sqlite3
import json
from pathlib import Path
from contextlib import contextmanager

DEFAULT_VAULT_PATH = Path.home() / ".snipvault" / "vault.db"


def init_db(path: Path) -> None:
    """Create the vault database and snippets table if they don't already exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS snippets "
            "(name TEXT PRIMARY KEY, snippet TEXT NOT NULL, tags TEXT NOT NULL DEFAULT '[]')"
        )


@contextmanager
def _connect(path: Path):
    """Open a connection to the vault, initializing the schema if needed."""
    init_db(path)
    conn = sqlite3.connect(path)
    try:
        yield conn
    finally:
        conn.close()


def _parse_tags(raw: str) -> list[str]:
    """Deserialize a JSON tags string, returning an empty list if malformed."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []


def load(path: Path = DEFAULT_VAULT_PATH) -> dict:
    """Return all snippets as a dict keyed by name."""
    with _connect(path) as conn:
        rows = conn.execute("SELECT name, snippet, tags FROM snippets").fetchall()
    return {name: {"snippet": snippet, "tags": _parse_tags(tags)} for name, snippet, tags in rows}


def get_one(name: str, path: Path = DEFAULT_VAULT_PATH) -> dict | None:
    """Return a single snippet by name, or None if it doesn't exist."""
    with _connect(path) as conn:
        row = conn.execute(
            "SELECT snippet, tags FROM snippets WHERE name = ?", (name,)
        ).fetchone()
    if row is None:
        return None
    return {"snippet": row[0], "tags": _parse_tags(row[1])}


def upsert(name: str, snippet: str, tags: list[str], path: Path = DEFAULT_VAULT_PATH) -> None:
    """Insert or replace a snippet. Uses a single atomic statement."""
    with _connect(path) as conn:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO snippets (name, snippet, tags) VALUES (?, ?, ?)",
                (name, snippet, json.dumps(tags)),
            )


def remove(name: str, path: Path = DEFAULT_VAULT_PATH) -> bool:
    """Delete a snippet by name. Returns True if it existed, False otherwise."""
    with _connect(path) as conn:
        with conn:
            cursor = conn.execute("DELETE FROM snippets WHERE name = ?", (name,))
    return cursor.rowcount > 0
