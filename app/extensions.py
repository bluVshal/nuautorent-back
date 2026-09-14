"""Shared Flask extension instances.

Defining these here (rather than one-per-module) means every model and route
binds to the SAME SQLAlchemy metadata, bcrypt context and rate limiter. This
is required for authentication to work: the Users model and the login route
must share a single db session.
"""
import os

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Single shared ORM instance for all models.
db = SQLAlchemy()

# Password hashing (bcrypt).
bcrypt = Bcrypt()

# Rate limiter. Defaults are conservative global limits; sensitive endpoints
# (e.g. login) tighten these further with their own @limiter.limit decorator.
# Storage defaults to in-memory (fine for a single dev process); point
# RATELIMIT_STORAGE_URI at Redis for a real multi-process deployment.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
)
