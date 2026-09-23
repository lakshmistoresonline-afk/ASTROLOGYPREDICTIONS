import os
import shutil

root_dir = r"D:\ASTROLOGYPREDICTIONS"
artifacts_dir = r"C:\Users\User\AppData\Local\Google\AndroidStudio2026.1.4\projects\astrologypredictions.5d9a2c9\.artifacts\b018ee19-086f-4a2c-b91d-e24cb2dc90f4"

fname = "ENGINE_V5_PHASE4_DELIVERY_REPORT.md"
src = os.path.join(root_dir, fname)
dst = os.path.join(artifacts_dir, fname)

if os.path.exists(src):
    shutil.copy2(src, dst)
    print(f"  ✅ Copied {fname} ({os.path.getsize(dst)} bytes) to artifacts directory: {dst}")
