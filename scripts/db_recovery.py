import sqlite3
import os
import shutil
from datetime import datetime

def backup_db(db_path, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"app_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")

def verify_integrity(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        res = cursor.fetchone()
        conn.close()
        if res[0] == "ok":
            print("Database integrity: PASS")
            return True
        else:
            print(f"Database integrity: FAIL ({res[0]})")
            return False
    except Exception as e:
        print(f"Integrity check error: {e}")
        return False

if __name__ == "__main__":
    DB_PATH = "data/app.db"
    BACKUP_DIR = "backups"
    if os.path.exists(DB_PATH):
        backup_db(DB_PATH, BACKUP_DIR)
        verify_integrity(DB_PATH)
    else:
        print(f"DB not found at {DB_PATH}")
