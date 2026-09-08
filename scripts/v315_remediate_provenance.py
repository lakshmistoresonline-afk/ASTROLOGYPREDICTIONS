import os
import sys
import sqlite3

# Path to DB
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def remediate():
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Records 1-78 -> HISTORICAL
    cursor.execute("UPDATE prediction_outcomes SET source_type = 'HISTORICAL' WHERE id <= 78")
    print(f"Updated {cursor.rowcount} records to HISTORICAL.")

    # 2. Records 79-80 -> SYNTHETIC
    cursor.execute("UPDATE prediction_outcomes SET source_type = 'SYNTHETIC' WHERE id IN (79, 80)")
    print(f"Updated {cursor.rowcount} records to SYNTHETIC.")

    conn.commit()
    conn.close()
    print("Remediation complete.")

if __name__ == "__main__":
    remediate()
