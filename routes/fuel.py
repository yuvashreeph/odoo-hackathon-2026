from flask import Blueprint, request

from services import dashboard_service
from utils.response import success, error
from utils.auth_stub import token_required

fuel_bp = Blueprint("fuel_bp", __name__, url_prefix="/fuel")


@fuel_bp.route("", methods=["GET"])
@token_required
def list_fuel_logs():
    fuel_logs = dashboard_service.list_fuel_logs()
    return success("Fuel logs fetched", fuel_logs)


@fuel_bp.route("", methods=["POST"])
@token_required
def create_fuel_log():
    payload = request.get_json(silent=True) or {}

    fuel_log, errs = dashboard_service.create_fuel_log(payload)

    if errs:
        return error("Could not create fuel log", errs, status_code=422)

    return success(
        "Fuel log created",
        fuel_log,
        status_code=201
    )