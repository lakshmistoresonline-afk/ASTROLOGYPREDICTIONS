import os

os.makedirs('app/templates/commercial', exist_ok=True)

# Pricing
with open('app/templates/commercial/pricing.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing & Plans — Astro Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 20px; padding: 40px; color: #fff; height: 100%; }
        .btn-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #0b091a; font-weight: bold; border-radius: 30px; padding: 12px 30px; border: none; }
        a { color: #FFD700; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container py-5 text-center">
        <h1 class="display-5 fw-bold text-warning mb-3">Simple, Transparent Pricing</h1>
        <p class="lead text-muted mb-5">Unlock full Vedic astrology intelligence and detailed timing reports.</p>
        <div class="row g-4 justify-content-center">
            <div class="col-md-5">
                <div class="card-custom">
                    <h3>Free Tier</h3>
                    <h2 class="display-6 fw-bold my-3">₹0</h2>
                    <p class="text-muted">Basic chart, Moon sign, Nakshatra, and basic Dasha overview.</p>
                    <a href="/birth-chart" class="btn btn-outline-warning w-100 rounded-pill mt-4">Get Started Free</a>
                </div>
            </div>
            <div class="col-md-5">
                <div class="card-custom border-warning">
                    <span class="badge bg-warning text-dark mb-2">Most Popular</span>
                    <h3>Astro Plus</h3>
                    <h2 class="display-6 fw-bold my-3 text-warning">₹499 <span class="fs-6 text-muted">/ month</span></h2>
                    <p class="text-muted">Full prediction domains, advanced timing, full Life Timeline & ad-free experience.</p>
                    <a href="/checkout/plus_monthly" class="btn btn-gold w-100 mt-4">Unlock Astro Plus</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
''')

# Checkout
with open('app/templates/commercial/checkout.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Checkout — Astro Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 20px; padding: 40px; color: #fff; max-width: 500px; margin: 80px auto; }
        .btn-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #0b091a; font-weight: bold; border-radius: 30px; padding: 12px 30px; border: none; width: 100%; }
    </style>
</head>
<body>
    <div class="card-custom">
        <h2 class="h4 fw-bold mb-3 text-warning">Secure Checkout</h2>
        <p class="text-muted mb-4">Product: <strong>{{ product_id }}</strong></p>
        <h3 class="fw-bold mb-4">₹{{ amount }}</h3>
        <form action="/payment/success" method="GET">
            <input type="hidden" name="order_id" value="{{ order.provider_order_id }}">
            <button type="submit" class="btn btn-gold">Simulate Secure Payment & Activate</button>
        </form>
    </div>
</body>
</html>
''')

# Success
with open('app/templates/commercial/success.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Successful — Astro Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 20px; padding: 40px; text-align: center; max-width: 500px; width: 100%; }
        .btn-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #0b091a; font-weight: bold; border-radius: 30px; padding: 12px 30px; border: none; }
    </style>
</head>
<body>
    <div class="card-custom">
        <i class="fas fa-check-circle text-warning fa-3x mb-3"></i>
        <h1 class="h3 fw-bold mb-3">Payment Successful!</h1>
        <p class="text-muted mb-4">Your subscription / entitlement has been activated successfully.</p>
        <a href="/dashboard" class="btn btn-gold">Go to Dashboard</a>
    </div>
</body>
</html>
''')

# Admin Business Dashboard
with open('app/templates/commercial/admin_business.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Analytics — Astro Predictions Admin</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 15px; padding: 25px; color: #fff; }
    </style>
</head>
<body>
    <div class="container py-5">
        <h1 class="h3 fw-bold text-warning mb-4"><i class="fas fa-chart-line me-2"></i>Business & Revenue Analytics</h1>
        <div class="row g-4 mb-5">
            <div class="col-md-6">
                <div class="card-custom">
                    <h5 class="text-muted">Total Revenue</h5>
                    <h2 class="fw-bold text-warning">₹{{ total_revenue }}</h2>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card-custom">
                    <h5 class="text-muted">Active Subscriptions</h5>
                    <h2 class="fw-bold text-success">{{ active_subs }}</h2>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
''')

print('Commercial templates generated successfully.')
