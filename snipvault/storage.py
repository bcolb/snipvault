import sqlite3
import json
from pathlib import Path
from contextlib import contextmanager

DEFAULT_VAULT_PATH = Path.home() / ".snipvault" / "vault.db"


@contextmanager
def _connect(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS snippets "
        "(name TEXT PRIMARY KEY, snippet TEXT NOT NULL, tags TEXT NOT NULL DEFAULT '[]')"
    )
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()


def load(path: Path = DEFAULT_VAULT_PATH) -> dict:
    with _connect(path) as conn:
        rows = conn.execute("SELECT name, snippet, tags FROM snippets").fetchall()
    return {name: {"snippet": snippet, "tags": json.loads(tags)} for name, snippet, tags in rows}


def get_one(name: str, path: Path = DEFAULT_VAULT_PATH) -> dict | None:
    with _connect(path) as conn:
        row = conn.execute(
            "SELECT snippet, tags FROM snippets WHERE name = ?", (name,)
        ).fetchone()
    if row is None:
        return None
    return {"snippet": row[0], "tags": json.loads(row[1])}


def upsert(name: str, snippet: str, tags: list[str], path: Path = DEFAULT_VAULT_PATH) -> None:
    with _connect(path) as conn:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO snippets (name, snippet, tags) VALUES (?, ?, ?)",
                (name, snippet, json.dumps(tags)),
            )


def remove(name: str, path: Path = DEFAULT_VAULT_PATH) -> bool:
    with _connect(path) as conn:
        with conn:
            cursor = conn.execute("DELETE FROM snippets WHERE name = ?", (name,))
    return cursor.rowcount > 0
