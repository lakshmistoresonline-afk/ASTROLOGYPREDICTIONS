import sqlite3
db_path = "D:/ASTROLOGYPREDICTIONS/data/app.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT engine_version, source_type FROM prediction_outcomes WHERE id=84")
r = cursor.fetchone()
if r:
    print(f"Engine: {r['engine_version']}, Source: {r['source_type']}")
conn.close()
