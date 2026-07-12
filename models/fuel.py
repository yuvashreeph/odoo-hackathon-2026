"""
Fuel log document shape (Member 4 -- Dashboard, Reports, Fuel & Expenses).
Provided as the shared schema contract; Member 4 owns CRUD logic in
services/dashboard_service.py (or a dedicated fuel service) and
routes/fuel.py.

{
  "_id": ObjectId,
  "vehicleId": ObjectId,
  "tripId": ObjectId,
  "liters": number,
  "cost": number,
  "date": datetime
}
"""
from datetime import datetime


def fuel_log_document(vehicle_id, trip_id, liters, cost, date=None):
    return {
        "vehicleId": vehicle_id,
        "tripId": trip_id,
        "liters": liters,
        "cost": cost,
        "date": date or datetime.utcnow(),
    }
