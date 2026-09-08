import os
import sys

# Set up path
sys.path.append('D:/ASTROLOGYPREDICTIONS')

from app import create_app
from flask import session

app = create_app()

def generate(pid, filename):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['active_chart_id'] = pid

        r = client.get('/dashboard')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f"Generated {filename} for {pid}")

print("Starting generation...")
# We need calculation service running for this to work correctly if it hits the engine
# But if it's already calculated and cached...
# Actually, let's just try.
try:
    generate('de9427a1', 'dash_subra.html')
    generate('913637d9', 'dash_gate.html')
except Exception as e:
    print(f"Error: {e}")
