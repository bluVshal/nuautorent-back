from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Cars(db.Model):
    bookingId = db.Column(db.String(17), unique=True, nullable=False)
    carId = db.Column(db.Integer, unique=True)
    customerId = db.Column(db.Integer, nullable=False)
    bookingPickUpDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bookingReturnDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)

