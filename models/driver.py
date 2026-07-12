"""
Driver document shape (Mongo is schemaless — this just centralizes field
names so nobody types `licenseExpiry` one way and `license_expiry`
another).

{
  "_id": ObjectId,
  "name": str,
  "licenseNumber": str,
  "licenseCategory": str,
  "licenseExpiry": datetime,
  "phone": str,
  "safetyScore": int,
  "status": "AVAILABLE" | "ON_TRIP" | "OFF_DUTY" | "SUSPENDED",
  "createdAt": datetime,
  "updatedAt": datetime
}
"""
from datetime import datetime


def driver_document(name, license_number, license_category, license_expiry,
                     phone, safety_score=100, status="AVAILABLE"):
    now = datetime.utcnow()
    return {
        "name": name,
        "licenseNumber": license_number,
        "licenseCategory": license_category,
        "licenseExpiry": license_expiry,
        "phone": phone,
        "safetyScore": safety_score,
        "status": status,
        "createdAt": now,
        "updatedAt": now,
    }
