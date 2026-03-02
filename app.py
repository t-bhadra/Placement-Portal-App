from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(150),nullable=False)
    role=db.Column(db.String(50),nullable=False)

class Company_profile(db.Model):
    __tablename__='company_profile'
    company_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    company_name=db.Column(db.String(150),unique=True,nullable=False)
    hr_contact=db.Column(db.Integer,unique=True)
    website=db.Column(db.String(150),unique=True)
    app_status=db.Column(db.String(50),default='Pending')

class Placement_drive(db.Model):
    __tablename__='placement_drive'
    drive_id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey('company_profile.company_id'),nullable=False)
    job_title=db.Column(db.String(150),nullable=False)
    job_description=db.Column(db.Text,nullable=True)
    eligibility=db.Column(db.Text,nullable=True)
    app_deadline=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(50),default='Pending')

class Application(db.Model):
    __tablename__='application'
    app_id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey('placement_drive.drive_id'),nullable=False)
    app_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(50),default='Applied')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        existing_admin=User.query.filter_by(role="admin").first()
        if not existing_admin:
            admin_db=User(username="admin",password="admin",email="trisha@gmail.com",role="admin")
            db.session.add(admin_db)
            db.session.commit()
    app.run(debug=True)