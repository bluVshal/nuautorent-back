from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.models.cars import db, Cars
from app.models.users import Users
from app.utils.lib import to_dict
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    return jsonify([to_dict(car) for car in cars])


@app.get('/users')
def usersRouteAccess():
    return 'Inside Users'


@app.get('/users/all')
def getAllUsers():
    users = Users.query.all()
    return jsonify([to_dict(user) for user in users])


@app.get('/')
def index():  # put application's code here
    return 'Welcome to NuAuto!'


if __name__ == '__main__':
    app.run()


