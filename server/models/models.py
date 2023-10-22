from ..database.db import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# authenticate teacher
class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

# teacher can add new student
class Student(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    results = db.relationship('Result', backref='student', passive_deletes=True)  

# teacher enters student id, subject, score and feedback
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), db.ForeignKey('student.name', ondelete='CASCADE'), nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(300), nullable=False)
