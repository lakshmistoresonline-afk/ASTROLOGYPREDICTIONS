import sqlite3
import os

DB_PATH = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def audit():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, status, cohort, prediction_text FROM prediction_outcomes WHERE source_type='REAL_WORLD'")
    rows = c.fetchall()
    print(f"Total REAL_WORLD Predictions: {len(rows)}")
    for r in rows[:5]:
        print(r)

    # Check for simulated mock data (it often has 'Mock' or 'Test' in the text)
    c.execute("SELECT count(*) FROM prediction_outcomes WHERE source_type='REAL_WORLD' AND prediction_text LIKE '%Mock%'")
    mock_count = c.fetchone()[0]
    print(f"Detected Mock REAL_WORLD: {mock_count}")

    conn.close()

if __name__ == "__main__":
    audit()
