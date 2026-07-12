from flask import Blueprint, request

from services import trip_service
from utils.response import success, error
from utils.auth_stub import token_required  # SWAP on merge — see README

trips_bp = Blueprint("trips_bp", __name__, url_prefix="/trips")


@trips_bp.route("", methods=["GET"])
@token_required
def list_trips():
    status = request.args.get("status")
    trips = trip_service.list_trips(status=status)
    return success("Trips fetched", trips)


@trips_bp.route("/<trip_id>", methods=["GET"])
@token_required
def get_trip(trip_id):
    trip, err = trip_service.get_trip(trip_id)
    if err:
        return error(err, status_code=404)
    return success("Trip fetched", trip)


@trips_bp.route("", methods=["POST"])
@token_required
def create_trip():
    payload = request.get_json(silent=True) or {}
    trip, errs = trip_service.create_trip(payload)
    if errs:
        return error("Could not create trip", errs, status_code=422)
    return success("Trip Created", trip, status_code=201)


@trips_bp.route("/<trip_id>", methods=["PUT"])
@token_required
def update_trip(trip_id):
    payload = request.get_json(silent=True) or {}
    trip, errs = trip_service.update_trip(trip_id, payload)
    if errs:
        return error("Could not update trip", errs, status_code=422)
    return success("Trip Updated", trip)


@trips_bp.route("/<trip_id>", methods=["DELETE"])
@token_required
def delete_trip(trip_id):
    ok, err = trip_service.delete_trip(trip_id)
    if not ok:
        return error(err, status_code=422)
    return success("Trip Deleted")


@trips_bp.route("/<trip_id>/dispatch", methods=["PUT"])
@token_required
def dispatch_trip(trip_id):
    trip, errs = trip_service.dispatch_trip(trip_id)
    if errs:
        return error("Dispatch failed", errs, status_code=422)
    return success("Trip Dispatched", trip)


@trips_bp.route("/<trip_id>/complete", methods=["PUT"])
@token_required
def complete_trip(trip_id):
    payload = request.get_json(silent=True) or {}
    trip, errs = trip_service.complete_trip(
        trip_id,
        actual_distance=payload.get("actualDistance"),
        fuel_used=payload.get("fuelUsed"),
        revenue=payload.get("revenue"),
    )
    if errs:
        return error("Could not complete trip", errs, status_code=422)
    return success("Trip Completed", trip)


@trips_bp.route("/<trip_id>/cancel", methods=["PUT"])
@token_required
def cancel_trip(trip_id):
    trip, errs = trip_service.cancel_trip(trip_id)
    if errs:
        return error("Could not cancel trip", errs, status_code=422)
    return success("Trip Cancelled", trip)
