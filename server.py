from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.models.cars import db, Cars
from app.models.users import Users
from app.models.suppliers import Suppliers
from app.models.maintenanceType import MaintenanceType
from app.models.maintenanceAgency import MaintenanceAgency
from app.models.customerLoyalty import CustomerLoyalty
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


@app.get('/suppliers')
def suppliersRouteAccess():
    return 'Inside Suppliers'


@app.get('/suppliers/all')
def getAllSuppliers():
    suppliers = Suppliers.query.all()
    return jsonify([to_dict(supplier) for supplier in suppliers])


@app.get('/maintenancetype')
def maintenanceTypeRouteAccess():
    return 'Inside Maintenance Type'


@app.get('/maintenancetype/all')
def getAllMaintenanceTypes():
    maintenanceType = MaintenanceType.query.all()
    return jsonify([to_dict(maintenanceT) for maintenanceT in maintenanceType])

@app.get('/maintenanceagency')
def maintenanceAgencyRouteAccess():
    return 'Inside Maintenance Agency'


@app.get('/maintenanceagency/all')
def getAllMaintenanceAgencies():
    maintenanceAgency = MaintenanceAgency.query.all()
    return jsonify([to_dict(maintenanceA) for maintenanceA in maintenanceAgency])

@app.get('/customerloyalty')
def customerLoyaltyRouteAccess():
    return 'Inside Customer Loyalty'


@app.get('/customerloyalty/all')
def getAllCustomerLoyalty():
    customerLoyalty = CustomerLoyalty.query.all()
    return jsonify([to_dict(customerLo) for customerLo in customerLoyalty])


@app.get('/')
def index():  # put application's code here
    return 'Welcome to NuAuto!'


if __name__ == '__main__':
    app.run()
