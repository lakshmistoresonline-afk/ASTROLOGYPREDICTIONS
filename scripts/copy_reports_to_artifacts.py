import os
import shutil

artifacts_dir = r"C:\Users\User\AppData\Local\Google\AndroidStudio2026.1.4\projects\astrologypredictions.5d9a2c9\.artifacts\b018ee19-086f-4a2c-b91d-e24cb2dc90f4"
os.makedirs(artifacts_dir, exist_ok=True)

files_to_copy = [
    "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.pdf",
    "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.md",
    "SYSTEM_AUDIT_ARCHITECTURAL_REVIEW_REPORT.pdf",
    "SYSTEM_AUDIT_ARCHITECTURAL_REVIEW_REPORT.md",
    "FULL_INTELLIGENCE_REPORT_Subramanian_T_S.pdf",
    "FULL_INTELLIGENCE_REPORT_Subramanian_T_S.md"
]

print("Copying report files to artifacts directory...")
for fname in files_to_copy:
    src_path = os.path.abspath(fname)
    if os.path.exists(src_path):
        dst_path = os.path.join(artifacts_dir, fname)
        shutil.copy2(src_path, dst_path)
        sz = os.path.getsize(dst_path)
        print(f"  ✅ Copied {fname} ({sz} bytes) -> {dst_path}")
    else:
        print(f"  ⚠️ Source file not found: {src_path}")
