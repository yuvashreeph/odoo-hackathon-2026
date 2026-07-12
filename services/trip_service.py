"""
Trip business logic: CRUD (Draft-only edit/delete) plus the
dispatch / complete / cancel state machine, matching the team's agreed
business rules:

  DRAFT --dispatch--> DISPATCHED --complete--> COMPLETED
  DRAFT --cancel--> CANCELLED
  DISPATCHED --cancel--> CANCELLED (frees driver + vehicle)
"""
from datetime import datetime

from database.mongo import trips_collection, drivers_collection, vehicles_collection
from models.trip import trip_document
from utils.validators import to_object_id, serialize_document


def list_trips(status=None):
    query = {}
    if status:
        query["status"] = status
    docs = trips_collection.find(query)
    return [serialize_document(d) for d in docs]


def get_trip(trip_id):
    oid = to_object_id(trip_id)
    if oid is None:
        return None, "Invalid trip id"
    doc = trips_collection.find_one({"_id": oid})
    if doc is None:
        return None, "Trip not found"
    return serialize_document(doc), None


def create_trip(payload):
    required = ["source", "destination", "vehicleId", "driverId", "cargoWeight", "plannedDistance"]
    missing = [f for f in required if payload.get(f) in (None, "")]
    if missing:
        return None, [f"Missing field: {f}" for f in missing]

    vehicle_oid = to_object_id(payload["vehicleId"])
    driver_oid = to_object_id(payload["driverId"])
    if vehicle_oid is None:
        return None, ["Invalid vehicleId"]
    if driver_oid is None:
        return None, ["Invalid driverId"]

    doc = trip_document(
        source=payload["source"],
        destination=payload["destination"],
        vehicle_id=vehicle_oid,
        driver_id=driver_oid,
        cargo_weight=payload["cargoWeight"],
        planned_distance=payload["plannedDistance"],
        revenue=payload.get("revenue"),
        status="DRAFT",
    )
    result = trips_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_document(doc), None


def update_trip(trip_id, payload):
    oid = to_object_id(trip_id)
    if oid is None:
        return None, ["Invalid trip id"]

    existing = trips_collection.find_one({"_id": oid})
    if existing is None:
        return None, ["Trip not found"]

    if existing["status"] != "DRAFT":
        return None, ["Only trips in DRAFT status can be edited"]

    update_fields = {}
    for field in ("source", "destination", "cargoWeight", "plannedDistance", "revenue"):
        if field in payload:
            update_fields[field] = payload[field]

    if "vehicleId" in payload:
        vehicle_oid = to_object_id(payload["vehicleId"])
        if vehicle_oid is None:
            return None, ["Invalid vehicleId"]
        update_fields["vehicleId"] = vehicle_oid

    if "driverId" in payload:
        driver_oid = to_object_id(payload["driverId"])
        if driver_oid is None:
            return None, ["Invalid driverId"]
        update_fields["driverId"] = driver_oid

    if not update_fields:
        return None, ["No valid fields to update"]

    update_fields["updatedAt"] = datetime.utcnow()
    trips_collection.update_one({"_id": oid}, {"$set": update_fields})
    updated = trips_collection.find_one({"_id": oid})
    return serialize_document(updated), None


def delete_trip(trip_id):
    oid = to_object_id(trip_id)
    if oid is None:
        return False, "Invalid trip id"

    existing = trips_collection.find_one({"_id": oid})
    if existing is None:
        return False, "Trip not found"

    if existing["status"] != "DRAFT":
        return False, "Only trips in DRAFT status can be deleted"

    trips_collection.delete_one({"_id": oid})
    return True, None


def dispatch_trip(trip_id):
    """
    Runs the 8-point validation in order and returns ALL failing checks
    at once. On success, updates Trip -> DISPATCHED, Driver -> ON_TRIP,
    Vehicle -> ON_TRIP together.
    """
    oid = to_object_id(trip_id)
    if oid is None:
        return None, ["Invalid trip id"]

    trip = trips_collection.find_one({"_id": oid})
    if trip is None:
        return None, ["Trip not found"]

    if trip["status"] != "DRAFT":
        return None, ["Only trips in DRAFT status can be dispatched"]

    errors = []

    driver = drivers_collection.find_one({"_id": trip["driverId"]})
    vehicle = vehicles_collection.find_one({"_id": trip["vehicleId"]})

    # 1. Driver exists
    if driver is None:
        errors.append("Driver does not exist")
    # 2. Vehicle exists
    if vehicle is None:
        errors.append("Vehicle does not exist")

    if driver is not None:
        # 3. Driver status is AVAILABLE
        if driver.get("status") != "AVAILABLE":
            errors.append(f"Driver status must be AVAILABLE (currently {driver.get('status')})")
        # 5. Driver's license is not expired
        expiry = driver.get("licenseExpiry")
        if isinstance(expiry, datetime) and expiry < datetime.utcnow():
            errors.append("Driver's license is expired")
        # 7. Driver is not already ON_TRIP
        if driver.get("status") == "ON_TRIP":
            errors.append("Driver is already ON_TRIP")

    if vehicle is not None:
        # 4. Vehicle status is AVAILABLE
        if vehicle.get("status") != "AVAILABLE":
            errors.append(f"Vehicle status must be AVAILABLE (currently {vehicle.get('status')})")
        # 6. Cargo weight <= vehicle capacity
        capacity = vehicle.get("maxLoadCapacity")
        if capacity is not None and trip.get("cargoWeight", 0) > capacity:
            errors.append(f"Cargo weight ({trip.get('cargoWeight')}) exceeds vehicle capacity ({capacity})")
        # 8. Vehicle is not already ON_TRIP
        if vehicle.get("status") == "ON_TRIP":
            errors.append("Vehicle is already ON_TRIP")

    if errors:
        return None, errors

    now = datetime.utcnow()
    trips_collection.update_one({"_id": oid}, {"$set": {"status": "DISPATCHED", "updatedAt": now}})
    drivers_collection.update_one({"_id": driver["_id"]}, {"$set": {"status": "ON_TRIP", "updatedAt": now}})
    vehicles_collection.update_one({"_id": vehicle["_id"]}, {"$set": {"status": "ON_TRIP", "updatedAt": now}})

    updated = trips_collection.find_one({"_id": oid})
    return serialize_document(updated), None


def complete_trip(trip_id, actual_distance=None, fuel_used=None, revenue=None):
    oid = to_object_id(trip_id)
    if oid is None:
        return None, ["Invalid trip id"]

    trip = trips_collection.find_one({"_id": oid})
    if trip is None:
        return None, ["Trip not found"]

    if trip["status"] != "DISPATCHED":
        return None, ["Only DISPATCHED trips can be completed"]

    now = datetime.utcnow()
    update_fields = {"status": "COMPLETED", "updatedAt": now}
    if actual_distance is not None:
        update_fields["actualDistance"] = actual_distance
    if fuel_used is not None:
        update_fields["fuelUsed"] = fuel_used
    if revenue is not None:
        update_fields["revenue"] = revenue

    trips_collection.update_one({"_id": oid}, {"$set": update_fields})
    drivers_collection.update_one({"_id": trip["driverId"]}, {"$set": {"status": "AVAILABLE", "updatedAt": now}})
    vehicles_collection.update_one({"_id": trip["vehicleId"]}, {"$set": {"status": "AVAILABLE", "updatedAt": now}})

    updated = trips_collection.find_one({"_id": oid})
    return serialize_document(updated), None


def cancel_trip(trip_id):
    oid = to_object_id(trip_id)
    if oid is None:
        return None, ["Invalid trip id"]

    trip = trips_collection.find_one({"_id": oid})
    if trip is None:
        return None, ["Trip not found"]

    if trip["status"] not in ("DRAFT", "DISPATCHED"):
        return None, ["Only DRAFT or DISPATCHED trips can be cancelled"]

    now = datetime.utcnow()
    was_dispatched = trip["status"] == "DISPATCHED"

    trips_collection.update_one({"_id": oid}, {"$set": {"status": "CANCELLED", "updatedAt": now}})

    if was_dispatched:
        drivers_collection.update_one({"_id": trip["driverId"]}, {"$set": {"status": "AVAILABLE", "updatedAt": now}})
        vehicles_collection.update_one({"_id": trip["vehicleId"]}, {"$set": {"status": "AVAILABLE", "updatedAt": now}})

    updated = trips_collection.find_one({"_id": oid})
    return serialize_document(updated), None
