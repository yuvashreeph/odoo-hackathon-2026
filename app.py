"""
TransitOps — Main Entry Point
"""

from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database import mongo

# Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.driver import drivers_bp
from routes.trip import trips_bp
from routes.vehicle import vehicles_bp
from routes.maintenance import maintenance_bp

from utils.response import success, error


def create_app():
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    CORS(app)
    JWTManager(app)

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(maintenance_bp)

    # -------------------------
    # HTML Pages
    # -------------------------

    @app.route("/")
    def home():
        return render_template("login.html")

    @app.route("/dashboard-page")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/drivers-page")
    def drivers_page():
        return render_template("drivers.html")

    @app.route("/trips-page")
    def trips_page():
        return render_template("trips.html")

    @app.route("/vehicles-page")
    def vehicles_page():
        return render_template("vehicles.html")

    @app.route("/maintenance-page")
    def maintenance_page():
        return render_template("maintenance.html")

    # -------------------------
    # Health Check
    # -------------------------

    @app.route("/health")
    def health():
        try:
            mongo.ping()
            return success(
                "Service healthy",
                {"mongo": "connected"}
            )
        except Exception as exc:
            return error(
                "Service unhealthy",
                [str(exc)],
                status_code=503
            )

    # -------------------------
    # Error Handlers
    # -------------------------

    @app.errorhandler(404)
    def not_found(_):
        return error(
            "Route not found",
            status_code=404
        )

    @app.errorhandler(500)
    def internal_error(_):
        return error(
            "Internal server error",
            status_code=500
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=Config.DEBUG
    )