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
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import routes_bp

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class="config.Config"):
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_class (str): The configuration class to use for the application.
                            Defaults to "config.Config".

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # Register main blueprint
    app.register_blueprint(routes_bp)

    return app
