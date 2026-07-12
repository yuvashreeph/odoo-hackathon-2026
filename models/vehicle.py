"""
Vehicle document shape (Member 2 -- Vehicle & Maintenance).
Provided as the shared schema contract; Member 2 owns CRUD logic in
services/vehicle_service.py and routes/vehicle.py.

{
  "_id": ObjectId,
  "registrationNumber": str,   # must be unique
  "vehicleName": str,
  "vehicleType": str,
  "maxLoadCapacity": number,   # trips.cargoWeight is validated against this
  "odometer": number,
  "acquisitionCost": number,
  "status": "AVAILABLE" | "ON_TRIP" | "IN_SHOP" | "RETIRED",
  "region": str,
  "createdAt": datetime,
  "updatedAt": datetime
}
"""
from datetime import datetime


def vehicle_document(registration_number, vehicle_name, vehicle_type,
                      max_load_capacity, odometer=0, acquisition_cost=0,
                      status="AVAILABLE", region=None):
    now = datetime.utcnow()
    return {
        "registrationNumber": registration_number,
        "vehicleName": vehicle_name,
        "vehicleType": vehicle_type,
        "maxLoadCapacity": max_load_capacity,
        "odometer": odometer,
        "acquisitionCost": acquisition_cost,
        "status": status,
        "region": region,
        "createdAt": now,
        "updatedAt": now,
    }
