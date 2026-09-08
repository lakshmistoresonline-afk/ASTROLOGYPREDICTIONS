import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM profiles")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r['id']}, Name: {r['name']}")
conn.close()
