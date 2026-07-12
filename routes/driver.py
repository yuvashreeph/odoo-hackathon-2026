from flask import Blueprint, request

from services import driver_service
from utils.response import success, error
from utils.auth_stub import token_required  # SWAP on merge — see README

drivers_bp = Blueprint("drivers_bp", __name__, url_prefix="/drivers")


@drivers_bp.route("", methods=["GET"])
@token_required
def list_drivers():
    search = request.args.get("search")
    status = request.args.get("status")
    drivers = driver_service.list_drivers(search=search, status=status)
    return success("Drivers fetched", drivers)


@drivers_bp.route("/<driver_id>", methods=["GET"])
@token_required
def get_driver(driver_id):
    driver, err = driver_service.get_driver(driver_id)
    if err:
        return error(err, status_code=404)
    return success("Driver fetched", driver)


@drivers_bp.route("", methods=["POST"])
@token_required
def create_driver():
    payload = request.get_json(silent=True) or {}
    driver, errs = driver_service.create_driver(payload)
    if errs:
        return error("Could not create driver", errs, status_code=422)
    return success("Driver Added", driver, status_code=201)


@drivers_bp.route("/<driver_id>", methods=["PUT"])
@token_required
def update_driver(driver_id):
    payload = request.get_json(silent=True) or {}
    driver, errs = driver_service.update_driver(driver_id, payload)
    if errs:
        return error("Could not update driver", errs, status_code=422)
    return success("Driver Updated", driver)


@drivers_bp.route("/<driver_id>", methods=["DELETE"])
@token_required
def delete_driver(driver_id):
    ok, err = driver_service.delete_driver(driver_id)
    if not ok:
        return error(err, status_code=422)
    return success("Driver Deleted")
