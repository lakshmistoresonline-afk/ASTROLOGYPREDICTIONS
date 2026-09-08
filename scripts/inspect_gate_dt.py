import sqlite3
import json

conn = sqlite3.connect('D:/ASTROLOGYPREDICTIONS/data/app.db')
c = conn.cursor()
c.execute("SELECT raw_data FROM charts WHERE name='GateV323'")
row = c.fetchone()
if row:
    data = json.loads(row[0])
    print(f"GateV323 birth_datetime: {data.get('birth_datetime')}")

c.execute("SELECT raw_data FROM charts WHERE name='Subramanian T S'")
row = c.fetchone()
if row:
    data = json.loads(row[0])
    print(f"Subramanian birth_datetime: {data.get('birth_datetime')}")

conn.close()
