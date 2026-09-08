import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM prediction_outcomes WHERE chart_id='baae1f5a'")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r['id']}, Domain: {r['domain']}, Strength: {r['prediction_strength']}, Created: {r['created_at']}, Source: {r['source_type']}")
conn.close()
