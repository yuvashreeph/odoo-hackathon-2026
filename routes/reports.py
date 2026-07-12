"""
Reports API
Member 4
"""

from flask import Blueprint

from services import dashboard_service

from utils.response import success

from utils.auth_stub import token_required



reports_bp = Blueprint(
    "reports_bp",
    __name__,
    url_prefix="/reports"
)



@reports_bp.route("", methods=["GET"])
@token_required
def reports():

    data = dashboard_service.get_reports()

    return success(
        "Reports generated",
        data
    )