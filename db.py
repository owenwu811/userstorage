from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id, username, password = db.Column(db.Integer, primary_key=True), db.Column(db.String(80), unique=True, nullable=False), db.Column(db.String(120), nullable=False)
