import os

root_dir = r"D:\ASTROLOGYPREDICTIONS"

files = [
    "MAHATMA_GANDHI_V4_INTELLIGENCE_REPORT.md",
    "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.pdf",
    "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.md",
    "SYSTEM_AUDIT_ARCHITECTURAL_REVIEW_REPORT.pdf",
    "SYSTEM_AUDIT_ARCHITECTURAL_REVIEW_REPORT.md"
]

print(f"VERIFYING ALL REPORT FILES IN ROOT DIRECTORY ({root_dir}):")
for f in files:
    fp = os.path.join(root_dir, f)
    exists = os.path.exists(fp)
    sz = os.path.getsize(fp) if exists else 0
    print(f"  [{'EXISTS' if exists else 'MISSING'}] {f} ({sz} bytes)")
