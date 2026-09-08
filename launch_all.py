import subprocess
import time
import os
import sys
import signal

# TradeMind Jyotish AI - Unified Services Launcher
# Manages Calculation Service (8000) and Main Application (5001)

def launch():
    root = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(root, "venv", "Scripts", "python.exe")

    # Fallback if venv not found in standard path
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    print("="*60)
    print("🚀 ASTRO PREDICTIONS - STARTING ECOSYSTEM")
    print("="*60)

    # 1. Start Calculation Service (Uvicorn)
    print("\n[1/2] Starting Calculation Service (Port 8000)...")
    calc_proc = subprocess.Popen(
        [venv_python, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--app-dir", "calculation_service"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Wait for Calculation Service to be healthy
    time.sleep(5)

    # 2. Start Main Application (Flask)
    print("[2/2] Starting Main Dashboard (Port 5001)...")
    app_env = os.environ.copy()
    app_env["PYTHONPATH"] = root
    # Ensure Calculation Service URL is set for the client
    app_env["CALC_SERVICE_URL"] = "http://127.0.0.1:8000"

    app_proc = subprocess.Popen(
        [venv_python, "run.py"],
        cwd=root,
        env=app_env
    )

    print("\n" + "═"*60)
    print("✅ SYSTEM OPERATIONAL")
    print("═"*60)
    print("🔗 User Dashboard: http://localhost:5001")
    print("🔗 Showcase Mode:  http://localhost:5001/showcase")
    print("🔗 Admin Accuracy:  http://localhost:5001/admin/accuracy")
    print("═"*60)
    print("\nPress Ctrl+C to terminate all services.")

    try:
        # Keep the script running while the app is alive
        app_proc.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Astro Predictions ecosystem...")
        calc_proc.terminate()
        app_proc.terminate()
        print("👋 Services stopped.")

if __name__ == "__main__":
    launch()
