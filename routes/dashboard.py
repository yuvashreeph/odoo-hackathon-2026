"""
Dashboard APIs.
Member 4
"""

from flask import Blueprint

from services import dashboard_service

from utils.response import success

from utils.auth_stub import token_required



dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__,
    url_prefix="/dashboard"
)



@dashboard_bp.route(
    "",
    methods=["GET"]
)
@token_required
def dashboard():

    data = dashboard_service.get_dashboard_summary()

    return success(
        "Dashboard data fetched",
        data
    )