from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services.auth_service import (
    login,
    logout,
    get_profile
)

from utils.response import success, error

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login_route():

    data = request.get_json()

    if not data:
        return error("Request body is required")

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error("Email and password are required")

    result, err = login(email, password)

    if err:
        return error(err, status_code=401)

    return success(
        "Login successful",
        result
    )


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    profile = get_profile(user_id)

    if not profile:
        return error(
            "User not found",
            status_code=404
        )

    return success(
        "Profile fetched successfully",
        profile
    )


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout_route():

    return success(
        "Logout successful",
        logout()
    )