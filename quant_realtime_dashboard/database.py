import sqlite3
from utils.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            timestamp INTEGER,
            symbol TEXT,
            price REAL,
            qty REAL
        )
    """)
    conn.commit()
    conn.close()
