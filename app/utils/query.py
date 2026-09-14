"""Helpers for turning request query params into SQLAlchemy filters."""
from datetime import datetime

from flask import request


def arg(name):
    """Return a trimmed, non-empty query-string value, or None."""
    value = request.args.get(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def like(query, column, value):
    """Apply a case-insensitive `contains` filter when `value` is set."""
    if value:
        return query.filter(column.ilike(f"%{value}%"))
    return query


def bool_arg(name):
    """Parse a boolean query param ('true'/'false'), or None if absent."""
    value = arg(name)
    if value is None:
        return None
    return value.lower() == "true"


def parse_date(value):
    """Parse an ISO date/datetime string (tolerant of a trailing 'Z')."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d")
        except ValueError:
            return None
