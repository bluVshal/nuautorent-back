from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    userId = db.Column(db.Integer, unique=True, primary_key=True)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    userPassword = db.Column(db.String(60), unique=True, nullable=False)
    lastLoginDate = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)
