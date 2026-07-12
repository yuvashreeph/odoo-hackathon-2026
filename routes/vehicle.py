"""
Vehicle API routes (Member 2 — Fleet Manager module)
"""

from flask import Blueprint, request

from services.vehicle_service import (
    create_vehicle, get_all_vehicles, get_vehicle_by_id,
    update_vehicle, delete_vehicle,
)
from models.vehicle import validate_vehicle_payload
from utils.response import success, error
from utils.auth_stub import token_required

vehicles_bp = Blueprint("vehicles", __name__)


@vehicles_bp.route("/vehicles", methods=["POST"])
@token_required
def add_vehicle():
    data = request.get_json(silent=True) or {}

    errors = validate_vehicle_payload(data)
    if errors:
        return error("Validation failed", errors=errors, status_code=422)

    vehicle, err = create_vehicle(data)
    if err:
        return error(err, status_code=409)

    return success("Vehicle created", vehicle, 201)


@vehicles_bp.route("/vehicles", methods=["GET"])
@token_required
def list_vehicles():
    filters = {}
    status = request.args.get("status")
    vehicle_type = request.args.get("type")
    region = request.args.get("region")

    if status:
        filters["status"] = status
    if vehicle_type:
        filters["vehicleType"] = vehicle_type
    if region:
        filters["region"] = region

    vehicles = get_all_vehicles(filters)
    return success("Vehicles fetched", vehicles)


@vehicles_bp.route("/vehicles/<id>", methods=["GET"])
@token_required
def get_vehicle(id):
    vehicle, err = get_vehicle_by_id(id)
    if err:
        return error(err, status_code=404)
    return success("Vehicle fetched", vehicle)


@vehicles_bp.route("/vehicles/<id>", methods=["PUT"])
@token_required
def edit_vehicle(id):
    data = request.get_json(silent=True) or {}
    vehicle, err = update_vehicle(id, data)
    if err:
        status_code = 404 if "not found" in err.lower() else 409
        return error(err, status_code=status_code)
    return success("Vehicle updated", vehicle)


@vehicles_bp.route("/vehicles/<id>", methods=["DELETE"])
@token_required
def remove_vehicle(id):
    ok, err = delete_vehicle(id)
    if not ok:
        status_code = 404 if "not found" in err.lower() else 409
        return error(err, status_code=status_code)
    return success("Vehicle deleted", None)
