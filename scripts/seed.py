from datetime import date, timedelta
from app import create_app, db
from app.models.models import User, Donor, BloodRequest, Inventory
app=create_app()
with app.app_context():
    db.drop_all(); db.create_all()
    for username,password,role in [("admin","Admin@123","admin"),("staff","Staff@123","staff"),("viewer","Viewer@123","viewer")]:
        u=User(username=username,role=role); u.set_password(password); db.session.add(u)
    donors=[
        ("Aarav Sharma","O+",24,65,"Nagpur","9000000001"),
        ("Priya Patil","B+",28,58,"Nagpur","9000000002"),
        ("Rahul Verma","O-",31,72,"Wardha","9000000003"),
        ("Sneha Joshi","A+",22,55,"Nagpur","9000000004"),
        ("Vivek Singh","AB+",35,80,"Amravati","9000000005"),
        ("Neha Gupta","B-",27,62,"Nagpur","9000000006"),
        ("Riya Kulkarni","A- ",29,60,"Nagpur","9000000007"),
        ("Karan Mehta","O+",40,76,"Nagpur","9000000008"),
    ]
    for n,b,a,w,c,p in donors:
        db.session.add(Donor(name=n,blood_group=b.strip(),age=a,weight=w,city=c,phone=p,last_donation=date.today()-timedelta(days=120)))
    for p,h,b,u,pr in [("Patient A","City Hospital","O+",2,"Critical"),("Patient B","Lifeline Hospital","B+",3,"High"),("Patient C","District Hospital","A+",1,"Normal")]:
        db.session.add(BloodRequest(patient=p,hospital=h,blood_group=b,units=u,priority=pr))
    for b,u in [("O+",18),("O-",5),("A+",12),("A-",3),("B+",10),("B-",2),("AB+",7),("AB-",2)]:
        db.session.add(Inventory(blood_group=b,units=u,component="Whole Blood",expiry_date=date.today()+timedelta(days=20),batch_code=f"BC-{b.replace('+','P').replace('-','M')}-001"))
    db.session.commit()
    print("BloodCare database seeded successfully.")
