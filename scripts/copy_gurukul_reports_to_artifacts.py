import os
import shutil

root_dir = r"D:\ASTROLOGYPREDICTIONS"
artifacts_dir = r"C:\Users\User\AppData\Local\Google\AndroidStudio2026.1.4\projects\astrologypredictions.5d9a2c9\.artifacts\b018ee19-086f-4a2c-b91d-e24cb2dc90f4"
os.makedirs(artifacts_dir, exist_ok=True)

report_files = [
    "GURUKUL_HINDI_CHAPTER1_CONTENT_TRACE.md",
    "GURUKUL_HINDI_CHAPTER1_MISSING_RECORDS.md",
    "GURUKUL_HINDI_SOURCE_TO_UI_MATRIX.md",
    "GURUKUL_HINDI_DATA_COVERAGE_REPORT.md",
    "GURUKUL_HINDI_IMPLEMENTATION_REPORT.md"
]

for fname in report_files:
    src_p = os.path.join(root_dir, fname)
    dst_p = os.path.join(artifacts_dir, fname)
    if os.path.exists(src_p):
        shutil.copy2(src_p, dst_p)
        print(f"  ✅ Copied {fname} ({os.path.getsize(dst_p)} bytes) -> {dst_p}")
