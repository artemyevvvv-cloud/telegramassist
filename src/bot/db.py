import sqlite3
import os
from pathlib import Path
from datetime import datetime

_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("DB_PATH", str(_ROOT / "data" / "logs.db")))


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                ts        TEXT NOT NULL,
                user_id   INTEGER NOT NULL,
                username  TEXT,
                full_name TEXT,
                msg_type  TEXT NOT NULL,
                text      TEXT,
                reply     TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user ON messages(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ts ON messages(ts)")


def log_message(user_id: int, username: str, full_name: str,
                msg_type: str, text: str, reply: str = None):
    with _conn() as conn:
        conn.execute(
            "INSERT INTO messages (ts, user_id, username, full_name, msg_type, text, reply) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(timespec="seconds"),
             user_id, username, full_name, msg_type, text, reply),
        )
