from datetime import datetime

from app.extensions import db


class Suppliers(db.Model):
    supplierId = db.Column(db.Integer, unique=True, primary_key=True)
    supplierName = db.Column(db.String(150), unique=True, nullable=False)
    supplierAddress = db.Column(db.String(250), nullable=False)
    supplierEmail = db.Column(db.String(150), nullable=False)
    supplierContactName = db.Column(db.String(250), nullable=False)
    supplierPhone = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModified = db.Column(db.DateTime, default=datetime.utcnow)
