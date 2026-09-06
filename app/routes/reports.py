import csv, io
from flask import Blueprint, Response
from flask_login import login_required
from app.models.models import Donor, BloodRequest, Inventory
reports_bp=Blueprint("reports",__name__)

@reports_bp.get("/donors.csv")
@login_required
def donors_csv():
    out=io.StringIO(); w=csv.writer(out)
    w.writerow(["Name","Blood Group","Age","Weight","City","Eligible"])
    for d in Donor.query.all(): w.writerow([d.name,d.blood_group,d.age,d.weight,d.city,d.eligible()])
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=donors.csv"})

@reports_bp.get("/summary.csv")
@login_required
def summary_csv():
    out=io.StringIO(); w=csv.writer(out); w.writerow(["Metric","Value"])
    w.writerow(["Donors",Donor.query.count()]); w.writerow(["Requests",BloodRequest.query.count()])
    w.writerow(["Inventory Units",sum(i.units for i in Inventory.query.all())])
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=summary.csv"})
