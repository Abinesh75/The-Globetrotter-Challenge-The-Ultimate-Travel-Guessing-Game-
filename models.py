from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    clues = db.Column(db.JSON, nullable=False)
    fun_fact = db.Column(db.JSON, nullable=False)
    trivia = db.Column(db.JSON, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)
