"""
db.py
-----
This is our "notebook". It knows how to:
  1. Open the notebook (connect to the database file)
  2. Make blank pages ready (create tables) the FIRST time we use it
  3. Write new experiment info onto the pages (insert data)
  4. Read old experiment info back (query data)
"""

import sqlite3
import os
import time
import uuid

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            name TEXT,
            created_at REAL,
            status TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS params (
            run_id TEXT,
            key TEXT,
            value TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            run_id TEXT,
            key TEXT,
            value REAL,
            step INTEGER,
            timestamp REAL
        )
    """)

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
    run_id = str(uuid.uuid4())[:8]
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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE runs SET status = ? WHERE run_id = ?", (status, run_id))
    conn.commit()
    conn.close()


def log_param(run_id, key, value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO params (run_id, key, value) VALUES (?, ?, ?)",
        (run_id, key, str(value)),
    )
    conn.commit()
    conn.close()


def log_metric(run_id, key, value, step=0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO metrics (run_id, key, value, step, timestamp) VALUES (?, ?, ?, ?, ?)",
        (run_id, key, float(value), step, time.time()),
    )
    conn.commit()
    conn.close()


def log_artifact(run_id, file_path, file_type="model"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO artifacts (run_id, file_path, file_type) VALUES (?, ?, ?)",
        (run_id, file_path, file_type),
    )
    conn.commit()
    conn.close()


def get_all_runs():
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