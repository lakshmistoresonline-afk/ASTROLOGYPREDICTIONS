import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

def verify_login_html():
    app = create_app()
    client = app.test_client()

    response = client.get("/login")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    html = response.get_data(as_text=True)

    print("================================================================================")
    print("🔍 VERIFYING RENDERED /login HTML FROM RUNTIME ENGINE")
    print("================================================================================")

    # Check forbidden strings
    forbidden = [
        "Sign in as Standard Tester",
        "Sign in as Administrator",
        "Developer Preview Login",
        "Standard security protocols bypassed",
        "app-sidebar",
        "app-header"
    ]

    for f in forbidden:
        if f in html:
            print(f"   ❌ FORBIDDEN STRING FOUND: '{f}'")
            return False
        else:
            print(f"   ✅ ABSENT (CLEAN): '{f}'")

    # Check required strings
    required = [
        "ASTRO PREDICTIONS",
        "Dark Celestial AI",
        "Secure Sign In",
        "Secure access to your astrology workspace",
        "emailInput",
        "passwordInput",
        "Continue / Sign In"
    ]

    for r in required:
        if r not in html:
            print(f"   ❌ REQUIRED STRING MISSING: '{r}'")
            return False
        else:
            print(f"   ✅ PRESENT: '{r}'")

    print("================================================================================")
    print("🎯 PRODUCTION LOGIN UI VERIFICATION PASSED PERFECTLY (100% PARITY)")
    print("================================================================================")
    return True

if __name__ == "__main__":
    verify_login_html()
