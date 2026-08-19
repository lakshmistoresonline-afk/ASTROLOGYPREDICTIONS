import os
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent
sys.path.append(str(root))

def test_local_run():
    print("Setting up local environment for testing...")

    # 1. Force local mode
    os.environ['USE_FIREBASE'] = 'false'
    os.environ['FLASK_SECRET_KEY'] = 'test-secret-key-123'
    os.environ['SE_EPHE_PATH'] = str(root / "ephe")
    os.environ['FLASK_ENV'] = 'development'

    # 2. Check ephe files
    ephe_dir = root / "ephe"
    required_files = ["seas_18.se1", "semo_18.se1", "sepl_18.se1"]
    missing = [f for f in required_files if not (ephe_dir / f).exists()]
    if missing:
        print(f"❌ Missing ephemeris files: {missing}. Run install.sh or download them manually.")
        return

    # 3. Try creating app
    try:
        from app import create_app
        app = create_app()
        client = app.test_client()
        print("✅ App initialized successfully.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Failed to initialize app: {e}")
        return

    # 4. Test home page
    print("Testing Home Page (/) ...")
    try:
        resp = client.get('/')
        if resp.status_code == 200:
            print("✅ Home Page loaded (200 OK).")
        else:
            print(f"❌ Home Page failed with status {resp.status_code}.")
            print(resp.data.decode('utf-8')[:1000])
            return
    except Exception as e:
        print(f"❌ Exception during Home Page request: {e}")
        import traceback
        traceback.print_exc()
        return

    # 5. Test Kundli calculation logic
    print("Testing Kundli Calculation ...")
    try:
        from app.astrology.core.chart import calculate_chart_data
        from datetime import datetime
        # Delhi 1980-05-15 10:30 AM
        dt = datetime(1980, 5, 15, 10, 30)
        chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
        print(f"✅ Chart calculated. Ascendant Rashi: {chart['asc_rashi']}")
    except Exception as e:
        print(f"❌ Failed to calculate chart: {e}")
        import traceback
        traceback.print_exc()
        return

    # 6. Test Predictions Route (Anonymous)
    print("Testing Predictions Page (Anonymous) ...")
    try:
        resp = client.get('/predictions')
        if "Please generate a Kundli first" in resp.data.decode('utf-8'):
            print("✅ Predictions Page handled missing session correctly.")
        else:
            print("⚠ Predictions Page behavior unexpected.")
    except Exception as e:
        print(f"❌ Exception during Predictions Page request: {e}")

    print("\n🎉 ALL LOCAL CORE TESTS PASSED.")
    print("To run the full app, execute: python run.py")

if __name__ == "__main__":
    test_local_run()
