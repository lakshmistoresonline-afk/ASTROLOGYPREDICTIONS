import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM charts WHERE lat > 10.9 AND lat < 11.1")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r['id']}, Name: {r['name']}, Lat: {r['lat']}, Lon: {r['lon']}")
conn.close()
