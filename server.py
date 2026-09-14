import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate

from app.extensions import db, bcrypt, limiter
from app.models.cars import (
    Cars,
    CarStatusEnum,
    CarTypeEnum,
    CarTransmissionTypeEnum,
)
from app.models.users import Users
from app.models.suppliers import Suppliers
from app.models.maintenanceType import MaintenanceType
from app.models.maintenanceAgency import MaintenanceAgency
from app.models.customerLoyalty import CustomerLoyalty
from app.models.customers import Customers
from app.models.booking import Booking
from app.models.rental import Rental
from app.models.maintenance import Maintenance
from app.utils.lib import to_dict
from app.utils.query import arg, like, bool_arg, parse_date
from app.middleware.auth import token_required, roles_required
from app.middleware.security_headers import register_security_headers
from app.routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)

# --- CORS: restrict to known frontend origins only (no wildcard) ------------
# Comma-separated list in FRONTEND_ORIGIN, defaulting to the local Vite/CRA
# dev servers.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGIN", "http://localhost:5173,http://localhost:3000"
    ).split(",")
    if origin.strip()
]
CORS(app, origins=allowed_origins, supports_credentials=False)

# --- Database ---------------------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- JWT: fail closed if no secret is configured ----------------------------
jwt_secret = os.getenv("JWT_SECRET")
if not jwt_secret:
    raise RuntimeError(
        "JWT_SECRET environment variable is required. Refusing to start with an "
        "unsigned/insecure token configuration."
    )
app.config["JWT_SECRET_KEY"] = jwt_secret

# --- Initialize shared extensions -------------------------------------------
db.init_app(app)
bcrypt.init_app(app)
limiter.init_app(app)
migrate = Migrate(app, db)

# --- Security response headers ----------------------------------------------
register_security_headers(app)

# --- Blueprints -------------------------------------------------------------
app.register_blueprint(auth_bp)


# --- Public endpoints -------------------------------------------------------
@app.get("/")
def index():
    return "Welcome to NuAuto!"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# --- Protected data endpoints (require a valid Bearer token) ----------------
@app.get("/cars/all")
@token_required
def getAllCars():
    cars = Cars.query.all()
    return jsonify([to_dict(car, exclude=["carPhoto"]) for car in cars])


@app.get("/cars/short")
@token_required
def getSomeCars():
    q = Cars.query
    q = like(q, Cars.carMake, arg("carMake"))
    q = like(q, Cars.carModel, arg("carModel"))
    q = like(q, Cars.carNTARegNumber, arg("carNTARegNumber"))

    # Enum filters: ignore an unrecognized value rather than erroring.
    for param, column, enum_cls in (
        ("carType", Cars.carType, CarTypeEnum),
        ("carStatus", Cars.carStatus, CarStatusEnum),
        ("carTransmission", Cars.carTransmission, CarTransmissionTypeEnum),
    ):
        value = arg(param)
        if value:
            try:
                q = q.filter(column == enum_cls(value))
            except ValueError:
                pass

    electric = bool_arg("isCarElectric")
    if electric is not None:
        q = q.filter(Cars.isCarElectric == electric)
    hybrid = bool_arg("isCarHybrid")
    if hybrid is not None:
        q = q.filter(Cars.isCarHybrid == hybrid)

    cars = q.with_entities(Cars.carModel, Cars.carMake).all()
    return jsonify([{"carModel": c.carModel, "carMake": c.carMake} for c in cars])


@app.get("/users/all")
@roles_required("admin")  # user accounts are admin-only
def getAllUsers():
    users = Users.query.all()
    # to_dict strips the password hash via SENSITIVE_FIELDS.
    return jsonify([to_dict(user) for user in users])


@app.get("/suppliers/all")
@token_required
def getAllSuppliers():
    suppliers = Suppliers.query.all()
    return jsonify([to_dict(supplier) for supplier in suppliers])


@app.get("/suppliers/short")
@token_required
def getSomeSuppliers():
    q = Suppliers.query
    q = like(q, Suppliers.supplierName, arg("supplierName"))
    q = like(q, Suppliers.supplierAddress, arg("supplierAddress"))
    q = like(q, Suppliers.supplierEmail, arg("supplierEmail"))
    q = like(q, Suppliers.supplierContactName, arg("supplierContactName"))
    phone = arg("supplierPhone")
    if phone and phone.isdigit():
        q = q.filter(Suppliers.supplierPhone == int(phone))
    suppliers = q.all()
    return jsonify([to_dict(supplier) for supplier in suppliers])


@app.get("/maintenancetype/all")
@token_required
def getAllMaintenanceTypes():
    maintenance_types = MaintenanceType.query.all()
    return jsonify([to_dict(m) for m in maintenance_types])


@app.get("/maintenanceagency/all")
@token_required
def getAllMaintenanceAgencies():
    agencies = MaintenanceAgency.query.all()
    return jsonify([to_dict(a) for a in agencies])


@app.get("/customerloyalty/all")
@token_required
def getAllCustomerLoyalty():
    loyalty = CustomerLoyalty.query.all()
    return jsonify([to_dict(item) for item in loyalty])


# --- "/short" list endpoints (trimmed lists used by the frontend search pages).
# These match the frontend's `/<resource>/short` convention.
@app.get("/users/short")
@roles_required("admin")  # user accounts are admin-only
def getSomeUsers():
    users = Users.query.with_entities(
        Users.userId, Users.userName, Users.userRole
    ).all()
    return jsonify(
        [
            {"userId": u.userId, "userName": u.userName, "userRole": u.userRole}
            for u in users
        ]
    )


@app.get("/maintenanceagency/short")
@token_required
def getSomeMaintenanceAgencies():
    agencies = MaintenanceAgency.query.all()
    return jsonify([to_dict(a) for a in agencies])


@app.get("/customerloyalty/short")
@token_required
def getSomeCustomerLoyalty():
    loyalty = CustomerLoyalty.query.all()
    return jsonify([to_dict(item) for item in loyalty])


# --- Customers --------------------------------------------------------------
@app.get("/customers/all")
@token_required
def getAllCustomers():
    customers = Customers.query.all()
    return jsonify([to_dict(c) for c in customers])


@app.get("/customers/short")
@token_required
def getSomeCustomers():
    q = Customers.query
    q = like(q, Customers.customerFName, arg("customerFName"))
    q = like(q, Customers.customerLName, arg("customerLName"))
    q = like(q, Customers.customerMName, arg("customerMName"))
    q = like(q, Customers.customerOName, arg("customerOName"))
    q = like(q, Customers.customerAddress, arg("customerAddress"))
    q = like(q, Customers.customerEmail, arg("customerEmail"))
    q = like(q, Customers.customerPhone, arg("customerPhone"))
    customers = q.all()
    return jsonify([to_dict(c) for c in customers])


# --- Booking ----------------------------------------------------------------
@app.get("/booking/all")
@token_required
def getAllBookings():
    bookings = Booking.query.all()
    return jsonify([to_dict(b) for b in bookings])


@app.get("/booking/short")
@token_required
def getSomeBookings():
    q = Booking.query
    reg = arg("carRegNo")
    if reg:
        q = q.join(Cars, Cars.carId == Booking.carId).filter(
            Cars.carNTARegNumber.ilike(f"%{reg}%")
        )
    name = arg("customerName")
    if name:
        q = q.join(Customers, Customers.customerId == Booking.customerId).filter(
            Customers.customerFName.ilike(f"%{name}%")
            | Customers.customerLName.ilike(f"%{name}%")
        )
    pickup = parse_date(arg("bookingPickUpDate"))
    if pickup:
        q = q.filter(Booking.bookingPickUpDate >= pickup)
    return_date = parse_date(arg("bookingReturnDate"))
    if return_date:
        q = q.filter(Booking.bookingReturnDate <= return_date)
    bookings = q.all()
    return jsonify([to_dict(b) for b in bookings])


# --- Rental -----------------------------------------------------------------
@app.get("/rental/all")
@token_required
def getAllRentals():
    rentals = Rental.query.all()
    return jsonify([to_dict(r) for r in rentals])


@app.get("/rental/short")
@token_required
def getSomeRentals():
    q = Rental.query
    reg = arg("carRegNo")
    if reg:
        q = q.join(Cars, Cars.carId == Rental.carId).filter(
            Cars.carNTARegNumber.ilike(f"%{reg}%")
        )
    name = arg("customerName")
    if name:
        q = q.join(Customers, Customers.customerId == Rental.customerId).filter(
            Customers.customerFName.ilike(f"%{name}%")
            | Customers.customerLName.ilike(f"%{name}%")
        )
    pickup = parse_date(arg("rentalPickupDate"))
    if pickup:
        q = q.filter(Rental.rentalPickupDate >= pickup)
    return_date = parse_date(arg("rentalReturnDate"))
    if return_date:
        q = q.filter(Rental.rentalReturnDate <= return_date)
    rentals = q.all()
    return jsonify([to_dict(r) for r in rentals])


# --- Maintenance records ----------------------------------------------------
@app.get("/maintenance/all")
@token_required
def getAllMaintenance():
    records = Maintenance.query.all()
    return jsonify([to_dict(m) for m in records])


@app.get("/maintenance/short")
@token_required
def getSomeMaintenance():
    q = Maintenance.query
    start = parse_date(arg("maintenanceStartDate"))
    if start:
        q = q.filter(Maintenance.maintenanceStartDate >= start)
    end = parse_date(arg("maintenanceEndDate"))
    if end:
        q = q.filter(Maintenance.maintenanceEndDate <= end)
    records = q.all()
    return jsonify([to_dict(m) for m in records])


if __name__ == "__main__":
    # Secure-by-default run configuration. Debug is OFF unless explicitly
    # enabled, and we bind to localhost rather than 0.0.0.0. For production use
    # a real WSGI server (gunicorn/waitress) instead of app.run().
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=debug)
