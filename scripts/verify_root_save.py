import os
import shutil

root_dir = r"D:\ASTROLOGYPREDICTIONS"
artifacts_dir = r"C:\Users\User\AppData\Local\Google\AndroidStudio2026.1.4\projects\astrologypredictions.5d9a2c9\.artifacts\b018ee19-086f-4a2c-b91d-e24cb2dc90f4"

gandhi_pdf_root = os.path.join(root_dir, "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.pdf")
gandhi_md_root = os.path.join(root_dir, "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.md")

gandhi_pdf_art = os.path.join(artifacts_dir, "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.pdf")
gandhi_md_art = os.path.join(artifacts_dir, "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.md")

# Ensure files exist in root directory
if not os.path.exists(gandhi_pdf_root) and os.path.exists(gandhi_pdf_art):
    shutil.copy2(gandhi_pdf_art, gandhi_pdf_root)

if not os.path.exists(gandhi_md_root) and os.path.exists(gandhi_md_art):
    shutil.copy2(gandhi_md_art, gandhi_md_root)

print(f"Checking root directory files in {root_dir}:")
print(f"  PDF in Root: {os.path.exists(gandhi_pdf_root)} ({os.path.getsize(gandhi_pdf_root) if os.path.exists(gandhi_pdf_root) else 0} bytes)")
print(f"  MD in Root:  {os.path.exists(gandhi_md_root)} ({os.path.getsize(gandhi_md_root) if os.path.exists(gandhi_md_root) else 0} bytes)")
