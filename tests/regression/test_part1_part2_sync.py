import pytest
import os
from datetime import datetime
from app import create_app
from scripts.build_and_sync_frontend import build_and_sync

def test_part1_part2_sync_build_and_routes():
    # 1. Test build and sync script
    sync_success = build_and_sync()
    assert sync_success is True

    # 2. Test Flask app root route '/' serves dashboard
    app = create_app()
    client = app.test_client()

    with client:
        # Test / route returns 200 or 302 (redirect to login or load dashboard)
        response = client.get("/")
        assert response.status_code in [200, 302]

def test_part1_layout_styling_tokens():
    layout_p = os.path.abspath("frontend/src/components/layout/DashboardLayout.tsx")
    assert os.path.exists(layout_p)

    with open(layout_p, "r", encoding="utf-8") as f:
        content = f.read()

    assert "#0B0F19" in content
    assert "radial-gradient" in content
    assert "max-w-7xl" in content
