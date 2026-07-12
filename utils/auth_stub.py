"""
TEMPORARY placeholder auth decorator.

This lets Member 3's module (driver + trip routes) run and be tested
standalone before Member 1's real authentication is merged in. It does
NOT check tokens — every request passes through.

--- On merge, delete this file. ---
In routes/driver.py and routes/trip.py, replace:

    from utils.auth_stub import token_required

with the real decorator, e.g.:

    from services.auth_service import token_required
"""
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # NOTE: no token verification here — stub only.
        return f(*args, **kwargs)
    return decorated
