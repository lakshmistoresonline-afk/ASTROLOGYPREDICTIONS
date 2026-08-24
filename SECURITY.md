# Security Policy

ASTROLOGYPREDICTIONS is designed with local-first privacy and secure deployment standards.

## 🛡️ Core Security Features

### 🔑 Mandatory Secret Enforcement
- **`FLASK_SECRET_KEY`**: The application will not start in production if this key is missing. It is used to sign session cookies and protect against CSRF.
- **API Keys**: Keys for optional geocoding (OpenCage) and timezone (TimeZoneDB) services are managed via environment variables and never committed to source control.

### 🌐 Secure Headers
In production environments, the following headers are enforced:
- **HSTS (Strict-Transport-Security)**: Forces HTTPS for a year.
- **CSP (Content-Security-Policy)**: Restricts script and style sources to 'self' and safe inlines.
- **X-Frame-Options**: Set to 'SAMEORIGIN' to prevent clickjacking.
- **X-Content-Type-Options**: Set to 'nosniff'.

### 📦 Persistence
- **Docker Volumes**: Ephemeris data (`ephe/`) and user database (`data/`) are stored in persistent volumes to prevent data loss on container restarts.
- **Encrypted Exports**: User data export/import uses standard JSON structures designed for local backup, keeping your cosmic data in your own hands.

## ⚠️ Reporting Vulnerabilities
If you discover a security vulnerability, please do not open a public issue. Instead, contact the maintainers directly.
