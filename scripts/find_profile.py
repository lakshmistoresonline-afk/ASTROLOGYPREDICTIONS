import sqlite3
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM charts")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r[0]}, Name: {r[1]}")
conn.close()
