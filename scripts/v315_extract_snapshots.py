import sqlite3
import json
import os

db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def extract():
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    chart_id = 'baae1f5a'
    cursor.execute("SELECT * FROM prediction_outcomes WHERE chart_id = ?", (chart_id,))
    rows = cursor.fetchall()

    if not rows:
        print(f"No snapshots found for chart_id {chart_id}")
        return

    print(f"Total Snapshots Found: {len(rows)}\n")

    for r in rows:
        print(f"==================================================")
        print(f"SNAPSHOT ID: {r['id']}")
        print(f"==================================================")

        # Identity
        print(f"Profile ID: {r['chart_id']}")
        print(f"Domain: {r['domain']}")

        # Prediction Content
        # Note: 'prediction_title' or similar might not exist in schema, checking what's there
        print(f"Prediction Title: NOT STORED (Field not in schema)")
        print(f"Prediction Statement: {r['prediction_text'] if r['prediction_text'] else 'NOT STORED'}")

        # Metrics
        print(f"Strength: {r['prediction_strength'] if r['prediction_strength'] else 'NOT STORED'}")
        print(f"Score: {r['confluence_score'] if r['confluence_score'] is not None else 'NOT STORED'}")
        print(f"Confidence: {r['engine_confidence'] if r['engine_confidence'] else 'NOT STORED'}")
        print(f"Quality Score: {r['quality_score'] if r['quality_score'] is not None else 'NOT STORED'}")

        # Timing
        print(f"Start Date: {r['start_date'] if r['start_date'] else 'NOT STORED'}")
        print(f"Peak Date: {r['peak_date'] if r['peak_date'] else 'NOT STORED'}")
        print(f"End Date: {r['end_date'] if r['end_date'] else 'NOT STORED'}")
        print(f"Proximity Weight: {r['proximity_weight'] if r['proximity_weight'] is not None else 'NOT STORED'}")

        # Evidence
        print(f"Evidence Snapshot: {r['evidence_snapshot'] if r['evidence_snapshot'] else 'NOT STORED'}")

        # Meta
        print(f"Engine Version: {r['engine_version'] if r['engine_version'] else 'NOT STORED'}")
        print(f"Calculation Version: {r['calculation_version'] if r['calculation_version'] else 'NOT STORED'}")
        print(f"Created At: {r['created_at']}")
        print(f"Source Type: {r['source_type']}")
        print(f"Outcome Status: {r['status']}")

        # Governance
        print(f"Group ID: {r['group_id']}")
        print(f"Participant ID: {r['participant_id']}")
        print(f"Session ID: {r['session_id']}")

        print("\n")

    conn.close()

if __name__ == "__main__":
    extract()
