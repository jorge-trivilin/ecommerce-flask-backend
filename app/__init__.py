# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # Import routes main Blueprint
    from app.routes import routes_bp

    # Register main blueprint
    app.register_blueprint(routes_bp)

    return app
