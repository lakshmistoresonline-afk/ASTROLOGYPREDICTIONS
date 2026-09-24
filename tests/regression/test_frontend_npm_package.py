import pytest
import os
import json

def test_frontend_package_json_exists_and_valid():
    p_path = os.path.abspath("frontend/package.json")
    assert os.path.exists(p_path), "frontend/package.json is missing!"

    with open(p_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["name"] == "astrology-predictions-frontend"
    assert "next" in data["dependencies"]
    assert "react" in data["dependencies"]
    assert "tailwindcss" in data["devDependencies"]
