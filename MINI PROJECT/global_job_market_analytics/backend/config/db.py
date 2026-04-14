"""
backend/config/db.py
Database configuration and connection settings.
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH  = os.path.join(BASE_DIR, 'data', 'job_market.db')

DB_CONFIG = {
    'path': DB_PATH,
    'timeout': 30,
    'check_same_thread': False,
    'journal_mode': 'WAL',
    'foreign_keys': 'ON',
}

def get_db():
    """Return a configured SQLite connection."""
    conn = sqlite3.connect(DB_CONFIG['path'], timeout=DB_CONFIG['timeout'])
    conn.row_factory = sqlite3.Row
    conn.execute(f"PRAGMA journal_mode = {DB_CONFIG['journal_mode']}")
    conn.execute(f"PRAGMA foreign_keys = {DB_CONFIG['foreign_keys']}")
    return conn

def close_db(conn):
    if conn:
        conn.close()

def test_connection():
    try:
        conn = get_db()
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"[DB] Connected. Tables: {[t['name'] for t in tables]}")
        close_db(conn)
        return True
    except Exception as e:
        print(f"[DB] Connection failed: {e}")
        return False

if __name__ == '__main__':
    test_connection()
