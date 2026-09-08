import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM prediction_outcomes")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r['id']}, ChartID: {r['chart_id']}, Participant: {r['participant_id']}")
conn.close()
