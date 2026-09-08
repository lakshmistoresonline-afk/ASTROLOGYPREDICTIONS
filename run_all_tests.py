import threading
import uvicorn
import time
import subprocess
import sys

def start_calc_service():
    from calculation_service.app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

if __name__ == "__main__":
    t = threading.Thread(target=start_calc_service, daemon=True)
    t.start()
    time.sleep(2)

    from app.astrology.core.calc_client import calc_client
    if not calc_client.check_health():
        print("ERROR: Calculation service failed to start.")
        sys.exit(1)
    print("Calculation service started successfully on port 8000.")

    print("\n--- Running V3.15 Integrity Regression ---")
    subprocess.run([sys.executable, "tests/v315_integrity_regression.py"], check=True)

    print("\n--- Regenerating Regression Baselines ---")
    subprocess.run([sys.executable, "tests/regression/generate_baseline.py"], check=True)

    print("\n--- Running Regression Test Suite (pytest) ---")
    res = subprocess.run([sys.executable, "-m", "pytest", "tests/regression/"])
    sys.exit(res.returncode)
