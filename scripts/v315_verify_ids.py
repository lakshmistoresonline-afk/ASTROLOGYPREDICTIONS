import sqlite3
conn = sqlite3.connect('D:/ASTROLOGYPREDICTIONS/data/app.db')
cursor = conn.cursor()
cursor.execute("SELECT id, domain FROM prediction_outcomes WHERE chart_id='baae1f5a' ORDER BY id")
for r in cursor.fetchall():
    print(f"ID: {r[0]}, Domain: {r[1]}")
conn.close()
