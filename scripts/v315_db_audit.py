import os
import sys
import sqlite3
from datetime import datetime

# Path to DB
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def audit():
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("# DATABASE AUDIT: prediction_outcomes\n")

    try:
        cursor.execute("SELECT COUNT(*) as total FROM prediction_outcomes")
        total = cursor.fetchone()['total']
        print(f"Total Records: {total}\n")

        # Group by engine version and status
        cursor.execute("""
            SELECT engine_version, status, group_id, COUNT(*) as count
            FROM prediction_outcomes
            GROUP BY engine_version, status, group_id
        """)
        rows = cursor.fetchall()
        print("## Record Distribution")
        print("| Engine | Status | Group | Count |")
        print("| :--- | :--- | :--- | :--- |")
        for r in rows:
            print(f"| {r['engine_version']} | {r['status']} | {r['group_id']} | {r['count']} |")

        # Check source script/provenance if possible
        # Look for the last 5 records
        print("\n## Last 5 Records Metadata")
        cursor.execute("SELECT id, created_at, engine_version, group_id, domain, status, actual_event_date FROM prediction_outcomes ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        print("| ID | Created At | Engine | Group | Domain | Status | Event Date |")
        print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for r in rows:
            print(f"| {r['id']} | {r['created_at']} | {r['engine_version']} | {r['group_id']} | {r['domain']} | {r['status']} | {r['actual_event_date']} |")

        # Trace Snapshot 80 if it exists
        print("\n## Snapshot 80 Forensic Trace")
        cursor.execute("SELECT * FROM prediction_outcomes WHERE id = 80")
        r = cursor.fetchone()
        if r:
            for key in r.keys():
                print(f"- **{key}**: {r[key]}")
        else:
            print("Snapshot 80 not found.")

    except sqlite3.OperationalError as e:
        print(f"Error: {e}")

    conn.close()

if __name__ == "__main__":
    audit()
