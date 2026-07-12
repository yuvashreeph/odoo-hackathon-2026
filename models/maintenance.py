"""
Maintenance log document shape (Member 2 -- Vehicle & Maintenance).
Provided as the shared schema contract; Member 2 owns CRUD logic in
services/vehicle_service.py (or a dedicated maintenance service) and
routes/maintenance.py.

Business rule: opening a maintenance log sets the linked vehicle's
status to IN_SHOP; closing it (status -> COMPLETED) sets the vehicle
back to AVAILABLE.

{
  "_id": ObjectId,
  "vehicleId": ObjectId,
  "maintenanceType": str,      # e.g. "Oil Change"
  "cost": number,
  "date": datetime,
  "status": "ACTIVE" | "COMPLETED"
}
"""
from datetime import datetime


def maintenance_document(vehicle_id, maintenance_type, cost, date=None, status="ACTIVE"):
    return {
        "vehicleId": vehicle_id,
        "maintenanceType": maintenance_type,
        "cost": cost,
        "date": date or datetime.utcnow(),
        "status": status,
    }
