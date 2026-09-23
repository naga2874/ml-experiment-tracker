"""
db.py
-----
This is our "notebook". It knows how to:
  1. Open the notebook (connect to the database file)
  2. Make blank pages ready (create tables) the FIRST time we use it
  3. Write new experiment info onto the pages (insert data)
  4. Read old experiment info back (query data)

Think of the database file "experiments.db" as one single notebook file
that lives on your computer. Every time you run your training script,
we open the SAME notebook and add a new page to it.
"""

import sqlite3
import os
import time
import uuid

# This is the name of our notebook file. It will be created automatically
# the first time we run anything.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments.db")


def get_connection():
    """
    Opens the notebook so we can read or write in it.
    'sqlite3.connect' either opens the existing file, or creates
    a brand new empty one if it doesn't exist yet.
    """
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    """
    This draws the blank tables (like drawing lines/columns on notebook
    pages) IF they don't already exist. Safe to call this every time
    the program starts - it won't erase existing data.
    """
    conn = get_connection()
    cur = conn.cursor()

    # One row per "experiment run" - like one page per experiment.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            name TEXT,
            created_at REAL,
            status TEXT
        )
    """)

    # The "settings" you chose for that experiment (e.g. learning_rate=0.01)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS params (
            run_id TEXT,
            key TEXT,
            value TEXT
        )
    """)

    # The "results" you measured, possibly many times per run
    # (e.g. loss=0.5 at step 1, loss=0.3 at step 2, ...)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            run_id TEXT,
            key TEXT,
            value REAL,
            step INTEGER,
            timestamp REAL
        )
    """)

    # Where saved model files live for that run
    cur.execute("""
        CREATE TABLE IF NOT EXISTS artifacts (
            run_id TEXT,
            file_path TEXT,
            file_type TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_run(name="unnamed_run"):
    """
    Starts a brand new experiment page. Gives it a unique ID
    (like a page number nobody else has) and remembers when it started.
    Returns the run_id so we can keep writing to THIS page later.
    """
    run_id = str(uuid.uuid4())[:8]  # short random ID, e.g. 'a1b2c3d4'
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO runs (run_id, name, created_at, status) VALUES (?, ?, ?, ?)",
        (run_id, name, time.time(), "running"),
    )
    conn.commit()
    conn.close()
    return run_id


def finish_run(run_id, status="finished"):
    """Marks a run as done (or failed) so the dashboard knows it's complete."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE runs SET status = ? WHERE run_id = ?", (status, run_id))
    conn.commit()
    conn.close()


def log_param(run_id, key, value):
    """Writes down one setting, like 'learning_rate = 0.01'."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO params (run_id, key, value) VALUES (?, ?, ?)",
        (run_id, key, str(value)),
    )
    conn.commit()
    conn.close()


def log_metric(run_id, key, value, step=0):
    """Writes down one measurement, like 'loss = 0.42 at step 5'."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO metrics (run_id, key, value, step, timestamp) VALUES (?, ?, ?, ?, ?)",
        (run_id, key, float(value), step, time.time()),
    )
    conn.commit()
    conn.close()


def log_artifact(run_id, file_path, file_type="model"):
    """Remembers where a saved model file is for this run."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO artifacts (run_id, file_path, file_type) VALUES (?, ?, ?)",
        (run_id, file_path, file_type),
    )
    conn.commit()
    conn.close()


def get_all_runs():
    """Reads back a list of every experiment page ever written."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT run_id, name, created_at, status FROM runs ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_params(run_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM params WHERE run_id = ?", (run_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_metrics(run_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT key, value, step FROM metrics WHERE run_id = ? ORDER BY step ASC", (run_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
