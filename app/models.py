from app import db

class Manager(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    staffname = db.Column(db.String(80), unique=True, nullable=False) 
    password = db.Column(db.String(120), unique=True, nullable=False) 


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffname = db.Column(db.String(80), unique=True, nullable=True) 
    email = db.Column(db.String(120), unique=True, nullable=True)


    
    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False) 
    staff = db.relationship('Staff', backref=db.backref('tasks', lazy=True))