"""
Vehicle + Maintenance business logic (Member 2 — Fleet Manager module)
All MongoDB operations for the `vehicles` and `maintenance_logs` collections.
"""

from database.mongo import vehicles_collection, maintenance_logs_collection
from models.vehicle import build_vehicle_doc, serialize_vehicle
from models.maintenance import build_maintenance_doc, serialize_maintenance
from utils.constants import VEHICLE_STATUS, MAINTENANCE_STATUS
from utils.validators import to_object_id

AVAILABLE, ON_TRIP, IN_SHOP, RETIRED = VEHICLE_STATUS
ACTIVE, COMPLETED = MAINTENANCE_STATUS

vehicles_col = vehicles_collection
maintenance_col = maintenance_logs_collection


# ---------------- Vehicle CRUD ----------------

def create_vehicle(data):
    reg_no = str(data.get("registrationNumber", "")).strip().upper()
    if vehicles_col.find_one({"registrationNumber": reg_no}):
        return None, "A vehicle with this registration number already exists"

    doc = build_vehicle_doc(data)
    result = vehicles_col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_vehicle(doc), None


def get_all_vehicles(filters=None):
    query = filters or {}
    vehicles = list(vehicles_col.find(query))
    return [serialize_vehicle(v) for v in vehicles]


def get_vehicle_by_id(vehicle_id):
    oid = to_object_id(vehicle_id)
    if not oid:
        return None, "Invalid vehicle id"
    vehicle = vehicles_col.find_one({"_id": oid})
    if not vehicle:
        return None, "Vehicle not found"
    return serialize_vehicle(vehicle), None


def update_vehicle(vehicle_id, data):
    oid = to_object_id(vehicle_id)
    if not oid:
        return None, "Invalid vehicle id"

    vehicle = vehicles_col.find_one({"_id": oid})
    if not vehicle:
        return None, "Vehicle not found"

    update_data = dict(data)

    new_reg = update_data.get("registrationNumber")
    if new_reg:
        new_reg = new_reg.strip().upper()
        if new_reg != vehicle["registrationNumber"] and vehicles_col.find_one({"registrationNumber": new_reg}):
            return None, "A vehicle with this registration number already exists"
        update_data["registrationNumber"] = new_reg

    allowed_fields = [
        "registrationNumber", "vehicleName", "vehicleType",
        "maxLoadCapacity", "odometer", "acquisitionCost", "status", "region",
    ]
    set_doc = {k: v for k, v in update_data.items() if k in allowed_fields and v is not None}

    if set_doc:
        vehicles_col.update_one({"_id": oid}, {"$set": set_doc})

    updated = vehicles_col.find_one({"_id": oid})
    return serialize_vehicle(updated), None


def delete_vehicle(vehicle_id):
    oid = to_object_id(vehicle_id)
    if not oid:
        return False, "Invalid vehicle id"

    vehicle = vehicles_col.find_one({"_id": oid})
    if not vehicle:
        return False, "Vehicle not found"

    if vehicle.get("status") == ON_TRIP:
        return False, "Cannot delete a vehicle that is currently on a trip"

    vehicles_col.delete_one({"_id": oid})
    return True, None


# ---------------- Maintenance ----------------

def create_maintenance(data):
    vehicle_oid = to_object_id(data.get("vehicleId"))
    if not vehicle_oid:
        return None, "Invalid vehicleId"

    vehicle = vehicles_col.find_one({"_id": vehicle_oid})
    if not vehicle:
        return None, "Vehicle not found"

    if vehicle.get("status") == ON_TRIP:
        return None, "Vehicle is currently on a trip and cannot be sent for maintenance"

    if vehicle.get("status") == RETIRED:
        return None, "Vehicle is retired and cannot be sent for maintenance"

    doc = build_maintenance_doc(data, vehicle_oid)
    result = maintenance_col.insert_one(doc)
    doc["_id"] = result.inserted_id

    # Business rule: creating an ACTIVE maintenance record -> vehicle status = IN_SHOP
    vehicles_col.update_one({"_id": vehicle_oid}, {"$set": {"status": IN_SHOP}})

    return serialize_maintenance(doc), None


def close_maintenance(maintenance_id):
    oid = to_object_id(maintenance_id)
    if not oid:
        return None, "Invalid maintenance id"

    record = maintenance_col.find_one({"_id": oid})
    if not record:
        return None, "Maintenance record not found"

    if record.get("status") == COMPLETED:
        return None, "Maintenance record is already closed"

    maintenance_col.update_one({"_id": oid}, {"$set": {"status": COMPLETED}})

    vehicle = vehicles_col.find_one({"_id": record["vehicleId"]})
    if vehicle and vehicle.get("status") != RETIRED:
        # Business rule: closing maintenance restores vehicle to AVAILABLE, unless retired
        vehicles_col.update_one({"_id": record["vehicleId"]}, {"$set": {"status": AVAILABLE}})

    updated = maintenance_col.find_one({"_id": oid})
    return serialize_maintenance(updated), None


def get_all_maintenance(filters=None):
    query = filters or {}
    records = list(maintenance_col.find(query))
    return [serialize_maintenance(r) for r in records]
