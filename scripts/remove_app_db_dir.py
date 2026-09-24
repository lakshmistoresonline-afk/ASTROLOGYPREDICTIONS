import os
import shutil

app_db_dir = r"D:\ASTROLOGYPREDICTIONS\app\db"
if os.path.exists(app_db_dir):
    shutil.rmtree(app_db_dir, ignore_errors=True)
    print(f"Removed shadowing directory {app_db_dir}")
