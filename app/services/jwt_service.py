"""JWT creation and verification (HS256) built on PyJWT."""
from datetime import datetime, timedelta, timezone

import jwt

ALGORITHM = "HS256"
DEFAULT_EXPIRY_SECONDS = 3600  # 1 hour


def generate_token(identity, secret, role=None, expires_in=DEFAULT_EXPIRY_SECONDS):
    """Return a signed JWT for the given identity (e.g. a user id).

    The user's role is embedded as a claim so authorization checks don't need a
    database round-trip on every request.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(identity),
        "role": role,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def decode_token(token, secret):
    """Decode and verify a JWT. Raises jwt exceptions on failure."""
    return jwt.decode(token, secret, algorithms=[ALGORITHM])
