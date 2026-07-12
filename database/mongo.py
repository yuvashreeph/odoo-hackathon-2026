"""
Single Mongo connection, shared by every module. Collection names come
from utils/constants.py so nobody on the team drifts into `vehicle` vs
`vehicles` type mismatches.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from utils.constants import (
    COLLECTION_USERS,
    COLLECTION_VEHICLES,
    COLLECTION_DRIVERS,
    COLLECTION_TRIPS,
    COLLECTION_MAINTENANCE_LOGS,
    COLLECTION_FUEL_LOGS,
    COLLECTION_EXPENSES,
)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "transitops")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db[COLLECTION_USERS]
vehicles_collection = db[COLLECTION_VEHICLES]
drivers_collection = db[COLLECTION_DRIVERS]
trips_collection = db[COLLECTION_TRIPS]
maintenance_logs_collection = db[COLLECTION_MAINTENANCE_LOGS]
fuel_logs_collection = db[COLLECTION_FUEL_LOGS]
expenses_collection = db[COLLECTION_EXPENSES]


def ping():
    """Quick connectivity check used by /health."""
    client.admin.command("ping")
    return True
