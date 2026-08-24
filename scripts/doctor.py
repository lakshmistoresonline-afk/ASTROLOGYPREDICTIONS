import os
import sys
import subprocess
from pathlib import Path

def run_doctor():
    print("=" * 60)
    print("🏥 ASTROLOGYPREDICTIONS - SUPREME DOCTOR")
    print("=" * 60)

    # 1. Python Version Check
    print(f"\n[1/4] Checking Python: {sys.version.split()[0]}")
    if sys.version_info >= (3, 13):
        print("  ⚠ Python 3.13 detected. Many astrology libraries require C++ compilation on this version.")

    # 2. Dependency Check
    print("\n[2/4] Checking Dependencies...")
    required = ["pytz", "flask", "pydantic", "swisseph", "numpy"]
    missing = []

    for lib in required:
        try:
            __import__(lib)
            print(f"  ✅ {lib}: Installed")
        except ImportError:
            missing.append(lib)
            print(f"  ❌ {lib}: MISSING")

    # 3. Fix Missing
    if missing:
        print("\n[3/4] Attempting automatic repair...")
        for lib in missing:
            pkg = "pyswisseph" if lib == "swisseph" else lib
            print(f"  -> Installing {pkg}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                print(f"  ✅ {pkg} installed successfully.")
            except subprocess.CalledProcessError:
                print(f"  ❌ {pkg} failed to install.")
                if pkg == "pyswisseph":
                    print("\n" + "!" * 60)
                    print("CRITICAL: C++ BUILD TOOLS REQUIRED")
                    print("pyswisseph requires a C++ compiler to build the Swiss Ephemeris.")
                    print("Solution: Download and install 'Visual Studio C++ Build Tools'")
                    print("Link: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
                    print("!" * 60 + "\n")

    # 4. Ephemeris Files
    print("\n[4/4] Checking Ephemeris Data...")
    ephe_path = Path(__file__).parent.parent / "ephe"
    if not ephe_path.exists():
        print("  ❌ 'ephe' directory missing.")
    else:
        files = list(ephe_path.glob("*.se1"))
        if len(files) < 3:
            print(f"  ⚠ Found only {len(files)} .se1 files. Accuracy may be low.")
        else:
            print(f"  ✅ Ephemeris data found ({len(files)} files).")

    print("\n" + "=" * 60)
    print("🩺 DOCTOR'S FINAL VERDICT:")
    if not missing:
        print("🎉 SYSTEM STABILIZED: You are ready to run 'python run.py'")
    else:
        print("🛠️ ACTION REQUIRED: Please install the missing components listed above.")
    print("=" * 60)

if __name__ == "__main__":
    run_doctor()
