import subprocess
import time
import sys
import os
import http.client

def check_health(host, port):
    """Check if the service is up using standard library."""
    try:
        conn = http.client.HTTPConnection(host, port)
        conn.request("GET", "/health")
        resp = conn.getresponse()
        return resp.status == 200
    except:
        return False

def main():
    print("=" * 60)
    print("🌟 ASTRO PREDICTIONS — V3.15 CONTROLLED BETA")
    print("=" * 60)

    # 1. Database Migration (Safety Check)
    print("\n[1/3] Verifying Database Schema...")
    subprocess.run([sys.executable, "scripts/v315_migrate_db.py"])

    # 2. Start Calculation Service
    print("\n[2/3] Starting Calculation Engine (Port 8000)...")
    # We use PYTHONPATH to ensure the service can find its app
    calc_env = os.environ.copy()
    calc_env["PYTHONPATH"] = os.path.join(os.getcwd(), "calculation_service")

    calc_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="calculation_service",
        env=calc_env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for readiness
    print("      Waiting for engine to warm up...")
    ready = False
    for _ in range(15):
        if check_health("localhost", 8000):
            ready = True
            break
        time.sleep(1)

    if not ready:
        print("❌ ERROR: Calculation Engine failed to start on port 8000.")
        calc_proc.terminate()
        return

    print("✅ Calculation Engine is ONLINE.")

    # 3. Start Dashboard
    print("\n[3/3] Starting Jyotish Dashboard (Port 5001)...")
    print("-" * 60)
    print("👉 Dashboard will automatically open in your browser.")
    print("👉 Beta Participants: Use the 'Enroll' option in Settings or call /beta/enroll.")
    print("-" * 60)

    try:
        # Launch run.py which will open the browser
        subprocess.run([sys.executable, "run.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 SHUTTING DOWN...")
    finally:
        calc_proc.terminate()
        print("👋 All services stopped safely.")

if __name__ == "__main__":
    main()
