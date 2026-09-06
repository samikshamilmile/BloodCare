from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import Inventory, Notification
from app.services.audit import log_action
inventory_bp=Blueprint("inventory",__name__)

@inventory_bp.get("/")
@login_required
def list_inventory():
    rows=Inventory.query.order_by(Inventory.blood_group).all()
    return render_template("inventory.html", inventory=rows, today=date.today())

@inventory_bp.route("/add", methods=["GET","POST"])
@login_required
def add_inventory():
    if current_user.role not in ("admin","staff"):
        flash("Staff or admin access required.","danger"); return redirect(url_for("inventory.list_inventory"))
    if request.method=="POST":
        expiry=date.fromisoformat(request.form["expiry_date"]) if request.form.get("expiry_date") else None
        x=Inventory(blood_group=request.form["blood_group"],component=request.form["component"],
                    units=int(request.form["units"]),expiry_date=expiry,batch_code=request.form.get("batch_code",""))
        db.session.add(x)
        if x.units <= 3:
            db.session.add(Notification(title="Low Blood Stock",message=f"{x.blood_group} stock is low.",level="warning"))
        log_action(current_user.username,f"Added inventory {x.blood_group} {x.units} units")
        db.session.commit()
        return redirect(url_for("inventory.list_inventory"))
    return render_template("inventory_form.html")
