import sqlite3
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT prediction_text FROM prediction_outcomes WHERE chart_id='baae1f5a' LIMIT 1")
r = cursor.fetchone()
if r:
    print(r['prediction_text'])
conn.close()
