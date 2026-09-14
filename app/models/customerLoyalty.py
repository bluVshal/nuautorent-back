from datetime import datetime

from app.extensions import db


class CustomerLoyalty(db.Model):
    cLId = db.Column(db.Integer, unique=True, primary_key=True)
    cLLevel = db.Column(db.String(45), nullable=False)
    cLPercentage = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)

