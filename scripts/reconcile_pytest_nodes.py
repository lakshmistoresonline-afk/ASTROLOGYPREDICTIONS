import subprocess
import json
import sys
import os

def collect_and_reconcile():
    print("================================================================================")
    print("🔍 RECONCILING 100% OF PYTEST COLLECTED TEST NODES")
    print("================================================================================")

    # 1. Run pytest --collect-only -q
    cmd = [r"venv\Scripts\python.exe", "-m", "pytest", "--collect-only", "-q"]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=r"D:\ASTROLOGYPREDICTIONS")

    lines = [line.strip() for line in res.stdout.splitlines() if line.strip() and "::" in line]
    print(f"  TOTAL COLLECTED TEST NODES: {len(lines)}")

    # Print out script test files collected
    script_tests = [l for l in lines if l.startswith("scripts/")]
    print(f"\n  TEST NODES IN scripts/: ({len(script_tests)} nodes)")
    for st in script_tests:
        print(f"    - {st}")

    return lines

if __name__ == "__main__":
    collect_and_reconcile()
