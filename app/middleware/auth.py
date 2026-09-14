"""Authentication & authorization middleware.

- `token_required` enforces a valid JWT.
- `roles_required(*roles)` enforces a valid JWT AND that the caller's role is
  one of the allowed roles.

Both stash the authenticated user id and role on `flask.g`.
"""
from functools import wraps

import jwt
from flask import request, jsonify, current_app, g

from app.services.jwt_service import decode_token


def _authenticate():
    """Validate the request's bearer token.

    Returns (payload, None) on success, or (None, (response, status)) on failure.
    """
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, (jsonify({"error": "Missing or malformed Authorization header"}), 401)

    token = parts[1]
    try:
        payload = decode_token(token, current_app.config["JWT_SECRET_KEY"])
    except jwt.ExpiredSignatureError:
        return None, (jsonify({"error": "Token has expired"}), 401)
    except jwt.InvalidTokenError:
        return None, (jsonify({"error": "Invalid token"}), 401)

    g.user_id = payload.get("sub")
    g.user_role = payload.get("role")
    return payload, None


def token_required(f):
    """Reject requests without a valid `Authorization: Bearer <token>` header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        _, error = _authenticate()
        if error:
            return error
        return f(*args, **kwargs)

    return decorated


def roles_required(*allowed_roles):
    """Require a valid token whose role is one of `allowed_roles` (else 403)."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            payload, error = _authenticate()
            if error:
                return error
            if payload.get("role") not in allowed_roles:
                return jsonify({"error": "Insufficient permissions"}), 403
            return f(*args, **kwargs)

        return decorated

    return decorator
