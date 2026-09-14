from datetime import datetime

from app.extensions import db


class Customers(db.Model):
    customerId = db.Column(db.Integer, primary_key=True)
    customerFName = db.Column(db.String(100), nullable=False)
    customerLName = db.Column(db.String(100), nullable=False)
    customerMName = db.Column(db.String(100))
    customerOName = db.Column(db.String(100))
    customerAddress = db.Column(db.String(250))
    customerEmail = db.Column(db.String(150))
    customerPhone = db.Column(db.String(30))
    # Loyalty points balance (see the CustomerLoyalty model for tier definitions).
    customerLoyalty = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)
