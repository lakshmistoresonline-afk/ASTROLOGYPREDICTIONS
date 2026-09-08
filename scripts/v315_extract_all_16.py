import sqlite3
import json
import os

db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def extract():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get the last 16 snapshots
    cursor.execute("SELECT * FROM prediction_outcomes ORDER BY id DESC LIMIT 16")
    rows = cursor.fetchall()

    # Sort by domain for report consistency
    rows = sorted(rows, key=lambda x: x['domain'])

    print("# V3.15 FINAL 16-DOMAIN EXTRACTION\n")

    for r in rows:
        print(f"## {r['domain'].upper()} (ID: {r['id']})")
        print(f"**Text**: {r['prediction_text']}")
        print(f"**Strength**: {r['prediction_strength']} | **Score**: {r['confluence_score']*100:.2f}% | **Confidence**: {r['engine_confidence']}")
        print(f"**Timing**: {r['start_date']} to {r['end_date']} (Peak: {r['peak_date']})")
        print(f"**Phase**: {r['timing_phase']}")

        print("\n**Evidence Hierarchy**:")
        if r['evidence_snapshot']:
            ev = json.loads(r['evidence_snapshot'])
            for node in ev:
                print(f"- {node['source']}: {node['description']} (+{node['strength_score']*100:.1f})")
        else:
            print("- NO EVIDENCE STORED")

        print("\n**Action**: " + (r['what_to_do'] if r['what_to_do'] else "NOT STORED"))
        print("**Remedy**: " + (r['remedy_text'] if r['remedy_text'] else "NOT STORED"))
        print("\n" + "---" + "\n")

    conn.close()

if __name__ == "__main__":
    extract()
