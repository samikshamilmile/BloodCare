from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.models import User, AuditLog, Notification
admin_bp=Blueprint("admin",__name__)

def admin_only():
    return current_user.is_authenticated and current_user.role=="admin"

@admin_bp.get("/")
@login_required
def index():
    if not admin_only(): return "Forbidden",403
    return render_template("admin.html",users=User.query.all(),logs=AuditLog.query.order_by(AuditLog.created_at.desc()).limit(50).all(),
                           notifications=Notification.query.order_by(Notification.created_at.desc()).limit(20).all())
