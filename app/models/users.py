from datetime import datetime

from app.extensions import db

# Supported roles, ordered loosely from most to least privileged.
ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_USER = "user"
VALID_ROLES = {ROLE_ADMIN, ROLE_MANAGER, ROLE_USER}


class Users(db.Model):
    userId = db.Column(db.Integer, unique=True, primary_key=True)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    # Stores a bcrypt hash (60 chars). NOT unique: distinct users may
    # coincidentally hash to comparable lengths, and uniqueness here would
    # leak information and reject legitimate passwords.
    userPassword = db.Column(db.String(60), nullable=False)
    # Authorization role. server_default keeps existing rows valid on migration.
    userRole = db.Column(
        db.String(20), nullable=False, default=ROLE_USER, server_default=ROLE_USER
    )
    lastLoginDate = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, default=datetime.utcnow)
