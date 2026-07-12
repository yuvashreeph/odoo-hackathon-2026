"""
Expense document shape (Member 4 -- Dashboard, Reports, Fuel & Expenses).
Provided as the shared schema contract; Member 4 owns CRUD logic in
services/dashboard_service.py (or a dedicated expense service) and
routes/expense.py.

{
  "_id": ObjectId,
  "vehicleId": ObjectId,
  "expenseType": "Toll" | "Repair" | "Insurance" | "Parking" | "Miscellaneous",
  "amount": number,
  "date": datetime
}
"""
from datetime import datetime

from utils.constants import EXPENSE_TYPES


def expense_document(vehicle_id, expense_type, amount, date=None):
    if expense_type not in EXPENSE_TYPES:
        raise ValueError(f"expenseType must be one of {EXPENSE_TYPES}")
    return {
        "vehicleId": vehicle_id,
        "expenseType": expense_type,
        "amount": amount,
        "date": date or datetime.utcnow(),
    }
