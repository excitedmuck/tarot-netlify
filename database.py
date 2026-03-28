"""SQLite persistence layer for readings, users, and insights."""
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "readings.db"))


def _conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                google_id   TEXT    UNIQUE NOT NULL,
                email       TEXT,
                name        TEXT,
                picture     TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS readings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                type            TEXT    NOT NULL,
                question        TEXT,
                spread_type     TEXT,
                cards           TEXT,
                interpretation  TEXT,
                metadata        TEXT    DEFAULT '{}',
                created_at      TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS insights (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                insight_text    TEXT,
                reading_count   INTEGER DEFAULT 0,
                generated_at    TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


def upsert_user(google_id: str, email: str, name: str, picture: str) -> int:
    with _conn() as c:
        c.execute(
            """INSERT INTO users (google_id, email, name, picture) VALUES (?,?,?,?)
               ON CONFLICT(google_id) DO UPDATE SET
                   email=excluded.email, name=excluded.name, picture=excluded.picture""",
            (google_id, email, name, picture),
        )
        row = c.execute("SELECT id FROM users WHERE google_id=?", (google_id,)).fetchone()
        return row["id"]


def save_reading(user_id: int, type_: str, question: str, spread_type: str,
                 cards, interpretation: str, metadata: dict = None) -> int:
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO readings
               (user_id, type, question, spread_type, cards, interpretation, metadata)
               VALUES (?,?,?,?,?,?,?)""",
            (
                user_id, type_, question, spread_type,
                json.dumps(cards) if not isinstance(cards, str) else cards,
                interpretation,
                json.dumps(metadata or {}),
            ),
        )
        return cur.lastrowid


def get_readings(user_id: int, limit: int = 100) -> list:
    with _conn() as c:
        rows = c.execute(
            """SELECT id, type, question, spread_type, cards, interpretation, metadata, created_at
               FROM readings WHERE user_id=? ORDER BY created_at DESC LIMIT ?""",
            (user_id, limit),
        ).fetchall()
    return [
        {
            "id": r["id"],
            "type": r["type"],
            "question": r["question"],
            "spread_type": r["spread_type"],
            "cards": json.loads(r["cards"]) if r["cards"] else [],
            "interpretation": r["interpretation"] or "",
            "metadata": json.loads(r["metadata"]) if r["metadata"] else {},
            "created_at": r["created_at"],
        }
        for r in rows
    ]


def reading_count(user_id: int) -> int:
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM readings WHERE user_id=?", (user_id,)).fetchone()[0]


def save_insight(user_id: int, insight_text: str, n_readings: int):
    with _conn() as c:
        c.execute(
            "INSERT INTO insights (user_id, insight_text, reading_count) VALUES (?,?,?)",
            (user_id, insight_text, n_readings),
        )


def get_insights(user_id: int, limit: int = 5) -> list:
    with _conn() as c:
        rows = c.execute(
            """SELECT id, insight_text, reading_count, generated_at
               FROM insights WHERE user_id=? ORDER BY generated_at DESC LIMIT ?""",
            (user_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]
