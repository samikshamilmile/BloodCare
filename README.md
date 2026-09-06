# BloodCare – Complete Smart Blood Donor Management System

## Included features
- Flask + SQLAlchemy + SQLite
- Admin / Staff / Viewer role-based login
- Password hashing and CSRF protection
- Donor management, search and profiles
- Donor eligibility engine
- Blood-group compatibility engine
- Intelligent donor match scoring
- Emergency blood requests and critical notifications
- Donation recording and donation interval validation
- Blood inventory with batch and expiry data
- Low-stock notifications
- Dashboard KPIs
- REST-style JSON APIs
- CSV reports
- Audit logging
- Responsive modern UI with icons
- Dark-mode toggle foundation
- Seed/demo data
- Pytest tests

## Run on Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed.py
python app.py
```
Open http://127.0.0.1:5000

Demo accounts:
- admin / Admin@123
- staff / Staff@123
- viewer / Viewer@123

## Resume description
Developed a full-stack Blood Donor Management System using Python, Flask, SQLAlchemy and SQLite featuring role-based authentication, donor eligibility validation, intelligent compatibility-based matching, emergency workflows, inventory and expiry tracking, notifications, audit logging, REST APIs, CSV reporting and responsive analytics-oriented UI.
