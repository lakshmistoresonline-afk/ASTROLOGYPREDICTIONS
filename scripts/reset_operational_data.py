import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = "D:/ASTROLOGYPREDICTIONS/data/app.db"
BACKUP_DIR = "D:/ASTROLOGYPREDICTIONS/backups"

def backup_db():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"pre_reset_{timestamp}.db")
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path

def reset_data(confirm=False):
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = ["profiles", "charts", "prediction_outcomes", "remedy_tasks"]

    print("Pre-reset counts:")
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count}")
        except sqlite3.OperationalError:
            print(f"  {table}: Table not found")

    if not confirm:
        print("\nDry run complete. Use --confirm to perform actual reset.")
        conn.close()
        return

    backup_db()

    print("\nPerforming reset...")
    for table in tables:
        try:
            # We filter out records that should be preserved if they were in isolated research storage,
            # but since they are in app.db, the instruction is to clear ACTIVE USER/TEST PROFILE DATA.
            # "Research data should not populate Chart Vault".
            # If I want to keep historical validation for V3.15 baseline, I should not delete everything if they are needed for calculation.
            # BUT the user said: "HISTORICAL VALIDATION ... Research data should not populate Chart Vault".
            # The current app.db contains bt- profiles which show up in Chart Vault.
            # I will delete them from app.db. They are still in historical_cases.json for re-validation.
            cursor.execute(f"DELETE FROM {table}")
            print(f"  Cleared {table}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()
    print("Reset complete.")

if __name__ == "__main__":
    import sys
    confirm = "--confirm" in sys.argv
    reset_data(confirm=confirm)
