from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.donors import donors_bp
    from app.routes.requests import requests_bp
    from app.routes.inventory import inventory_bp
    from app.routes.donations import donations_bp
    from app.routes.reports import reports_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(donors_bp, url_prefix="/donors")
    app.register_blueprint(requests_bp, url_prefix="/requests")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(donations_bp, url_prefix="/donations")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        from app.models.models import User, Donor, BloodRequest, Inventory, Donation, Notification, AuditLog
        db.create_all()

    return app
