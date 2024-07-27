from .import db
from flask_login import UserMixin
from website import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    meals = db.relationship('Meal', backref='user', lazy=True)
    symptoms = db.relationship('Symptom', backref='user', lazy=True)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_name = db.Column(db.String(100), nullable=False)
    meal_datetime = db.Column(db.DateTime, nullable=False)

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptom_name = db.Column(db.String(100), nullable=False)
    symptom_datetime = db.Column(db.DateTime, nullable=False)
    severity_level = db.Column(db.Integer, nullable=False)
    
class CombinedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(100), nullable=False)
    symptom_name = db.Column(db.String(100), nullable=False)


    



