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
        ("group_id", "TEXT DEFAULT 'BETA_GROUP_1'"),
        ("participant_id", "TEXT"),
        ("session_id", "TEXT"),
        ("engine_version", "TEXT DEFAULT 'V3.15'"),
        ("timing_calibration_version", "TEXT DEFAULT 'V3.15'"),
        ("event_type", "TEXT"),
        ("event_magnitude", "TEXT"),
        ("engine_confidence", "TEXT"),
        ("evidence_snapshot", "TEXT"),
        ("proximity_weight", "REAL"),
        ("actual_event_end_date", "TEXT"),
        ("verification_level", "TEXT DEFAULT 'SELF_REPORTED'"),
        ("lead_time_days", "INTEGER"),
        ("practitioner_feedback", "TEXT"),
        ("timing_phase", "TEXT"),
        ("what_may_develop", "TEXT")
    ]

    for col_name, col_type in cols:
        try:
            cursor.execute(f"ALTER TABLE prediction_outcomes ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")
        except sqlite3.OperationalError:
            print(f"Column {col_name} already exists or error.")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
