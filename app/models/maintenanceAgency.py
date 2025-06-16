from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum


class DesignationEnum(str, enum.Enum):
    Mr = 'Mr'
    Mrs = 'Mrs'
    Ms = 'Ms'


db = SQLAlchemy()


class MaintenanceAgency(db.Model):
    maintenanceAgencyId = db.Column(db.Integer, unique=True, primary_key=True)
    maintenanceAgencyName = db.Column(db.String(200), nullable=False)
    maintenanceAgencyResponsible = db.Column(db.String(300), nullable=False)
    maintenanceAgencyAddress = db.Column(db.String(250), nullable=False)
    maintenanceAgencyDesignation = db.Column(db.Enum(DesignationEnum), nullable=False)
    maintenanceAgencyEmail = db.Column(db.String(150), nullable=False)
    maintenanceAgencyPhone = db.Column(db.Integer, nullable=False)
    maintenanceAgencyActive = db.Column(db.Boolean(), default=False)
    maintenanceAgencyAddDate = db.Column(db.DateTime, default=datetime.utcnow)
    maintenanceAgencyLastModified = db.Column(db.DateTime, default=datetime.utcnow)

