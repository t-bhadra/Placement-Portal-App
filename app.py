from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request,redirect,url_for,session
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
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/registration',methods=["POST","GET"])
    def registration():
        if request.method=="POST":
            username=request.form['username']
            email=request.form['email']
            password=request.form['password']
            role=request.form['role']
            user=User.query.filter_by(username=username,email=email).first()
            if user:
                return redirect(url_for('login'))
            new_user=User(username=username,email=email,password=password,role=role)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('registration.html')
    
    @app.route('/login',methods=["POST","GET"])
    def login():
        if request.method=="POST":
            username=request.form['username']
            password=request.form['password']
            user=User.query.filter_by(username=username,password=password).first()
            if user and user.role=="student":
                return redirect(url_for('student_dashboard'))
            elif user and user.role=="company":
                return redirect(url_for('company_dashboard'))
            elif user and user.role=="admin":
                return redirect(url_for('admin_dashboard'))
            return render_template('registration.html',error_message="You are new user. Please register yourself")
        return render_template('login.html')
    
    @app.route('/company_dashboard')
    def company_dashboard():
        return render_template('company_dashboard.html')
    
    @app.route('/student_dashboard')
    def student_dashboard():
        return render_template('student_dashboard.html')
    
    @app.route('/admin_dashboard')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        existing_admin=User.query.filter_by(role="admin").first()
        if not existing_admin:
            admin_db=User(username="admin",password="admin",email="trisha@gmail.com",role="admin")
            db.session.add(admin_db)
            db.session.commit()
    app.run(debug=True)