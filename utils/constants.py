"""
Shared status enums — the whole team imports from here.
Nobody redefines these locally or uses different casing.
"""

VEHICLE_STATUS = ["AVAILABLE", "ON_TRIP", "IN_SHOP", "RETIRED"]

DRIVER_STATUS = ["AVAILABLE", "ON_TRIP", "OFF_DUTY", "SUSPENDED"]

TRIP_STATUS = ["DRAFT", "DISPATCHED", "COMPLETED", "CANCELLED"]

MAINTENANCE_STATUS = ["ACTIVE", "COMPLETED"]

USER_ROLES = ["Fleet Manager", "Driver", "Safety Officer", "Financial Analyst"]

EXPENSE_TYPES = ["Toll", "Repair", "Insurance", "Parking", "Miscellaneous"]

# Shared Mongo collection names — everyone must use these exact names.
COLLECTION_USERS = "users"
COLLECTION_VEHICLES = "vehicles"
COLLECTION_DRIVERS = "drivers"
COLLECTION_TRIPS = "trips"
COLLECTION_MAINTENANCE_LOGS = "maintenance_logs"
COLLECTION_FUEL_LOGS = "fuel_logs"
COLLECTION_EXPENSES = "expenses"
