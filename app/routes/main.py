from flask import Blueprint, render_template
from flask_login import login_required
from app.models.models import Donor, BloodRequest, Inventory, Notification
main_bp = Blueprint("main", __name__)

@main_bp.get("/")
@login_required
def dashboard():
    inventory = Inventory.query.all()
    return render_template("dashboard.html",
        donors=Donor.query.count(),
        requests=BloodRequest.query.count(),
        units=sum(i.units for i in inventory),
        urgent=BloodRequest.query.filter_by(priority="Critical").count(),
        unread=Notification.query.filter_by(read=False).count())
