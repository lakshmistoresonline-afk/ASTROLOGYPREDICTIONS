import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM charts ORDER BY saved_at DESC LIMIT 1")
r = cursor.fetchone()
if r:
    print(json.dumps(dict(r), default=str, indent=2))
else:
    print("No charts found.")
conn.close()
