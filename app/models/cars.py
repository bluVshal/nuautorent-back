from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import LargeBinary
import enum


class CarStatusEnum(str, enum.Enum):
    Available = 'Available'
    Rented = 'Rented'
    Maintenance = 'Maintenance'
    Sold = 'Sold'


class CarTypeEnum(str, enum.Enum):
    Small = 'Small'
    Compact = 'Compact'
    Large = 'Large'
    Limousine = 'Limousine'


class CarTransmissionTypeEnum(str, enum.Enum):
    AT = 'AT'
    MT = 'MT'


db = SQLAlchemy()


class Cars(db.Model):
    carId = db.Column(db.Integer, unique=True, primary_key=True)
    carChassisNumber = db.Column(db.String(17), unique=True, nullable=False)
    carMake = db.Column(db.String(100), nullable=False)
    carModel = db.Column(db.String(100), nullable=False)
    carNTARegNumber = db.Column(db.String(45), nullable=False)
    carBuyDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    carPrice = db.Column(db.Text, nullable=False)
    carStatus = db.Column(db.Enum(CarStatusEnum), nullable=False)
    carSoldDate = db.Column(db.DateTime, default=datetime.utcnow)
    carPhoto = db.Column(LargeBinary)
    carType = db.Column(db.Enum(CarTypeEnum), nullable=False)
    isCarElectric = db.Column(db.Boolean(), default=False)
    isCarHybrid = db.Column(db.Boolean(), default=False)
    carTransmission = db.Column(db.Enum(CarTransmissionTypeEnum), nullable=False)
    carSeats = db.Column(db.Integer, nullable=False)
    carNoDoors = db.Column(db.Integer, nullable=False)
    carHP = db.Column(db.Integer, nullable=False)
    carMileage = db.Column(db.Integer, nullable=False)
    carCo2Emission = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean(), default=False)
    carAddDate = db.Column(db.DateTime, default=datetime.utcnow)
    carLastModDate = db.Column(db.DateTime, default=datetime.utcnow)
