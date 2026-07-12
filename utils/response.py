"""
Consistent success()/error() JSON helpers — the team's agreed response shape:

  { "success": true,  "message": "...", "data": { ... } }
  { "success": false, "message": "...", "errors": ["...", "..."] }
"""
from flask import jsonify


def success(message="Success", data=None, status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }), status_code


def error(message="Something went wrong", errors=None, status_code=400):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status_code
