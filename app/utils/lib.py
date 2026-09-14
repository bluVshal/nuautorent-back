"""Serialization helpers."""
import base64
import enum

from sqlalchemy import inspect

# Never serialize these columns, regardless of the model. This stops password
# hashes (and any future secret column) from leaking through an API response.
SENSITIVE_FIELDS = {"userPassword", "password", "passwordHash"}


def _clean(value):
    """Coerce a column value into something JSON-serializable."""
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, enum.Enum):
        return value.value
    return value


def to_dict(model, exclude=None):
    """Serialize any SQLAlchemy model instance to a plain dict.

    Sensitive fields (see SENSITIVE_FIELDS) are always removed; pass `exclude`
    to drop additional columns (e.g. large binary blobs).
    """
    excluded = set(exclude or ()) | SENSITIVE_FIELDS
    mapper = inspect(model).mapper
    return {
        column.key: _clean(getattr(model, column.key))
        for column in mapper.column_attrs
        if column.key not in excluded
    }
