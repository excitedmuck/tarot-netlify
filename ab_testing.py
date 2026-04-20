"""A/B testing framework for UI variants.

Assigns users to variant A or B randomly, persists in session state,
allows URL override via ?variant=A or ?variant=B.
Logs variant impressions and conversions to SQLite.
"""
import sqlite3
import os
import random
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "readings.db")


def _conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_ab_tables():
    """Create A/B testing tables if not present."""
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS ab_impressions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                variant     TEXT,
                page        TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS ab_conversions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                variant     TEXT,
                action      TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );
        """)


def get_or_assign_variant(session_state, query_params) -> str:
    """Return A or B variant for this session.

    Priority:
    1. Already assigned in session_state
    2. URL param ?variant=A/B
    3. Random 50/50 assignment
    """
    if "ab_variant" in session_state:
        return session_state["ab_variant"]

    # URL override
    if "variant" in query_params:
        v = query_params["variant"].upper()
        if v in ("A", "B"):
            session_state["ab_variant"] = v
            return v

    # Random assignment
    variant = random.choice(["A", "B"])
    session_state["ab_variant"] = variant
    return variant


def log_impression(session_state, page: str = "main"):
    """Log that this variant was shown."""
    variant = session_state.get("ab_variant", "A")
    sid = session_state.get("ab_session_id")
    if not sid:
        sid = hashlib.md5(str(random.random()).encode()).hexdigest()[:12]
        session_state["ab_session_id"] = sid

    try:
        with _conn() as c:
            c.execute(
                "INSERT INTO ab_impressions (session_id, variant, page) VALUES (?,?,?)",
                (sid, variant, page),
            )
    except Exception:
        pass  # non-critical


def log_conversion(session_state, action: str):
    """Log a conversion event (button click, reading completed, etc.)."""
    variant = session_state.get("ab_variant", "A")
    sid = session_state.get("ab_session_id", "unknown")
    try:
        with _conn() as c:
            c.execute(
                "INSERT INTO ab_conversions (session_id, variant, action) VALUES (?,?,?)",
                (sid, variant, action),
            )
    except Exception:
        pass


def get_ab_stats() -> dict:
    """Return impression and conversion counts per variant."""
    try:
        with _conn() as c:
            impressions = dict(
                c.execute(
                    "SELECT variant, COUNT(*) FROM ab_impressions GROUP BY variant"
                ).fetchall()
            )
            conversions = dict(
                c.execute(
                    "SELECT variant, COUNT(*) FROM ab_conversions GROUP BY variant"
                ).fetchall()
            )
        stats = {}
        for v in ("A", "B"):
            imp = impressions.get(v, 0)
            conv = conversions.get(v, 0)
            rate = round(conv / imp * 100, 1) if imp > 0 else 0
            stats[v] = {"impressions": imp, "conversions": conv, "conversion_rate": rate}
        return stats
    except Exception:
        return {"A": {}, "B": {}}
