"""
Initialization module for the Flask application.

This module contains the setup and configuration for the Flask application,
including initializing the SQLAlchemy database instance, the JWTManager, and
registering the main routes blueprint. It defines the `create_app` factory
function that sets up and returns an instance of the Flask application.

Imports:
    - Flask: The Flask class used to create the application instance.
    - SQLAlchemy: The SQLAlchemy class used to manage the database.
    - JWTManager: The JWTManager class used for handling JSON Web Tokens.
    - routes_bp: The main routes blueprint (imported inside the function to avoid circular imports).
    - register_error_handlers: Function to register global error handlers.
"""

from flask import Flask  # Third party import
from config import Config  # First party import
from app.extensions import db, jwt
from app.routes import routes_bp, orders_bp
from app.routes.cart import cart_bp
from app.error_handlers import register_error_handlers

# from app.models import User, Product, Cart, CartItem, Order, OrderItem


def create_app(config_class=Config) -> Flask:
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_class (Type[ConfigType]): The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(cart_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(orders_bp, url_prefix="/api")

    # Register global error handlers
    register_error_handlers(app)

    return app
