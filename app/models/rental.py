from datetime import datetime

from app.extensions import db


class Rental(db.Model):
    rentalId = db.Column(db.Integer, primary_key=True)
    # References Cars.carId / Customers.customerId.
    carId = db.Column(db.Integer, nullable=False)
    customerId = db.Column(db.Integer, nullable=False)
    rentalPickupDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rentalReturnDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)
