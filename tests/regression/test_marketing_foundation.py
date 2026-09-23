import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_marketing_welcome_page(client):
    res = client.get("/welcome")
    assert res.status_code == 200
    assert b"Astro Predictions" in res.data
    assert b"Vedic Astrology Intelligence" in res.data

def test_marketing_robots_txt(client):
    res = client.get("/robots.txt")
    assert res.status_code == 200
    assert b"Sitemap:" in res.data

def test_marketing_sitemap_xml(client):
    res = client.get("/sitemap.xml")
    assert res.status_code == 200
    assert b"urlset" in res.data
    assert b"vedic-astrology" in res.data

def test_marketing_birth_chart_funnel(client):
    res = client.get("/birth-chart")
    assert res.status_code == 200
    assert b"Free Vedic Birth Chart Generator" in res.data

def test_marketing_seo_page(client):
    res = client.get("/vedic-astrology")
    assert res.status_code == 200
    assert b"Vedic Astrology" in res.data

def test_marketing_download_page(client):
    res = client.get("/download")
    assert res.status_code == 200
    assert b"Download Astro Predictions App" in res.data

def test_marketing_privacy_page(client):
    res = client.get("/privacy")
    assert res.status_code == 200
    assert b"Privacy Policy" in res.data

def test_marketing_share_card(client):
    res = client.get("/share/testtoken123")
    assert res.status_code == 200
    assert b"Astro Predictions" in res.data

def test_protected_v315_hashes():
    import hashlib
    baselines = {
        'app/astrology/core/chart.py': '3875b891f1c2cd058f9859bd7c43f0be42c0ae40b346b8fdf826a336448103e5',
        'app/astrology/core/swe_proxy.py': 'a6584a3216853fdd8685dc2ce7e71091e9443818a969b56f01945af9603b1bf1',
        'app/astrology/core/ephemeris.py': 'a2a56bb7f277a061583fb39c73d9e534df212b5d70e7ba2704bbb4c17a2b3c6a'
    }
    for path, base_h in baselines.items():
        with open(path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        assert h == base_h
