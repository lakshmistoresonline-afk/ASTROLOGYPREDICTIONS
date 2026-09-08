import sqlite3
import os

DB_PATH = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def fix():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Relabel simulated data to prevent REAL_WORLD contamination
    c.execute("""
        UPDATE prediction_outcomes
        SET source_type = 'SIMULATED'
        WHERE source_type = 'REAL_WORLD' AND prediction_text LIKE '%Mock%'
    """)
    affected = conn.total_changes
    print(f"Relabeled {affected} simulated records to 'SIMULATED'.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix()
