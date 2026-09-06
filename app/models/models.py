from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="viewer")
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(80), default="Nagpur")
    phone = db.Column(db.String(30), default="")
    email = db.Column(db.String(120), default="")
    available = db.Column(db.Boolean, default=True)
    last_donation = db.Column(db.Date, nullable=True)
    medical_restriction = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def eligible(self):
        if not self.available or self.medical_restriction:
            return False
        if self.age < 18 or self.age > 65 or self.weight < 50:
            return False
        if self.last_donation and (date.today() - self.last_donation).days < 90:
            return False
        return True

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey("donor.id"), nullable=False)
    donation_date = db.Column(db.Date, default=date.today)
    units = db.Column(db.Integer, default=1)
    component = db.Column(db.String(40), default="Whole Blood")
    notes = db.Column(db.String(300), default="")

class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(120), nullable=False)
    hospital = db.Column(db.String(160), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    units = db.Column(db.Integer, default=1)
    priority = db.Column(db.String(20), default="Normal")
    status = db.Column(db.String(30), default="Pending")
    contact = db.Column(db.String(30), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(5), nullable=False)
    component = db.Column(db.String(40), default="Whole Blood")
    units = db.Column(db.Integer, default=0)
    expiry_date = db.Column(db.Date, nullable=True)
    batch_code = db.Column(db.String(50), default="")

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    level = db.Column(db.String(20), default="info")
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), default="")
    action = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
