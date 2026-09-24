import pytest
import os

def test_dark_celestial_ui_layout_files_exist():
    files = [
        "frontend/src/components/layout/Sidebar.tsx",
        "frontend/src/components/layout/Header.tsx",
        "frontend/src/components/layout/DashboardLayout.tsx",
        "frontend/src/pages/Landing.tsx",
        "frontend/src/pages/Dashboard.tsx",
        "frontend/src/pages/Login.tsx",
        "frontend/src/pages/ProfileNew.tsx"
    ]

    for f in files:
        full_path = os.path.abspath(f)
        assert os.path.exists(full_path), f"File {f} is missing!"
        assert os.path.getsize(full_path) > 100, f"File {f} is empty or incomplete!"

def test_sidebar_component_content():
    with open("frontend/src/components/layout/Sidebar.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const Sidebar" in content
    assert "ASTRO PREDICTIONS" in content
    assert "DARK CELESTIAL AI" in content
    assert "Dashboard" in content
    assert "Export PDF Report" in content

def test_header_component_content():
    with open("frontend/src/components/layout/Header.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const Header" in content
    assert "TRANSIT FOCUS" in content
    assert "Search domains" in content

def test_dashboard_layout_content():
    with open("frontend/src/components/layout/DashboardLayout.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const DashboardLayout" in content
    assert "Sidebar" in content
    assert "Header" in content

def test_login_page_content():
    with open("frontend/src/pages/Login.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const Login" in content
    assert "Continue / Sign In" in content

def test_profile_new_page_content():
    with open("frontend/src/pages/ProfileNew.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const ProfileNew" in content
    assert "Quick City Preset" in content
    assert "COMPUTE CANONICAL CHART" in content
