import sqlite3
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("PROFILES:")
cursor.execute("SELECT id, name FROM profiles")
for r in cursor.fetchall():
    print(f"ID: {r[0]}, Name: {r[1]}")

print("\nCHARTS:")
cursor.execute("SELECT id, name FROM charts")
for r in cursor.fetchall():
    print(f"ID: {r[0]}, Name: {r[1]}")
conn.close()
