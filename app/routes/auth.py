"""Authentication routes: login and (gated) registration."""
import os
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app

from app.extensions import db, bcrypt, limiter
from app.models.users import Users, VALID_ROLES, ROLE_USER
from app.services.jwt_service import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _validate_credentials(data):
    """Basic input validation for a credentials payload.

    Returns (username, password) on success or (None, error_message).
    """
    if not isinstance(data, dict):
        return None, "Request body must be JSON"

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return None, "username and password are required strings"

    username = username.strip()
    if not (1 <= len(username) <= 100):
        return None, "username must be between 1 and 100 characters"
    if not (8 <= len(password) <= 128):
        return None, "password must be between 8 and 128 characters"

    return (username, password), None


@auth_bp.post("/login")
@limiter.limit("5 per minute")  # throttle brute-force attempts
def login():
    creds, error = _validate_credentials(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    username, password = creds
    user = Users.query.filter_by(userName=username).first()

    # Generic message + always-run hash check would be ideal to fully avoid
    # timing/user-enumeration; at minimum we return an identical response for
    # "no such user" and "wrong password".
    if user is None or not bcrypt.check_password_hash(user.userPassword, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.active:
        return jsonify({"error": "Account is disabled"}), 403

    user.lastLoginDate = datetime.utcnow()
    db.session.commit()

    token = generate_token(
        user.userId, current_app.config["JWT_SECRET_KEY"], role=user.userRole
    )
    return jsonify({"token": token, "tokenType": "Bearer", "role": user.userRole}), 200


@auth_bp.post("/register")
@limiter.limit("3 per minute")
def register():
    # Open registration is off by default. Enable deliberately for local setup
    # only; in production users should be provisioned by an admin/seed script.
    if os.getenv("ALLOW_OPEN_REGISTRATION", "false").lower() != "true":
        return jsonify({"error": "Registration is disabled"}), 403

    creds, error = _validate_credentials(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    username, password = creds
    if Users.query.filter_by(userName=username).first() is not None:
        return jsonify({"error": "Username already taken"}), 409

    # Role is optional; defaults to the least-privileged role. Only accepted here
    # because open registration is a deliberate, gated dev-only path.
    role = (request.get_json(silent=True) or {}).get("role", ROLE_USER)
    if role not in VALID_ROLES:
        return jsonify({"error": f"role must be one of {sorted(VALID_ROLES)}"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Users(userName=username, userPassword=password_hash, userRole=role, active=True)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created", "userId": user.userId, "role": role}), 201
