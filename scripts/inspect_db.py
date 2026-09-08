import sqlite3
import json

conn = sqlite3.connect('D:/ASTROLOGYPREDICTIONS/data/app.db')
c = conn.cursor()
c.execute("SELECT id, name, dob, tob, raw_data FROM charts WHERE id='913637d9'")
row = c.fetchone()
if row:
    print(f"ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"DOB: {row[2]}")
    print(f"TOB: {row[3]}")
    if row[4]:
        raw = json.loads(row[4])
        print("Raw Data Keys:", raw.keys())
        print("Raw birth_dob:", raw.get("birth_dob"))
else:
    print("Not found")
conn.close()
