from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import BloodRequest, Donor, Notification
from app.services.matching import match_donors
from app.services.audit import log_action
requests_bp=Blueprint("requests",__name__)

@requests_bp.get("/")
@login_required
def list_requests():
    return render_template("requests.html", requests=BloodRequest.query.order_by(BloodRequest.created_at.desc()).all())

@requests_bp.route("/add", methods=["GET","POST"])
@login_required
def add_request():
    if request.method=="POST":
        r=BloodRequest(patient=request.form["patient"],hospital=request.form["hospital"],
            blood_group=request.form["blood_group"],units=int(request.form["units"]),
            priority=request.form["priority"],contact=request.form.get("contact",""))
        db.session.add(r)
        if r.priority=="Critical":
            db.session.add(Notification(title="Critical Blood Request",message=f"{r.blood_group} needed at {r.hospital}",level="danger"))
        log_action(current_user.username,f"Created blood request for {r.blood_group}")
        db.session.commit()
        return redirect(url_for("requests.list_requests"))
    return render_template("request_form.html")

@requests_bp.get("/<int:req_id>/matches")
@login_required
def matches(req_id):
    r=BloodRequest.query.get_or_404(req_id)
    rows=match_donors(Donor.query.all(),r.blood_group,r.hospital)
    return render_template("matches.html", req=r, results=rows)
