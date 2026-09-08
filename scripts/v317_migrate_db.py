import sqlite3
import os

DB_PATH = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create timeline_event_snapshots table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_event_snapshots (
        id VARCHAR(36) PRIMARY KEY,
        chart_id VARCHAR(36) NOT NULL,
        domain VARCHAR(50) NOT NULL,
        event_type VARCHAR(100),
        event_magnitude VARCHAR(20),
        start_date VARCHAR(20),
        peak_date VARCHAR(20),
        end_date VARCHAR(20),
        age_at_peak REAL,
        signal_strength VARCHAR(20),
        confidence VARCHAR(20),
        evidence_snapshot TEXT,
        why_now TEXT,
        status VARCHAR(30),
        engine_version VARCHAR(20) DEFAULT 'V3.17',
        actual_event_date VARCHAR(20),
        matching_status VARCHAR(30) DEFAULT 'UNKNOWN',
        timing_error_days INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(chart_id) REFERENCES charts(id)
    )
    """)

    conn.commit()
    conn.close()
    print("V3.17 Migration: timeline_event_snapshots table created.")

if __name__ == "__main__":
    migrate()
