"""
database.py — NeonDB PostgreSQL Layer
Built by Vishnuram — Software Engineer | TCE Alumni

Database : neondb  (NeonDB cloud PostgreSQL)
Schema   : jyotish (all app tables live here)

Tables:
  jyotish.app_users          — registered user accounts
  jyotish.horoscope_profiles — saved horoscope data per user
  jyotish.match_results      — full 10-porutham match results
  jyotish.match_poruthams    — individual porutham scores per match

Credentials: loaded from .env (never hardcoded)
"""

import os
import json
import contextlib
from pathlib import Path
from typing import Optional

import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool
import streamlit as st


# ─────────────────────────────────────────────────────────────
# .env LOADER — pure Python, zero dependencies
# Works on Windows, venv, any environment
# ─────────────────────────────────────────────────────────────

def _read_env_file() -> dict:
    """Parse .env from same folder as this file or cwd."""
    for path in [Path(__file__).resolve().parent / ".env", Path.cwd() / ".env"]:
        if path.exists():
            result = {}
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                result[key.strip()] = val.strip().strip('"').strip("'")
            return result
    return {}

# Push .env into os.environ (won't override real OS env vars)
for _k, _v in _read_env_file().items():
    os.environ.setdefault(_k, _v)


# ─────────────────────────────────────────────────────────────
# PASSWORD HASHING (SHA-256)
# ─────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Store password as-is (plain text). No hashing."""
    return password

def verify_password(password: str, stored: str) -> bool:
    """Direct comparison — plain text passwords."""
    return password == stored


# ─────────────────────────────────────────────────────────────
# NEONDB CONNECTION — uses psycopg2.connect(host=, database=, ...)
# Password passed as plain kwarg — no URL encoding needed
# NeonDB uses DB_DATABASE (not DB_NAME)
# ─────────────────────────────────────────────────────────────
def _get_connect_kwargs() -> dict:
    """Build psycopg2 connection kwargs from Streamlit secrets or env."""

    # 1️⃣ Prefer Streamlit secrets (Cloud deployment)
    try:
        s = st.secrets
        if "DB_HOST" in s:
            return {
                "host":     str(s["DB_HOST"]).strip(),
                "port":     int(s.get("DB_PORT", 5432)),
                "database": str(s.get("DB_DATABASE", "neondb")).strip(),
                "user":     str(s["DB_USER"]).strip(),
                "password": str(s["DB_PASSWORD"]).strip(),
                "sslmode":  str(s.get("DB_SSLMODE", "require")).strip(),
                "connect_timeout": 15,
            }
    except Exception:
        pass

    # 2️⃣ Fallback to local .env / OS env (for development)
    host = os.environ.get("DB_HOST")
    if host:
        return {
            "host":     host.strip(),
            "port":     int(os.environ.get("DB_PORT", "5432")),
            "database": os.environ.get("DB_DATABASE", "neondb").strip(),
            "user":     os.environ.get("DB_USER", "").strip(),
            "password": os.environ.get("DB_PASSWORD", "").strip(),
            "sslmode":  os.environ.get("DB_SSLMODE", "require").strip(),
            "connect_timeout": 15,
        }

    raise RuntimeError("Database credentials not found")

# ─────────────────────────────────────────────────────────────
# CONNECTION POOL
# ─────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def _get_pool() -> ThreadedConnectionPool:
    """Thread-safe pool, cached by Streamlit for the app lifetime."""
    kwargs = _get_connect_kwargs()
    return ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        cursor_factory=psycopg2.extras.RealDictCursor,
        **kwargs,
    )


@contextlib.contextmanager
def get_conn():
    """Borrow a connection from pool. Auto-commit or rollback."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


# ─────────────────────────────────────────────────────────────
# SCHEMA + TABLE INIT
# Schema : jyotish
# ─────────────────────────────────────────────────────────────

def init_db() -> None:
    """Create schema + all tables if they don't exist. Safe to call every startup."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""

            -- Schema: all Jyotish Matcher tables live here
            CREATE SCHEMA IF NOT EXISTS jyotish;

            -- app_users: one row per registered account
            CREATE TABLE IF NOT EXISTS jyotish.app_users (
                id            SERIAL        PRIMARY KEY,
                username      TEXT          NOT NULL UNIQUE,
                display_name  TEXT          NOT NULL DEFAULT '',
                email         TEXT          NOT NULL UNIQUE,
                password_hash TEXT          NOT NULL DEFAULT '',
                created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
                last_login    TIMESTAMPTZ
            );

            -- horoscope_profiles: saved horoscope data, one row per person per user
            CREATE TABLE IF NOT EXISTS jyotish.horoscope_profiles (
                id            SERIAL        PRIMARY KEY,
                user_id       INTEGER       NOT NULL
                                REFERENCES jyotish.app_users(id) ON DELETE CASCADE,
                person_name   TEXT          NOT NULL,
                gender        TEXT          NOT NULL DEFAULT 'Unknown',
                star_name     TEXT          NOT NULL,
                padham        SMALLINT      NOT NULL CHECK (padham BETWEEN 1 AND 4),
                rasi_name     TEXT          NOT NULL,
                notes         TEXT          DEFAULT '',
                created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
            );

            -- match_results: one row per matching session, stores full result snapshot
            CREATE TABLE IF NOT EXISTS jyotish.match_results (
                id               SERIAL        PRIMARY KEY,
                user_id          INTEGER       NOT NULL
                                   REFERENCES jyotish.app_users(id) ON DELETE CASCADE,
                groom_profile_id INTEGER       NOT NULL
                                   REFERENCES jyotish.horoscope_profiles(id),
                bride_profile_id INTEGER       NOT NULL
                                   REFERENCES jyotish.horoscope_profiles(id),
                raw_score        NUMERIC(6,2)  NOT NULL DEFAULT 0,
                raw_max          NUMERIC(6,2)  NOT NULL DEFAULT 41,
                raw_percentage   NUMERIC(6,2)  NOT NULL DEFAULT 0,
                weighted_score   NUMERIC(8,2)  NOT NULL DEFAULT 0,
                max_weighted     NUMERIC(8,2)  NOT NULL DEFAULT 0,
                final_percentage NUMERIC(6,2)  NOT NULL DEFAULT 0,
                verdict          TEXT          NOT NULL DEFAULT '',
                verdict_color    TEXT          NOT NULL DEFAULT '',
                total_doshas     SMALLINT      NOT NULL DEFAULT 0,
                critical_doshas  JSONB         NOT NULL DEFAULT '[]',
                minor_doshas     JSONB         NOT NULL DEFAULT '[]',
                padham_analysis  JSONB         NOT NULL DEFAULT '{}',
                full_result_json JSONB         NOT NULL DEFAULT '{}',
                matched_at       TIMESTAMPTZ   NOT NULL DEFAULT NOW()
            );

            -- match_poruthams: 10 rows per match, one per porutham
            CREATE TABLE IF NOT EXISTS jyotish.match_poruthams (
                id             SERIAL        PRIMARY KEY,
                match_id       INTEGER       NOT NULL
                                 REFERENCES jyotish.match_results(id) ON DELETE CASCADE,
                porutham_name  TEXT          NOT NULL,
                tamil_name     TEXT          NOT NULL DEFAULT '',
                category       TEXT          NOT NULL DEFAULT '',
                score          NUMERIC(6,2)  NOT NULL DEFAULT 0,
                max_score      NUMERIC(6,2)  NOT NULL DEFAULT 0,
                percentage     NUMERIC(6,2)  NOT NULL DEFAULT 0,
                compatibility  TEXT          NOT NULL DEFAULT '',
                details        TEXT          NOT NULL DEFAULT '',
                is_dosha       BOOLEAN       NOT NULL DEFAULT FALSE,
                is_critical    BOOLEAN       NOT NULL DEFAULT FALSE
            );

            -- Indexes
            CREATE INDEX IF NOT EXISTS idx_jyotish_users_username
                ON jyotish.app_users(username);
            CREATE INDEX IF NOT EXISTS idx_jyotish_users_email
                ON jyotish.app_users(email);
            CREATE INDEX IF NOT EXISTS idx_jyotish_profiles_user
                ON jyotish.horoscope_profiles(user_id);
            CREATE INDEX IF NOT EXISTS idx_jyotish_matches_user
                ON jyotish.match_results(user_id);
            CREATE INDEX IF NOT EXISTS idx_jyotish_matches_time
                ON jyotish.match_results(matched_at DESC);
            CREATE INDEX IF NOT EXISTS idx_jyotish_poruthams_match
                ON jyotish.match_poruthams(match_id);

            """)


# ─────────────────────────────────────────────────────────────
# USER AUTH
# ─────────────────────────────────────────────────────────────

def register_user(username: str, email: str, password: str,
                  display_name: str = "") -> dict:
    """Register a new user. Raises ValueError on duplicate username/email."""
    username = username.strip().lower()
    email    = email.strip().lower()
    display  = display_name.strip() or username.title()
    ph       = hash_password(password)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM jyotish.app_users WHERE username=%s", (username,))
            if cur.fetchone():
                raise ValueError(f"Username '{username}' is already taken.")
            cur.execute("SELECT id FROM jyotish.app_users WHERE email=%s", (email,))
            if cur.fetchone():
                raise ValueError(f"Email '{email}' is already registered. Please sign in.")
            cur.execute("""
                INSERT INTO jyotish.app_users
                    (username, display_name, email, password_hash, last_login)
                VALUES (%s,%s,%s,%s,NOW()) RETURNING *
            """, (username, display, email, ph))
            return dict(cur.fetchone())


def login_user(username_or_email: str, password: str) -> dict:
    """Login by username or email. Raises ValueError on failure."""
    ident = username_or_email.strip().lower()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM jyotish.app_users WHERE username=%s OR email=%s",
                (ident, ident))
            row = cur.fetchone()
            if not row:
                raise ValueError("No account found with that username or email.")
            if not verify_password(password, row["password_hash"]):
                raise ValueError("Incorrect password. Please try again.")
            cur.execute(
                "UPDATE jyotish.app_users SET last_login=NOW() WHERE id=%s", (row["id"],))
            return dict(row)


def get_user_by_id(user_id: int) -> Optional[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM jyotish.app_users WHERE id=%s", (user_id,))
            r = cur.fetchone()
            return dict(r) if r else None


def update_user_profile(user_id: int, display_name: str, email: str) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jyotish.app_users SET display_name=%s, email=%s WHERE id=%s",
                (display_name.strip(), email.strip().lower(), user_id))


# ─────────────────────────────────────────────────────────────
# HOROSCOPE PROFILES
# ─────────────────────────────────────────────────────────────

def save_horoscope(user_id: int, person_name: str, gender: str,
                   star_name: str, padham: int, rasi_name: str,
                   notes: str = "") -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO jyotish.horoscope_profiles
                    (user_id, person_name, gender, star_name, padham, rasi_name, notes)
                VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id
            """, (user_id, person_name.strip(), gender, star_name, padham, rasi_name, notes))
            return cur.fetchone()["id"]


def get_user_horoscopes(user_id: int) -> list:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM jyotish.horoscope_profiles
                WHERE user_id=%s ORDER BY created_at DESC
            """, (user_id,))
            return [dict(r) for r in cur.fetchall()]


def delete_horoscope(horo_id: int, user_id: int) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM jyotish.horoscope_profiles WHERE id=%s AND user_id=%s",
                (horo_id, user_id))


# ─────────────────────────────────────────────────────────────
# MATCH RESULTS
# ─────────────────────────────────────────────────────────────

def save_match_result(user_id: int, groom_horo_id: int,
                      bride_horo_id: int, summary: dict) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO jyotish.match_results (
                    user_id, groom_profile_id, bride_profile_id,
                    raw_score, raw_max, raw_percentage,
                    weighted_score, max_weighted, final_percentage,
                    verdict, verdict_color, total_doshas,
                    critical_doshas, minor_doshas,
                    padham_analysis, full_result_json
                ) VALUES (
                    %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s, %s,%s
                ) RETURNING id
            """, (
                user_id, groom_horo_id, bride_horo_id,
                summary["raw_score"], summary["raw_max"], summary["raw_percentage"],
                summary["weighted_score"], summary["max_weighted"], summary["final_percentage"],
                summary["verdict"], summary["verdict_color"], summary["total_doshas"],
                json.dumps(summary["critical_doshas"]),
                json.dumps(summary["minor_doshas"]),
                json.dumps(summary["padham_analysis"]),
                json.dumps(summary),
            ))
            match_id = cur.fetchone()["id"]
            for r in summary["results"]:
                cur.execute("""
                    INSERT INTO jyotish.match_poruthams (
                        match_id, porutham_name, tamil_name, category,
                        score, max_score, percentage,
                        compatibility, details, is_dosha, is_critical
                    ) VALUES (%s,%s,%s,%s, %s,%s,%s, %s,%s,%s,%s)
                """, (
                    match_id, r["name"], r["tamil"], r["category"],
                    r["score"], r["max_score"], r["percentage"],
                    r["compatibility"], r["details"], r["dosha"], r["is_critical"],
                ))
            return match_id


def get_user_match_history(user_id: int) -> list:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT mr.*,
                       gp.person_name AS groom_name,
                       gp.star_name   AS groom_star,
                       gp.rasi_name   AS groom_rasi,
                       bp.person_name AS bride_name,
                       bp.star_name   AS bride_star,
                       bp.rasi_name   AS bride_rasi
                FROM   jyotish.match_results mr
                JOIN   jyotish.horoscope_profiles gp ON gp.id = mr.groom_profile_id
                JOIN   jyotish.horoscope_profiles bp ON bp.id = mr.bride_profile_id
                WHERE  mr.user_id = %s
                ORDER  BY mr.matched_at DESC
            """, (user_id,))
            result = []
            for r in cur.fetchall():
                d = dict(r)
                d["critical_doshas"] = (d["critical_doshas"] if isinstance(d["critical_doshas"], list)
                                        else json.loads(d["critical_doshas"]))
                d["minor_doshas"]    = (d["minor_doshas"] if isinstance(d["minor_doshas"], list)
                                        else json.loads(d["minor_doshas"]))
                result.append(d)
            return result


def get_match_by_id(match_id: int, user_id: int) -> Optional[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT mr.*,
                       gp.person_name AS groom_name,
                       gp.star_name   AS groom_star,
                       gp.rasi_name   AS groom_rasi,
                       gp.padham      AS groom_padham,
                       bp.person_name AS bride_name,
                       bp.star_name   AS bride_star,
                       bp.rasi_name   AS bride_rasi,
                       bp.padham      AS bride_padham
                FROM   jyotish.match_results mr
                JOIN   jyotish.horoscope_profiles gp ON gp.id = mr.groom_profile_id
                JOIN   jyotish.horoscope_profiles bp ON bp.id = mr.bride_profile_id
                WHERE  mr.id=%s AND mr.user_id=%s
            """, (match_id, user_id))
            row = cur.fetchone()
            if not row:
                return None
            d = dict(row)
            d["summary"]         = (d["full_result_json"] if isinstance(d["full_result_json"], dict)
                                    else json.loads(d["full_result_json"]))
            d["critical_doshas"] = (d["critical_doshas"] if isinstance(d["critical_doshas"], list)
                                    else json.loads(d["critical_doshas"]))
            d["minor_doshas"]    = (d["minor_doshas"] if isinstance(d["minor_doshas"], list)
                                    else json.loads(d["minor_doshas"]))
            d["padham_analysis"] = (d["padham_analysis"] if isinstance(d["padham_analysis"], dict)
                                    else json.loads(d["padham_analysis"]))
            return d


def delete_match(match_id: int, user_id: int) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM jyotish.match_results WHERE id=%s AND user_id=%s",
                (match_id, user_id))


def get_user_stats(user_id: int) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)                                  AS total_matches,
                       ROUND(AVG(final_percentage)::NUMERIC, 1) AS avg_score,
                       ROUND(MAX(final_percentage)::NUMERIC, 1) AS best_score
                FROM jyotish.match_results WHERE user_id=%s
            """, (user_id,))
            r1 = dict(cur.fetchone())
            cur.execute(
                "SELECT COUNT(*) AS n FROM jyotish.horoscope_profiles WHERE user_id=%s",
                (user_id,))
            r2 = dict(cur.fetchone())
            return {
                "total_matches":    int(r1["total_matches"] or 0),
                "avg_score":        float(r1["avg_score"]   or 0),
                "best_score":       float(r1["best_score"]  or 0),
                "saved_horoscopes": int(r2["n"]             or 0),
            }