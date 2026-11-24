"""Save job applications in a local SQLite database."""
import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path("data/tracker.db")
STATUSES = ["Saved", "Applied", "Interviewing", "Offer", "Rejected"]


def _connect(db_path=None):
    path = Path(db_path or DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Saved',
            score INTEGER,
            notes TEXT NOT NULL DEFAULT '',
            tailored_resume TEXT NOT NULL DEFAULT '',
            job_posting TEXT NOT NULL DEFAULT '',
            date_added TEXT NOT NULL
        )"""
    )
    return conn


def add_application(company, role="", status="Saved", score=None, notes="",
                    tailored_resume="", job_posting="", db_path=None):
    if not company.strip():
        raise ValueError("Company is required.")
    if status not in STATUSES:
        raise ValueError(f"Status must be one of {STATUSES}")
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO applications (company, role, status, score, notes, tailored_resume,"
            " job_posting, date_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (company.strip(), role.strip(), status, score, notes, tailored_resume,
             job_posting, date.today().isoformat()),
        )
        return cursor.lastrowid


def list_applications(db_path=None):
    with _connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def update_application(app_id, status, notes, db_path=None):
    if status not in STATUSES:
        raise ValueError(f"Status must be one of {STATUSES}")
    with _connect(db_path) as conn:
        conn.execute("UPDATE applications SET status = ?, notes = ? WHERE id = ?",
                     (status, notes, app_id))


def delete_application(app_id, db_path=None):
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
