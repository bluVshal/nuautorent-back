from datetime import datetime

from app.extensions import db


class Booking(db.Model):
    # Business booking reference (e.g. "BKG-000123").
    bookingId = db.Column(db.String(17), primary_key=True)
    # References Cars.carId / Customers.customerId (a car/customer can appear in
    # many bookings, so these are not unique).
    carId = db.Column(db.Integer, nullable=False)
    customerId = db.Column(db.Integer, nullable=False)
    bookingPickUpDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bookingReturnDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)
