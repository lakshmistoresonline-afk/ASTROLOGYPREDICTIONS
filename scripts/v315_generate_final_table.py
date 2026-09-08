import sqlite3
import json
import os

db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"

def generate():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get snapshots 100-115
    cursor.execute("SELECT * FROM prediction_outcomes WHERE id >= 100 AND id <= 115 ORDER BY domain")
    rows = cursor.fetchall()

    print("| Domain | Prediction (Trunc) | Score | Strength | Conf | Peak | Nodes | Status |")
    print("| :--- | :--- | :---: | :--- | :--- | :--- | :---: | :--- |")

    for r in rows:
        ev = json.loads(r['evidence_snapshot']) if r['evidence_snapshot'] else []
        nodes = len(ev)
        text = r['prediction_text'][:50] + "..."
        print(f"| {r['domain']} | {text} | {r['confluence_score']*100:.1f}% | {r['prediction_strength']} | {r['engine_confidence']} | {r['peak_date']} | {nodes} | {r['status']} |")

    conn.close()

if __name__ == "__main__":
    generate()
