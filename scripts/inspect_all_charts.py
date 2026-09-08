import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT id, name, dob, raw_data FROM charts")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r['id']}, Name: {r['name']}, DOB: {r['dob']}")
    if r['raw_data']:
        try:
            data = json.loads(r['raw_data'])
            if "Subramanian" in str(data):
                print("FOUND SUBRAMANIAN IN RAW_DATA")
        except:
            pass
conn.close()
