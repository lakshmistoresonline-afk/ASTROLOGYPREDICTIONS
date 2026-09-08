import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM prediction_outcomes WHERE id=101")
r = cursor.fetchone()
if r:
    print(f"ID: {r['id']}")
    print(f"Domain: {r['domain']}")
    print(f"Text: {r['prediction_text']}")
    ev = json.loads(r['evidence_snapshot'])
    print(f"Evidence Nodes: {len(ev)}")
    for n in ev:
        print(f"  - {n['source']}: {n['description']}")
else:
    print("Not found.")
conn.close()
