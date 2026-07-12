"""
Trip document shape.

{
  "_id": ObjectId,
  "source": str,
  "destination": str,
  "vehicleId": ObjectId,
  "driverId": ObjectId,
  "cargoWeight": number,
  "plannedDistance": number,
  "actualDistance": number | None,
  "fuelUsed": number | None,
  "revenue": number | None,
  "status": "DRAFT" | "DISPATCHED" | "COMPLETED" | "CANCELLED",
  "createdAt": datetime,
  "updatedAt": datetime
}
"""
from datetime import datetime


def trip_document(source, destination, vehicle_id, driver_id, cargo_weight,
                   planned_distance, revenue=None, status="DRAFT"):
    now = datetime.utcnow()
    return {
        "source": source,
        "destination": destination,
        "vehicleId": vehicle_id,
        "driverId": driver_id,
        "cargoWeight": cargo_weight,
        "plannedDistance": planned_distance,
        "actualDistance": None,
        "fuelUsed": None,
        "revenue": revenue,
        "status": status,
        "createdAt": now,
        "updatedAt": now,
    }
