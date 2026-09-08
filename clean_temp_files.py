import os
import shutil

root_dir = "D:/ASTROLOGYPREDICTIONS"

# 1. Delete temporary HTML dumps in root
temp_htmls = [
    "current_dash.html",
    "dashboard_audit.html",
    "dump_de9427a1.html",
    "gate_dash.html",
    "rendered_dashboard.html",
    "subra_dash.html",
    "temp_index.html"
]

for h in temp_htmls:
    path = os.path.join(root_dir, h)
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed temp html: {h}")

# 2. Clear log files
log_path = os.path.join(root_dir, "logs", "app.log")
if os.path.exists(log_path):
    with open(log_path, "w") as f:
        f.write("")
    print("Cleared logs/app.log")

# 3. Remove __pycache__ folders
for root, dirs, files in os.walk(root_dir):
    for d in dirs:
        if d == "__pycache__":
            cache_path = os.path.join(root, d)
            shutil.rmtree(cache_path, ignore_errors=True)
            print(f"Removed cache dir: {cache_path}")

print("Cleanup complete.")
