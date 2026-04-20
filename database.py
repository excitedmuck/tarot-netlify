"""PostgreSQL persistence layer for readings, users, and insights."""
import json
import os

import psycopg2
import psycopg2.extras


def _conn():
    conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
    return conn


def init_db():
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id          SERIAL PRIMARY KEY,
                    google_id   TEXT    UNIQUE NOT NULL,
                    email       TEXT,
                    name        TEXT,
                    picture     TEXT,
                    created_at  TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS readings (
                    id              SERIAL PRIMARY KEY,
                    user_id         INTEGER NOT NULL REFERENCES users(id),
                    type            TEXT    NOT NULL,
                    question        TEXT,
                    spread_type     TEXT,
                    cards           TEXT,
                    interpretation  TEXT,
                    metadata        TEXT    DEFAULT '{}',
                    created_at      TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS insights (
                    id              SERIAL PRIMARY KEY,
                    user_id         INTEGER NOT NULL REFERENCES users(id),
                    insight_text    TEXT,
                    reading_count   INTEGER DEFAULT 0,
                    generated_at    TIMESTAMPTZ DEFAULT NOW()
                );
            """)
        c.commit()


def upsert_user(google_id: str, email: str, name: str, picture: str) -> int:
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute(
                """INSERT INTO users (google_id, email, name, picture) VALUES (%s,%s,%s,%s)
                   ON CONFLICT(google_id) DO UPDATE SET
                       email=EXCLUDED.email, name=EXCLUDED.name, picture=EXCLUDED.picture
                   RETURNING id""",
                (google_id, email, name, picture),
            )
            row = cur.fetchone()
        c.commit()
    return row[0]


def save_reading(user_id: int, type_: str, question: str, spread_type: str,
                 cards, interpretation: str, metadata: dict = None) -> int:
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute(
                """INSERT INTO readings
                   (user_id, type, question, spread_type, cards, interpretation, metadata)
                   VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
                (
                    user_id, type_, question, spread_type,
                    json.dumps(cards) if not isinstance(cards, str) else cards,
                    interpretation,
                    json.dumps(metadata or {}),
                ),
            )
            row = cur.fetchone()
        c.commit()
    return row[0]


def get_readings(user_id: int, limit: int = 100) -> list:
    with _conn() as c:
        with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """SELECT id, type, question, spread_type, cards, interpretation, metadata, created_at
                   FROM readings WHERE user_id=%s ORDER BY created_at DESC LIMIT %s""",
                (user_id, limit),
            )
            rows = cur.fetchall()
    return [
        {
            "id": r["id"],
            "type": r["type"],
            "question": r["question"],
            "spread_type": r["spread_type"],
            "cards": json.loads(r["cards"]) if r["cards"] else [],
            "interpretation": r["interpretation"] or "",
            "metadata": json.loads(r["metadata"]) if r["metadata"] else {},
            "created_at": str(r["created_at"]),
        }
        for r in rows
    ]


def reading_count(user_id: int) -> int:
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM readings WHERE user_id=%s", (user_id,))
            return cur.fetchone()[0]


def save_insight(user_id: int, insight_text: str, n_readings: int):
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO insights (user_id, insight_text, reading_count) VALUES (%s,%s,%s)",
                (user_id, insight_text, n_readings),
            )
        c.commit()


def get_insights(user_id: int, limit: int = 5) -> list:
    with _conn() as c:
        with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """SELECT id, insight_text, reading_count, generated_at
                   FROM insights WHERE user_id=%s ORDER BY generated_at DESC LIMIT %s""",
                (user_id, limit),
            )
            rows = cur.fetchall()
    return [dict(r) for r in rows]
