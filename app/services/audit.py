from app import db
from app.models.models import AuditLog
def log_action(username, action):
    db.session.add(AuditLog(username=username or "system", action=action))
