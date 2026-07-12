"""
Fuel & Expense business logic.
Member 4
"""

from database.mongo import fuel_logs_collection, expenses_collection
from models.fuel import fuel_log_document
from models.expense import expense_document
from utils.validators import (
    to_object_id,
    parse_date,
    serialize_document,
)


# ======================================================
# Fuel CRUD
# ======================================================

def list_fuel_logs():
    docs = fuel_logs_collection.find().sort("date", -1)
    return [serialize_document(doc) for doc in docs]


def create_fuel_log(payload):
    required = [
        "vehicleId",
        "tripId",
        "liters",
        "cost"
    ]

    missing = [field for field in required if not payload.get(field)]

    if missing:
        return None, [f"Missing field: {field}" for field in missing]

    vehicle_id = to_object_id(payload["vehicleId"])
    trip_id = to_object_id(payload["tripId"])

    if vehicle_id is None:
        return None, ["Invalid vehicleId"]

    if trip_id is None:
        return None, ["Invalid tripId"]

    date = None
    if payload.get("date"):
        date = parse_date(payload["date"])
        if date is None:
            return None, ["date must be YYYY-MM-DD"]

    doc = fuel_log_document(
        vehicle_id=vehicle_id,
        trip_id=trip_id,
        liters=float(payload["liters"]),
        cost=float(payload["cost"]),
        date=date,
    )

    result = fuel_logs_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    return serialize_document(doc), None


# ======================================================
# Expense CRUD
# ======================================================

def list_expenses():
    docs = expenses_collection.find().sort("date", -1)
    return [serialize_document(doc) for doc in docs]


def create_expense(payload):
    required = [
        "vehicleId",
        "expenseType",
        "amount"
    ]

    missing = [field for field in required if not payload.get(field)]

    if missing:
        return None, [f"Missing field: {field}" for field in missing]

    vehicle_id = to_object_id(payload["vehicleId"])

    if vehicle_id is None:
        return None, ["Invalid vehicleId"]

    date = None
    if payload.get("date"):
        date = parse_date(payload["date"])
        if date is None:
            return None, ["date must be YYYY-MM-DD"]

    try:
        doc = expense_document(
            vehicle_id=vehicle_id,
            expense_type=payload["expenseType"],
            amount=float(payload["amount"]),
            date=date,
        )
    except ValueError as exc:
        return None, [str(exc)]

    result = expenses_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    return serialize_document(doc), None