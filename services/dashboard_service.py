"""
Dashboard, Fuel & Expense business logic.
Member 4
"""

from database.mongo import (
    fuel_logs_collection,
    expenses_collection,
    trips_collection,
    vehicles_collection,
    drivers_collection
)

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

    return [
        serialize_document(doc)
        for doc in docs
    ]



def create_fuel_log(payload):

    required = [
        "vehicleId",
        "tripId",
        "liters",
        "cost"
    ]


    missing = [
        field
        for field in required
        if not payload.get(field)
    ]


    if missing:
        return None, [
            f"Missing field: {field}"
            for field in missing
        ]


    vehicle_id = to_object_id(
        payload["vehicleId"]
    )

    trip_id = to_object_id(
        payload["tripId"]
    )


    if vehicle_id is None:
        return None, ["Invalid vehicleId"]


    if trip_id is None:
        return None, ["Invalid tripId"]



    date = None


    if payload.get("date"):

        date = parse_date(
            payload["date"]
        )

        if date is None:
            return None, [
                "date must be YYYY-MM-DD"
            ]



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

    return [
        serialize_document(doc)
        for doc in docs
    ]



def create_expense(payload):

    required = [
        "vehicleId",
        "expenseType",
        "amount"
    ]


    missing = [
        field
        for field in required
        if not payload.get(field)
    ]


    if missing:
        return None, [
            f"Missing field: {field}"
            for field in missing
        ]



    vehicle_id = to_object_id(
        payload["vehicleId"]
    )


    if vehicle_id is None:
        return None, [
            "Invalid vehicleId"
        ]



    date = None


    if payload.get("date"):

        date = parse_date(
            payload["date"]
        )


        if date is None:
            return None, [
                "date must be YYYY-MM-DD"
            ]



    try:

        doc = expense_document(
            vehicle_id=vehicle_id,
            expense_type=payload["expenseType"],
            amount=float(payload["amount"]),
            date=date,
        )


    except ValueError as exc:

        return None, [
            str(exc)
        ]



    result = expenses_collection.insert_one(doc)

    doc["_id"] = result.inserted_id


    return serialize_document(doc), None



# ======================================================
# Dashboard KPIs
# ======================================================


def get_dashboard_summary():


    total_vehicles = vehicles_collection.count_documents({})


    available_vehicles = vehicles_collection.count_documents(
        {
            "status": "AVAILABLE"
        }
    )


    maintenance_vehicles = vehicles_collection.count_documents(
        {
            "status": "IN_SHOP"
        }
    )


    active_vehicles = vehicles_collection.count_documents(
        {
            "status": "ON_TRIP"
        }
    )


    total_drivers = drivers_collection.count_documents({})


    drivers_on_duty = drivers_collection.count_documents(
        {
            "status": "ON_TRIP"
        }
    )


    active_trips = trips_collection.count_documents(
        {
            "status": "DISPATCHED"
        }
    )


    pending_trips = trips_collection.count_documents(
        {
            "status": "DRAFT"
        }
    )



    total_fuel_cost = sum(
        item.get("cost", 0)
        for item in fuel_logs_collection.find()
    )


    total_expenses = sum(
        item.get("amount", 0)
        for item in expenses_collection.find()
    )



    utilization = 0


    if total_vehicles > 0:

        utilization = (
            active_vehicles / total_vehicles
        ) * 100



    return {

        "totalVehicles": total_vehicles,

        "activeVehicles": active_vehicles,

        "availableVehicles": available_vehicles,

        "vehiclesInMaintenance": maintenance_vehicles,


        "totalDrivers": total_drivers,

        "driversOnDuty": drivers_on_duty,


        "activeTrips": active_trips,

        "pendingTrips": pending_trips,


        "totalFuelCost": total_fuel_cost,

        "totalExpenses": total_expenses,


        "fleetUtilizationPercentage": round(
            utilization,
            2
        )
    }



# ======================================================
# Reports
# ======================================================


def get_reports():


    total_fuel_cost = sum(
        item.get("cost", 0)
        for item in fuel_logs_collection.find()
    )



    total_expenses = sum(
        item.get("amount", 0)
        for item in expenses_collection.find()
    )



    operational_cost = (
        total_fuel_cost +
        total_expenses
    )



    total_liters = sum(
        item.get("liters", 0)
        for item in fuel_logs_collection.find()
    )



    total_distance = sum(
        item.get("actualDistance", 0)
        for item in trips_collection.find()
        if item.get("actualDistance")
    )



    fuel_efficiency = 0


    if total_liters > 0:

        fuel_efficiency = (
            total_distance /
            total_liters
        )



    total_revenue = sum(
        item.get("revenue", 0)
        for item in trips_collection.find()
        if item.get("revenue")
    )



    vehicle_count = vehicles_collection.count_documents({})


    vehicle_roi = 0


    if vehicle_count > 0:

        vehicle_roi = (
            total_revenue /
            vehicle_count
        )



    return {

        "totalFuelCost": total_fuel_cost,

        "totalExpenses": total_expenses,

        "operationalCost": operational_cost,

        "fuelEfficiency": round(
            fuel_efficiency,
            2
        ),

        "totalRevenue": total_revenue,

        "vehicleROI": round(
            vehicle_roi,
            2
        )

    }