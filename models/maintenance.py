"""
Maintenance model helpers (Member 2 — Fleet Manager module)

Collection: maintenance_logs
Fields (team schema — README.md):
    vehicleId          (ObjectId)
    maintenanceType     (str)
    cost                (number)
    date                (str, e.g. "2026-07-12")
    status              (str)  -> ACTIVE | COMPLETED
"""

from utils.constants import MAINTENANCE_STATUS
from utils.validators import serialize_document

REQUIRED_FIELDS = ["vehicleId", "maintenanceType", "cost", "date"]


def build_maintenance_doc(data, vehicle_object_id):
    return {
        "vehicleId": vehicle_object_id,
        "maintenanceType": str(data.get("maintenanceType", "")).strip(),
        "cost": data.get("cost"),
        "date": data.get("date"),
        "status": MAINTENANCE_STATUS[0],  # "ACTIVE"
    }


def validate_maintenance_payload(data):
    errors = []
    for field in REQUIRED_FIELDS:
        if data.get(field) in (None, ""):
            errors.append(f"'{field}' is required")

    if data.get("cost") is not None:
        if not isinstance(data["cost"], (int, float)) or data["cost"] < 0:
            errors.append("'cost' must be a non-negative number")

    return errors


def serialize_maintenance(record):
    """Convert a Mongo maintenance document into a JSON-safe dict."""
    return serialize_document(record)
