from app import db
from datetime import datetime
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(150),nullable=False)
    role=db.Column(db.String(50),nullable=False)

class Company_profile(db.Model):
    __tablename__='company_profile'
    company_id=db.Column(db.Integer,db.ForeignKey('User.id'),primary_key=True)
    company_name=db.Column(db.String(150),unique=True,nullable=False)
    hr_contact=db.Column(db.Integer,unique=True)
    website=db.Column(db.String(150),unique=True)
    app_status=db.Column(db.String(50),default='Pending')

class Placement_drive(db.Model):
    __tablename__='placement_drive'
    drive_id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey('Company_profile.company_id'),nullable=False)
    job_title=db.Column(db.String(150),nullable=False)
    job_description=db.Column(db.Text,nullable=True)
    eligibility=db.Column(db.Text,nullable=True)
    app_deadline=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(50),default='Pending')

class Application(db.Model):
    __tablename__='application'
    app_id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey('Placement_drive.drive_id'),nullable=False)
    app_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(50),default='Applied')