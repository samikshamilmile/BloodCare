from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import Donor
from app.services.audit import log_action
from app.services.eligibility import eligibility_reasons

donors_bp = Blueprint("donors", __name__)

@donors_bp.get("/")
@login_required
def list_donors():
    q = request.args.get("q","").strip()
    bg = request.args.get("blood_group","").strip()
    query = Donor.query
    if q: query = query.filter(Donor.name.ilike(f"%{q}%"))
    if bg: query = query.filter_by(blood_group=bg)
    return render_template("donors.html", donors=query.order_by(Donor.name).all(), q=q, bg=bg)

@donors_bp.route("/add", methods=["GET","POST"])
@login_required
def add_donor():
    if current_user.role not in ("admin","staff"):
        flash("Staff or admin access required.","danger"); return redirect(url_for("donors.list_donors"))
    if request.method == "POST":
        d=Donor(name=request.form["name"], blood_group=request.form["blood_group"],
                age=int(request.form["age"]), weight=float(request.form["weight"]),
                city=request.form.get("city",""), phone=request.form.get("phone",""),
                email=request.form.get("email",""))
        db.session.add(d); log_action(current_user.username, f"Added donor {d.name}"); db.session.commit()
        flash("Donor added successfully.","success"); return redirect(url_for("donors.list_donors"))
    return render_template("donor_form.html")

@donors_bp.get("/<int:donor_id>")
@login_required
def profile(donor_id):
    d=Donor.query.get_or_404(donor_id)
    return render_template("donor_profile.html", donor=d, reasons=eligibility_reasons(d))
