from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.models import Donor, BloodRequest, Inventory
from app.services.matching import match_donors
api_bp=Blueprint("api",__name__)

@api_bp.get("/stats")
@login_required
def stats():
    return jsonify({
        "donors":Donor.query.count(),
        "requests":BloodRequest.query.count(),
        "inventory_units":sum(i.units for i in Inventory.query.all()),
        "critical":BloodRequest.query.filter_by(priority="Critical").count()
    })

@api_bp.get("/matches/<blood_group>")
@login_required
def matches(blood_group):
    city=request.args.get("city")
    return jsonify([{"donor_id":d.id,"name":d.name,"blood_group":d.blood_group,"score":score}
                    for d,score in match_donors(Donor.query.all(),blood_group,city)])
