from flask import Blueprint
from flask_jwt_extended import jwt_required

from services.dashboard_service import get_dashboard
from utils.response import success, error

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    try:
        data = get_dashboard()

        return success(
            "Dashboard data fetched successfully",
            data
        )

    except Exception as e:
        return error(
            "Failed to fetch dashboard",
            [str(e)],
            status_code=500
        )