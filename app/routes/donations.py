from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import Donation, Donor
from app.services.audit import log_action
donations_bp=Blueprint("donations",__name__)

@donations_bp.route("/",methods=["GET","POST"])
@login_required
def donations():
    if request.method=="POST":
        d=Donation(donor_id=int(request.form["donor_id"]),donation_date=date.fromisoformat(request.form["donation_date"]),
                   units=int(request.form["units"]),component=request.form["component"],notes=request.form.get("notes",""))
        donor=Donor.query.get_or_404(d.donor_id)
        if not donor.eligible():
            flash("Donor is not currently eligible.","danger")
            return redirect(url_for("donations.donations"))
        donor.last_donation=d.donation_date
        donor.available=False
        db.session.add(d); log_action(current_user.username,f"Recorded donation by {donor.name}"); db.session.commit()
        flash("Donation recorded.","success")
    return render_template("donations.html", donations=Donation.query.order_by(Donation.donation_date.desc()).all(), donors=Donor.query.all())
