import sqlite3
import json
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM charts WHERE id='baae1f5a'")
r = cursor.fetchone()
if r:
    print(f"ID: {r['id']}")
    print(f"Name: {r['name']}")
    print(f"DOB: {r['dob']}")
    print(f"TOB: {r['tob']}")
    print(f"Lat: {r['lat']}, Lon: {r['lon']}, TZ: {r['tz']}")
    if r['raw_data']:
        data = json.loads(r['raw_data'])
        print(f"JSON Name: {data.get('name')}")
else:
    print("Not found.")
conn.close()
