from flask import Flask
from flask_cors import CORS
from config import Config
from database import close_db, get_db
from middleware.error_handler import register_error_handlers

from routes.main_routes import main_bp
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp
from routes.report_routes import report_bp
from routes.admin_routes import admin_bp

def create_app(config_class=Config):
    """Application factory for initializing the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS
    CORS(app)

    # Register request-scoped database teardown
    app.teardown_appcontext(close_db)

    # Register centralized error handlers
    register_error_handlers(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        get_db()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print("Rodando em http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
