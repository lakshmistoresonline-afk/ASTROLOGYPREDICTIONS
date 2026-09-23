import os
import shutil

root_dir = r"D:\ASTROLOGYPREDICTIONS"
artifacts_dir = r"C:\Users\User\AppData\Local\Google\AndroidStudio2026.1.4\projects\astrologypredictions.5d9a2c9\.artifacts\b018ee19-086f-4a2c-b91d-e24cb2dc90f4"

for fname in ["SYSTEM_AUDIT_ARCHITECTURAL_REVIEW_REPORT.pdf", "SYSTEM_AUDIT_ARCHITECTURAL_REVIEW_REPORT.md"]:
    art_path = os.path.join(artifacts_dir, fname)
    root_path = os.path.join(root_dir, fname)
    if os.path.exists(art_path):
        shutil.copy2(art_path, root_path)
        print(f"  ✅ Copied {fname} ({os.path.getsize(root_path)} bytes) to root directory: {root_path}")
