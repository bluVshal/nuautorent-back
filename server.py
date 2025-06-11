from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.models.cars import db, Cars


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')

db.init_app(app)

@app.get('/cars')
def carsRouteAccess():
    return 'Inside Cars'


@app.get('/cars/all')
def getAllCars():
    cars = Cars.query.all()
    for car in cars:
        print(car.carChassisNumber)
    return 'cars'


@app.get('/')
def index():  # put application's code here
    return 'Welcome to NuAuto!'


if __name__ == '__main__':
    app.run()

