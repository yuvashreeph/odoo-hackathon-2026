"""
Member 1 -- Authentication & Project Setup. Not part of Member 3's
(Driver + Trip) submission -- stub only.

This is where the REAL token_required decorator should live once built.
On merge, routes/driver.py and routes/trip.py switch their import from
    utils.auth_stub.token_required
to
    services.auth_service.token_required

Work to implement here:
    - register(payload) -> hash password, insert into users_collection
    - login(email, password) -> verify + issue JWT
    - token_required(f) -> real @jwt_required-style decorator
    - role_required(*roles) -> optional RBAC decorator
"""
