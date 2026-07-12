"""
Vehicle model helpers (Member 2 — Fleet Manager module)

Collection: vehicles
Fields (must match team schema exactly — README.md):
    registrationNumber (str, unique)
    vehicleName        (str)
    vehicleType        (str)
    maxLoadCapacity     (number)
    odometer            (number)
    acquisitionCost     (number)
    status              (str)  -> AVAILABLE | ON_TRIP | IN_SHOP | RETIRED
    region              (str)
"""

from utils.constants import VEHICLE_STATUS
from utils.validators import serialize_document

REQUIRED_FIELDS = [
    "registrationNumber",
    "vehicleName",
    "vehicleType",
    "maxLoadCapacity",
    "acquisitionCost",
]


def build_vehicle_doc(data):
    """Build a clean vehicle document from incoming request JSON."""
    return {
        "registrationNumber": str(data.get("registrationNumber", "")).strip().upper(),
        "vehicleName": str(data.get("vehicleName", "")).strip(),
        "vehicleType": str(data.get("vehicleType", "")).strip(),
        "maxLoadCapacity": data.get("maxLoadCapacity"),
        "odometer": data.get("odometer", 0),
        "acquisitionCost": data.get("acquisitionCost"),
        "status": VEHICLE_STATUS[0],  # "AVAILABLE"
        "region": str(data.get("region", "")).strip(),
    }


def validate_vehicle_payload(data):
    """Return a list of validation error strings (empty list = valid)."""
    errors = []
    for field in REQUIRED_FIELDS:
        if data.get(field) in (None, ""):
            errors.append(f"'{field}' is required")

    if data.get("maxLoadCapacity") is not None:
        if not isinstance(data["maxLoadCapacity"], (int, float)) or data["maxLoadCapacity"] <= 0:
            errors.append("'maxLoadCapacity' must be a positive number")

    if data.get("acquisitionCost") is not None:
        if not isinstance(data["acquisitionCost"], (int, float)) or data["acquisitionCost"] < 0:
            errors.append("'acquisitionCost' must be a non-negative number")

    if data.get("status") is not None and data["status"] not in VEHICLE_STATUS:
        errors.append(f"'status' must be one of {VEHICLE_STATUS}")

    return errors


def serialize_vehicle(vehicle):
    """Convert a Mongo vehicle document into a JSON-safe dict."""
    return serialize_document(vehicle)
