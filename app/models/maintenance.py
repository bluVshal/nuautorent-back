from datetime import datetime

from app.extensions import db


class Maintenance(db.Model):
    maintenanceId = db.Column(db.Integer, primary_key=True)
    # References Cars.carId / MaintenanceAgency / MaintenanceType.
    carId = db.Column(db.Integer, nullable=False)
    maintenanceAgencyId = db.Column(db.Integer)
    maintenanceTypeId = db.Column(db.Integer)
    maintenanceStartDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    maintenanceEndDate = db.Column(db.DateTime)
    maintenanceCost = db.Column(db.Float)
    maintenanceDescription = db.Column(db.String(500))
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)
