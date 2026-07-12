"""
Input validation helpers shared by driver and trip routes/services.
"""
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId


def is_valid_object_id(id_str):
    """Return True if id_str is a valid Mongo ObjectId string."""
    if not id_str:
        return False
    try:
        ObjectId(id_str)
        return True
    except (InvalidId, TypeError):
        return False


def to_object_id(id_str):
    """Convert a string to ObjectId, or None if invalid."""
    if not is_valid_object_id(id_str):
        return None
    return ObjectId(id_str)


def parse_date(date_str):
    """
    Parse an ISO-8601 date/datetime string (e.g. '2026-07-12' or
    '2026-07-12T10:00:00') into a datetime object. Returns None on failure.
    """
    if not date_str:
        return None
    if isinstance(date_str, datetime):
        return date_str
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def missing_fields(payload, required):
    """Return a list of required field names missing from payload."""
    return [field for field in required if not payload.get(field)]


def serialize_document(doc):
    """Convert a Mongo document's _id (and any ObjectId fields) to strings."""
    if doc is None:
        return None
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    for key in ("driverId", "vehicleId", "tripId"):
        if key in doc and isinstance(doc[key], ObjectId):
            doc[key] = str(doc[key])
    for key in ("createdAt", "updatedAt", "licenseExpiry"):
        if key in doc and isinstance(doc[key], datetime):
            doc[key] = doc[key].isoformat()
    return doc
