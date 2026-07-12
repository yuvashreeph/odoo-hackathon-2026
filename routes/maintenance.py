"""
Maintenance API routes (Member 2 — Fleet Manager module)
"""

from flask import Blueprint, request

from services.vehicle_service import (
    create_maintenance, close_maintenance, get_all_maintenance,
)
from models.maintenance import validate_maintenance_payload
from utils.response import success, error
from utils.auth_stub import token_required
from utils.validators import to_object_id

maintenance_bp = Blueprint("maintenance", __name__)


@maintenance_bp.route("/maintenance", methods=["POST"])
@token_required
def add_maintenance():
    data = request.get_json(silent=True) or {}

    errors = validate_maintenance_payload(data)
    if errors:
        return error("Validation failed", errors=errors, status_code=422)

    record, err = create_maintenance(data)
    if err:
        return error(err, status_code=409)

    return success("Maintenance record created, vehicle moved to IN_SHOP", record, 201)


@maintenance_bp.route("/maintenance/close/<maintenanceId>", methods=["PUT"])
@token_required
def finish_maintenance(maintenanceId):
    record, err = close_maintenance(maintenanceId)
    if err:
        status_code = 404 if "not found" in err.lower() else 409
        return error(err, status_code=status_code)
    return success("Maintenance closed, vehicle status updated", record)


@maintenance_bp.route("/maintenance", methods=["GET"])
@token_required
def list_maintenance():
    filters = {}
    vehicle_id = request.args.get("vehicleId")
    if vehicle_id:
        oid = to_object_id(vehicle_id)
        if oid:
            filters["vehicleId"] = oid

    records = get_all_maintenance(filters)
    return success("Maintenance records fetched", records)
