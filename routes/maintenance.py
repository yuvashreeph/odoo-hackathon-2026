"""
Member 2 -- Vehicle & Maintenance. Not part of Member 3's (Driver +
Trip) submission -- stub only.

Collections: maintenance_logs (also updates vehicles.status)

APIs to implement here:
    POST /maintenance
    PUT  /maintenance/close

Business rules:
    - Opening a maintenance log -> linked vehicle.status = IN_SHOP
    - Closing it (status -> COMPLETED) -> linked vehicle.status = AVAILABLE

See models/maintenance.py for the shared document shape.
"""
