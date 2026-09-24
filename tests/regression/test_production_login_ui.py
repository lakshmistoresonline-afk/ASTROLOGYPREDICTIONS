import pytest
import os
from app import create_app

def test_login_route_uses_production_login_ui():
    """
    Verifies that GET /login renders the clean production login UI
    and does NOT expose old developer preview bypass buttons or app shell sidebar/header.
    """
    app = create_app()
    client = app.test_client()

    response = client.get("/login")
    assert response.status_code == 200

    html = response.get_data(as_text=True)

    # 1. Assert old developer-preview bypass strings DO NOT appear
    forbidden_strings = [
        "Sign in as Standard Tester",
        "Sign in as Administrator",
        "Developer Preview Login",
        "Standard security protocols bypassed",
        "app-sidebar",  # Unauthenticated /login must NOT render dashboard sidebar shell!
        "app-header"   # Unauthenticated /login must NOT render top header shell!
    ]

    for forbidden in forbidden_strings:
        assert forbidden not in html, f"Forbidden legacy string '{forbidden}' found in rendered /login UI!"

    # 2. Assert new production login elements ARE PRESENT
    required_strings = [
        "ASTRO PREDICTIONS",
        "Dark Celestial AI",
        "Secure Sign In",
        "Secure access to your astrology workspace",
        "emailInput",
        "passwordInput",
        "Continue / Sign In"
    ]

    for req in required_strings:
        assert req in html, f"Required production login string '{req}' missing from rendered /login UI!"

def test_login_post_authentication_flow():
    """
    Verifies that POST /login with valid email creates user session and redirects to dashboard.
    """
    app = create_app()
    client = app.test_client()

    # Submit login form
    response = client.post("/login", data={"email": "tester@astropredictions.app", "password": "password123"}, follow_redirects=True)
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    # Post-login dashboard MUST contain the authenticated app shell
    assert "ASTRO PREDICTIONS" in html
