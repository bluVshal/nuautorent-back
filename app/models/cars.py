from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()
class Car(db.Model):
    carId = db.Column(db.Integer, unique=True, primary_key=True)
    carChassisNumber = db.Column(db.String(17), unique=True, nullable=False)
    carMake = db.Column(db.String(100), nullable=False)
    carModel = db.Column(db.String(100), nullable=False)
    carNTARegNumber = db.Column(db.String(45), nullable=False)
    carBuyDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    carPrice = db.Column(db.Text, nullable=False)
    carStatus
    carSoldDate = db.Column(db.DateTime, default=datetime.utcnow)
    carPhoto
    carType
    isCarElectric
    isCarHybrid
    carTransmission
    carSeats
    carNoDoors
    carHP
    carCo2Emission
    active
    carAddDate = db.Column(db.DateTime, default=datetime.utcnow)
    carLastModDate = db.Column(db.DateTime, default=datetime.utcnow)