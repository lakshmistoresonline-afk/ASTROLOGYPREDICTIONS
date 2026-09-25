import os

dup_files = [
    "frontend/src/pages/dashboard.tsx",
    "frontend/src/pages/login.tsx"
]

for f in dup_files:
    full_p = os.path.abspath(f)
    if os.path.exists(full_p):
        os.remove(full_p)
        print(f"Removed duplicate route alias file: {full_p}")
