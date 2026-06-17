import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "calls.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mc_number TEXT,
            carrier_name TEXT,
            load_id TEXT,
            origin TEXT,
            destination TEXT,
            carrier_offer REAL,
            final_rate REAL,
            outcome TEXT,
            sentiment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_call(call):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO calls (
            mc_number,
            carrier_name,
            load_id,
            origin,
            destination,
            carrier_offer,
            final_rate,
            outcome,
            sentiment
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        call.mc_number,
        call.carrier_name,
        call.load_id,
        call.origin,
        call.destination,
        call.carrier_offer,
        call.final_rate,
        call.outcome,
        call.sentiment
    ))

    conn.commit()
    conn.close()


def get_all_calls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            mc_number,
            carrier_name,
            load_id,
            origin,
            destination,
            carrier_offer,
            final_rate,
            outcome,
            sentiment,
            created_at
        FROM calls
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows