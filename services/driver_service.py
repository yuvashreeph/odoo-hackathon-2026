"""
Driver business logic. Routes stay thin; all Mongo access and rule
enforcement lives here.
"""
from database.mongo import drivers_collection, trips_collection
from models.driver import driver_document
from utils.constants import DRIVER_STATUS, TRIP_STATUS
from utils.validators import to_object_id, parse_date, serialize_document


def list_drivers(search=None, status=None):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if status:
        query["status"] = status
    docs = drivers_collection.find(query)
    return [serialize_document(d) for d in docs]


def get_driver(driver_id):
    oid = to_object_id(driver_id)
    if oid is None:
        return None, "Invalid driver id"
    doc = drivers_collection.find_one({"_id": oid})
    if doc is None:
        return None, "Driver not found"
    return serialize_document(doc), None


def create_driver(payload):
    required = ["name", "licenseNumber", "licenseCategory", "licenseExpiry", "phone"]
    missing = [f for f in required if not payload.get(f)]
    if missing:
        return None, [f"Missing field: {f}" for f in missing]

    expiry = parse_date(payload["licenseExpiry"])
    if expiry is None:
        return None, ["licenseExpiry must be a valid date (YYYY-MM-DD)"]

    # licenseNumber must be unique
    if drivers_collection.find_one({"licenseNumber": payload["licenseNumber"]}):
        return None, ["A driver with this licenseNumber already exists"]

    doc = driver_document(
        name=payload["name"],
        license_number=payload["licenseNumber"],
        license_category=payload["licenseCategory"],
        license_expiry=expiry,
        phone=payload["phone"],
        safety_score=payload.get("safetyScore", 100),
        status=payload.get("status", "AVAILABLE"),
    )
    result = drivers_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_document(doc), None


def update_driver(driver_id, payload):
    oid = to_object_id(driver_id)
    if oid is None:
        return None, ["Invalid driver id"]

    existing = drivers_collection.find_one({"_id": oid})
    if existing is None:
        return None, ["Driver not found"]

    update_fields = {}
    for field in ("name", "licenseNumber", "licenseCategory", "phone", "safetyScore"):
        if field in payload:
            update_fields[field] = payload[field]

    if "licenseExpiry" in payload:
        expiry = parse_date(payload["licenseExpiry"])
        if expiry is None:
            return None, ["licenseExpiry must be a valid date (YYYY-MM-DD)"]
        update_fields["licenseExpiry"] = expiry

    if "status" in payload:
        if payload["status"] not in DRIVER_STATUS:
            return None, [f"status must be one of {DRIVER_STATUS}"]
        update_fields["status"] = payload["status"]

    if not update_fields:
        return None, ["No valid fields to update"]

    from datetime import datetime
    update_fields["updatedAt"] = datetime.utcnow()

    drivers_collection.update_one({"_id": oid}, {"$set": update_fields})
    updated = drivers_collection.find_one({"_id": oid})
    return serialize_document(updated), None


def delete_driver(driver_id):
    oid = to_object_id(driver_id)
    if oid is None:
        return False, "Invalid driver id"

    existing = drivers_collection.find_one({"_id": oid})
    if existing is None:
        return False, "Driver not found"

    if existing.get("status") == "ON_TRIP":
        return False, "Cannot delete a driver who is currently ON_TRIP"

    active_trip = trips_collection.find_one({
        "driverId": oid,
        "status": {"$in": ["DRAFT", "DISPATCHED"]}
    })
    if active_trip:
        return False, "Cannot delete a driver linked to an active trip"

    drivers_collection.delete_one({"_id": oid})
    return True, None
