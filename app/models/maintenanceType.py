from datetime import datetime

from app.extensions import db


class MaintenanceType(db.Model):
    maintenanceTypeIdId = db.Column(db.Integer, unique=True, primary_key=True)
    maintenanceTypeDesc = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=False)
    maintenanceAddDate = db.Column(db.DateTime, default=datetime.utcnow)
    maintenanceLastModDate = db.Column(db.DateTime, default=datetime.utcnow)
