"""
TransitOps — main entrypoint.

Currently wires up only Member 3's blueprints (drivers, trips) so this
module can be developed and demoed standalone. When the team merges,
Member 1's app.py becomes the single source of truth — just make sure
`drivers_bp` and `trips_bp` get registered there exactly as below.
"""
from flask import Flask
from flask_cors import CORS

from config import Config
from database import mongo
from routes.driver import drivers_bp
from routes.trip import trips_bp
from utils.response import success, error
from routes.fuel import fuel_bp
from routes.expense import expense_bp
from routes.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(drivers_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(fuel_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(dashboard_bp)

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
