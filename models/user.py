"""
User document shape (Member 1 -- Authentication & Project Setup).
Provided as the shared schema contract; Member 1 owns register/login/JWT
logic in services/auth_service.py and routes/auth.py.

{
  "_id": ObjectId,
  "name": str,
  "email": str,
  "password": str,      # hashed, never store plaintext
  "role": "Fleet Manager" | "Driver" | "Safety Officer" | "Financial Analyst"
}
"""
from datetime import datetime

from utils.constants import USER_ROLES


def user_document(name, email, hashed_password, role="Fleet Manager"):
    if role not in USER_ROLES:
        raise ValueError(f"role must be one of {USER_ROLES}")
    return {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "createdAt": datetime.utcnow(),
    }
