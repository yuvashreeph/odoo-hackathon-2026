"""
Dashboard Service

Calculates dashboard KPIs from MongoDB collections.
"""

from database.mongo import (
    vehicles_collection,
    drivers_collection,
    trips_collection,
)


def get_dashboard():
    """Return all dashboard KPI values."""

    # Vehicle KPIs
    total_vehicles = vehicles_collection.count_documents({})

    available_vehicles = vehicles_collection.count_documents({
        "status": "AVAILABLE"
    })

    vehicles_on_trip = vehicles_collection.count_documents({
        "status": "ON_TRIP"
    })

    vehicles_in_shop = vehicles_collection.count_documents({
        "status": "IN_SHOP"
    })

    # Trip KPIs
    active_trips = trips_collection.count_documents({
        "status": {
            "$in": ["ACTIVE", "DISPATCHED"]
        }
    })

    completed_trips = trips_collection.count_documents({
        "status": "COMPLETED"
    })

    cancelled_trips = trips_collection.count_documents({
        "status": "CANCELLED"
    })

    # Driver KPIs
    drivers_available = drivers_collection.count_documents({
        "status": "AVAILABLE"
    })

    drivers_on_trip = drivers_collection.count_documents({
        "status": "ON_TRIP"
    })

    # Fleet Utilization
    fleet_utilization = 0

    if total_vehicles > 0:
        fleet_utilization = round(
            (vehicles_on_trip / total_vehicles) * 100,
            2
        )

    return {

        "totalVehicles": total_vehicles,

        "availableVehicles": available_vehicles,

        "vehiclesOnTrip": vehicles_on_trip,

        "vehiclesInShop": vehicles_in_shop,

        "activeTrips": active_trips,

        "driversAvailable": drivers_available,

        "driversOnTrip": drivers_on_trip,

        "fleetUtilization": fleet_utilization,

        "vehicleStatusChart": {
            "Available": available_vehicles,
            "On Trip": vehicles_on_trip,
            "In Shop": vehicles_in_shop
        },

        "tripStatusChart": {
            "Active": active_trips,
            "Completed": completed_trips,
            "Cancelled": cancelled_trips
        }

    }