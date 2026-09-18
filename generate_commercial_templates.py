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

# Checkout (Admin UPI / QR)
with open('app/templates/commercial/checkout.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure UPI Checkout — Astro Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 20px; padding: 40px; color: #fff; max-width: 600px; margin: 40px auto; }
        .btn-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #0b091a; font-weight: bold; border-radius: 30px; padding: 12px 30px; border: none; width: 100%; }
        .qr-box { background: #fff; padding: 20px; border-radius: 10px; display: inline-block; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container py-4">
        <div class="card-custom shadow-lg">
            <h2 class="h4 fw-bold mb-3 text-warning">Complete UPI Payment</h2>
            <p class="text-muted mb-2">Product: <strong>{{ product_id }}</strong></p>
            <h3 class="fw-bold mb-4 text-warning">Amount: ₹{{ amount }}</h3>

            <div class="text-center mb-4">
                <p class="mb-1 text-muted">Scan QR or pay via UPI ID:</p>
                <div class="bg-dark p-3 rounded border border-warning text-warning fw-bold fs-5 mb-2">
                    {{ settings.upi_id }}
                </div>
                <p class="small text-muted">Payee: {{ settings.payee_name }}</p>
                {% if settings.qr_code_url %}
                <div class="qr-box">
                    <img src="{{ settings.qr_code_url }}" alt="UPI QR Code" style="max-width: 180px;">
                </div>
                {% endif %}
                <p class="small text-muted mt-2">{{ settings.instructions }}</p>
            </div>

            <hr class="border-secondary my-4">

            <form action="/payment/submit-proof" method="POST">
                <input type="hidden" name="order_id" value="{{ order.id }}">
                <div class="mb-3">
                    <label class="form-label text-muted">Enter UTR / Transaction Reference Number</label>
                    <input type="text" name="utr_number" class="form-control bg-dark text-light border-secondary" required placeholder="e.g. 325419827361">
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn btn-gold">I Have Paid — Submit UTR for Verification</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
''')

# Under Review / Payment Submitted
with open('app/templates/commercial/under_review.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Under Review — Astro Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 20px; padding: 40px; text-align: center; max-width: 500px; width: 100%; }
        .btn-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #0b091a; font-weight: bold; border-radius: 30px; padding: 12px 30px; border: none; }
    </style>
</head>
<body>
    <div class="card-custom">
        <i class="fas fa-clock text-warning fa-3x mb-3"></i>
        <h1 class="h3 fw-bold mb-3">Payment Submitted!</h1>
        <p class="text-muted mb-2">Order ID: <strong>#{{ order_id }}</strong></p>
        <p class="text-muted mb-4">UTR Reference: <strong>{{ utr }}</strong></p>
        <p class="small text-muted mb-4">Your payment is currently under review by our administrator. Entitlements will be activated immediately upon verification.</p>
        <a href="/dashboard" class="btn btn-gold">Return to Dashboard</a>
    </div>
</body>
</html>
''')

# Admin Payments Queue & Settings
with open('app/templates/commercial/admin_payments.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Payment Verification — Astro Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: #0b091a; color: #f1f1f1; font-family: 'Segoe UI', sans-serif; }
        .card-custom { background: #15102a; border: 1px solid #2d2254; border-radius: 15px; padding: 25px; color: #fff; }
    </style>
</head>
<body>
    <div class="container py-5">
        <h1 class="h3 fw-bold text-warning mb-4"><i class="fas fa-receipt me-2"></i>Admin Payment Verification & UPI Settings</h1>

        <div class="card-custom mb-5">
            <h4 class="text-warning mb-3">Configure UPI / QR Settings</h4>
            <form action="/admin/payments/settings" method="POST">
                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label text-muted">UPI ID</label>
                        <input type="text" name="upi_id" class="form-control bg-dark text-light border-secondary" value="{{ settings.upi_id }}" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Payee Name</label>
                        <input type="text" name="payee_name" class="form-control bg-dark text-light border-secondary" value="{{ settings.payee_name }}" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">QR Code Image URL</label>
                        <input type="text" name="qr_code_url" class="form-control bg-dark text-light border-secondary" value="{{ settings.qr_code_url }}">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Active Status</label>
                        <div class="form-check mt-2">
                            <input class="form-check-input" type="checkbox" name="is_active" id="isActive" {% if settings.is_active %}checked{% endif %}>
                            <label class="form-check-label text-light" for="isActive">Accepting UPI Payments</label>
                        </div>
                    </div>
                    <div class="col-12">
                        <label class="form-label text-muted">Instructions</label>
                        <textarea name="instructions" class="form-control bg-dark text-light border-secondary" rows="2">{{ settings.instructions }}</textarea>
                    </div>
                </div>
                <button type="submit" class="btn btn-warning mt-3 px-4 fw-bold">Save Payment Settings</button>
            </form>
        </div>

        <h3 class="h4 text-warning mb-3">Pending Payment Verifications</h3>
        {% if pending_orders %}
        <div class="table-responsive">
            <table class="table table-dark table-striped border border-secondary">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>User ID</th>
                        <th>Product</th>
                        <th>Amount</th>
                        <th>UTR / Ref</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for o in pending_orders %}
                    <tr>
                        <td>#{{ o.id }}</td>
                        <td>{{ o.user_id }}</td>
                        <td>{{ o.product_id }}</td>
                        <td>₹{{ o.amount }}</td>
                        <td><strong class="text-warning">{{ o.utr_number }}</strong></td>
                        <td>
                            <form action="/admin/payments/approve/{{ o.id }}" method="POST" class="d-inline">
                                <button type="submit" class="btn btn-success btn-sm">Approve</button>
                            </form>
                            <form action="/admin/payments/reject/{{ o.id }}" method="POST" class="d-inline ms-1">
                                <button type="submit" class="btn btn-danger btn-sm">Reject</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <p class="text-muted">No pending payment verifications.</p>
        {% endif %}
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
        <div class="text-end">
            <a href="/admin/payments" class="btn btn-warning fw-bold">Manage Payment Verifications & UPI</a>
        </div>
    </div>
</body>
</html>
''')

print('Commercial production hardening templates generated successfully.')
