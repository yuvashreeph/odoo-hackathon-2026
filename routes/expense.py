"""
Expense API routes.

Member 4 -- Dashboard, Reports, Fuel & Expenses.

Endpoints:
    GET  /expenses
    POST /expenses
"""

from flask import Blueprint, request

from services import dashboard_service
from utils.response import success, error
from utils.auth_stub import token_required


expense_bp = Blueprint(
    "expense_bp",
    __name__,
    url_prefix="/expenses"
)


# -----------------------------------
# Get all expenses
# -----------------------------------
@expense_bp.route("", methods=["GET"])
@token_required
def list_expenses():

    expenses = dashboard_service.list_expenses()

    return success(
        "Expenses fetched",
        expenses
    )


# -----------------------------------
# Create expense
# -----------------------------------
@expense_bp.route("", methods=["POST"])
@token_required
def create_expense():

    payload = request.get_json(silent=True) or {}

    expense, errs = dashboard_service.create_expense(payload)

    if errs:
        return error(
            "Could not create expense",
            errs,
            status_code=422
        )

    return success(
        "Expense created",
        expense,
        status_code=201
    )