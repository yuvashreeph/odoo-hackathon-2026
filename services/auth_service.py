"""
Authentication service.

Handles:
- Login
- JWT creation
- Password verification
- User profile
"""

from bson import ObjectId
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from database.mongo import users_collection


def login(email, password):
    """
    Authenticate a user and return JWT token.
    """

    user = users_collection.find_one({"email": email})

    if not user:
        return None, "Invalid email or password"

    if not check_password_hash(user["password"], password):
        return None, "Invalid email or password"

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={
            "role": user["role"],
            "name": user["name"]
        }
    )

    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }, None


def get_profile(user_id):
    """
    Fetch profile of logged-in user.
    """

    try:
        user = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )

        if not user:
            return None

        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }

    except Exception:
        return None


def logout():
    """
    JWT is stateless.
    Client only needs to delete the token.
    """

    return {
        "message": "Logout successful"
    }