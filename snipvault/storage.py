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


def save(data: dict, path: Path = DEFAULT_VAULT_PATH) -> None:
    with _connect(path) as conn:
        conn.execute("DELETE FROM snippets")
        conn.executemany(
            "INSERT INTO snippets (name, snippet, tags) VALUES (?, ?, ?)",
            [(name, entry["snippet"], json.dumps(entry["tags"])) for name, entry in data.items()],
        )
        conn.commit()
