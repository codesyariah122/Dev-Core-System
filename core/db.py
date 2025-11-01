# core/db.py
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), "devcore_projects.db")

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            client_name TEXT,
            project_type TEXT,
            stack TEXT,
            path TEXT,
            repo_url TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_project(name, client_name, project_type, stack, path, repo_url=None, status="created"):
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO projects (name, client_name, project_type, stack, path, repo_url, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, client_name, project_type, stack, path, repo_url, status, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def update_repo_url(name, repo_url):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE projects SET repo_url = ?, status = 'pushed' WHERE name = ?", (repo_url, name))
    conn.commit()
    conn.close()
