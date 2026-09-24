import hashlib
import os

protected_files = [
    "app/astrology/core/chart.py",
    "app/astrology/core/swe_proxy.py",
    "app/astrology/core/ephemeris.py"
]

print("================================================================================")
print("🔒 PROTECTED V3.15 CORE FILE SHA-256 HASH VERIFICATION")
print("================================================================================")

hashes = {}
for rel_path in protected_files:
    full_p = os.path.abspath(rel_path)
    if os.path.exists(full_p):
        with open(full_p, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
            hashes[rel_path] = h
            print(f"  {rel_path}: {h}")
    else:
        print(f"  ⚠️ MISSING: {rel_path}")

print("================================================================================")
