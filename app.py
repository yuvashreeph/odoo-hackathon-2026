"""
TransitOps — main entrypoint.

Wires up Member 3's blueprints (drivers, trips) and Member 2's
blueprints (vehicles, maintenance). When the rest of the team merges
in, Member 1's auth blueprint and Member 4's fuel/expense/dashboard
blueprints get added here the same way.
"""
from flask import Flask
from flask_cors import CORS

from config import Config
from database import mongo
from routes.driver import drivers_bp
from routes.trip import trips_bp
from routes.vehicle import vehicles_bp
from routes.maintenance import maintenance_bp
from utils.response import success, error


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(drivers_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(maintenance_bp)

    @app.route("/health", methods=["GET"])
    def health():
        try:
            mongo.ping()
            return success("Service healthy", {"mongo": "connected"})
        except Exception as exc:  # noqa: BLE001
            return error("Service unhealthy", [str(exc)], status_code=503)

    @app.errorhandler(404)
    def not_found(_):
        return error("Route not found", status_code=404)

    @app.errorhandler(500)
    def server_error(_):
        return error("Internal server error", status_code=500)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
