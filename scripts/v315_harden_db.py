import os
import sys
import sqlite3

# Path to DB
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List of columns to add to prediction_outcomes
    cols = [
        ("calibrated_probability", "REAL"),
        ("what_to_do", "TEXT"),
        ("remedy_text", "TEXT")
    ]

    for col_name, col_type in cols:
        try:
            cursor.execute(f"ALTER TABLE prediction_outcomes ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")
        except sqlite3.OperationalError:
            print(f"Column {col_name} already exists or error.")

    conn.commit()
    conn.close()
    print("Hardening migration complete.")

if __name__ == "__main__":
    migrate()
