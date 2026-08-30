import os
from app import create_app
from flask import url_for

def test():
    os.environ["FLASK_SECRET_KEY"] = "test-secret"
    app = create_app()
    with app.test_request_context():
        endpoints = [
            'main.index', 'main.dashboard', 'main.prashna',
            'main.kundli', 'main.varshaphala', 'main.transit',
            'main.admin_quality'
        ]
        for endpoint in endpoints:
            try:
                print(f"{endpoint}: {url_for(endpoint)}")
            except Exception as e:
                print(f"FAILED {endpoint}: {e}")

if __name__ == "__main__":
    test()
