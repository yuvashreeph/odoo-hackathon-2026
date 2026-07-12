"""
CSV Export API
Member 4
"""

from flask import Blueprint, Response

from services import dashboard_service
from utils.auth_stub import token_required


export_bp = Blueprint(
    "export_bp",
    __name__,
    url_prefix="/export"
)


@export_bp.route("/csv", methods=["GET"])
@token_required
def export_csv():

    csv_data = dashboard_service.generate_csv()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=transitops_report.csv"
        }
    )